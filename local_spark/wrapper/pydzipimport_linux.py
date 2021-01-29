"""Replacement for `zipimport.zipimporter` which allows C extension
modules to be loaded.
To use::
    import pydzipimport
    pydzipimport.install()
Create a zip file which contains any number of modules or packages,
add the zip file to `sys.path` and import as usual.
"""

# -----------------------------------------------------------------------------
#  Copyright (C) 2012 Bradley Froehle <brad.froehle@gmail.com>

#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# -----------------------------------------------------------------------------


__version__ = "0.1"

import imp
import os
import sys
import tempfile
import warnings
import zipimport
import pathlib
import glob

from importlib.machinery import EXTENSION_SUFFIXES

import logging

logger = logging.getLogger()
logger.setLevel("INFO")
if logger.handlers == []:
    logger.addHandler(logging.StreamHandler())

__all__ = [
    "PydZipImporter",
    "TemporaryExtensionFileLoader",
    "install",
    "uninstall",
]


tmp_library_folder = tempfile.TemporaryDirectory()


def _call_with_frames_removed(f, *args, **kwds):
    """remove_importlib_frames in import.c will always remove sequences
    of importlib frames that end with a call to this function
    """
    return f(*args, **kwds)


class PydZipImporter(zipimport.zipimporter):
    """A ZipImporter which allows loading C extension modules.
    To load a C extension module, the shared object contents are
    writen to a temporary file.
    """

    _extension_searchorder = [
        os.sep + "__init__" + s for s in EXTENSION_SUFFIXES
    ] + EXTENSION_SUFFIXES

    def _get_extension_module_info(self, fullname):
        """Get the suffix & path of the extension module by name 'fullname',
        returing `None` if no extension module is found.
        """
        subname = fullname.split(".")[-1]
        path = self.prefix + subname.replace(".", os.sep)

        for suffix in self._extension_searchorder:
            fullpath = path + suffix
            if fullpath in self._files:
                return suffix, fullpath

    # We replace the machinery used to find modules by one which first
    # checks for the existence of a C extension module in the archive,
    # before deferring to zipimport.zipimporter.

    def is_package(self, fullname):
        """Return a bool signifying whether the module is a package or not."""
        info = self._get_extension_module_info(fullname)
        if info and info[0].startswith(os.sep + "__init__"):
            return True
        return super().is_package(fullname)

    def find_module(self, fullname, path=None):
        """Check whether we can satisfy the import of the module named by
        'fullname'. Return self if we can, None if we can't."""
        loader, portions = self.find_loader(fullname, path)
        if loader is None and len(portions):
            msg = "Not importing directory {}: missing __init__"
            warnings.warn(msg.format(portions[0]), ImportWarning)
        return loader

    def find_loader(self, fullname, path=None):
        """Check whether we can satisfy the import of the module named by
        'fullname', or whether it could be a portion of a namespace
        package.
        """
        info = self._get_extension_module_info(fullname)

        if info:
            suffix, fullpath = info
            fakepath = self.archive + os.sep + fullpath

            data = self.get_data(fullpath)
            if ".so" in suffix:
                extra_libs = []
                module_name = fullpath.split("/")[0]
                if module_name == "sklearn":
                    dylib_dr = "scikit_learn.libs"
                else:
                    dylib_dr = module_name + ".libs/"
                dylib_files = [
                    x
                    for x in self._files.keys()
                    if (dylib_dr in x) and ".so" in str(x)
                ]

                # if (dylib_dr in x) and str(x).endswith(".dylib")
                for lib_path in dylib_files:
                    new_lib_path = os.path.join(
                        tmp_library_folder.name, lib_path
                    )

                    if len(glob.glob(new_lib_path, recursive=True)) == 0:
                        # create parent paths
                        parent_dir = os.path.join(
                            tmp_library_folder.name, *lib_path.split("/")[:-1]
                        )
                        pathlib.Path(parent_dir).mkdir(
                            parents=True, exist_ok=True
                        )
                        lib_data = self.get_data(lib_path)

                        with open(new_lib_path, "wb") as f:
                            f.write(lib_data)
                            f.flush()

                    extra_libs.append([lib_path, new_lib_path])

                return (
                    TemporaryExtensionFolderLoader(
                        fullname,
                        fakepath,
                        so_path=fullpath,
                        so_content=data,
                        module_name=module_name,
                        extra_libs=extra_libs,
                    ),
                    [],
                )

            ext = suffix
            if ext.startswith(os.sep + "__init__"):
                x = len(os.sep + "__init__")
                ext = ext[x:]
            ext = "." + fullname.split(".")[-1] + ext

            return (
                TemporaryExtensionFileLoader(fullname, fakepath, data, ext),
                [],
            )

        return super().find_loader(fullname, path)


class TemporaryExtensionFileLoader:
    """An extension file loader which takes a (fake) path and bytearray
    of data. The shared object (given in data) is written to a named
    temporary file before being loaded.
    Based upon `importlib.machinery.ExtensionFileLoader`.
    """

    def __init__(self, name, path, data, suffix):
        self.data = tempfile.NamedTemporaryFile(suffix=suffix)
        self.data.write(data)
        self.data.flush()
        self.path = path
        self.name = name

    def load_module(self, fullname):
        """Load an extension module."""
        # @_check_name
        if fullname is None:
            fullname = self.name
        elif fullname != self.name:
            raise ImportError(
                "loader cannot handle %s" % self.name, name=self.name
            )

        is_reload = fullname in sys.modules
        try:
            module = _call_with_frames_removed(
                imp.load_dynamic, fullname, self.data.name
            )
            module.__file__ = self.path  # Set this to our fake path!
            if self.is_package(fullname) and not hasattr(module, "__path__"):
                module.__path__ = [os.path.split(self.path)[0]]

            # @set_loader
            if not hasattr(module, "__loader__"):
                module.__loader__ = self

            # @set_package
            if getattr(module, "__package__", None) is None:
                module.__package__ = module.__name__
                if not hasattr(module, "__path__"):
                    module.__package__ = module.__package__.rpartition(".")[0]

            return module
        except Exception:
            if not is_reload and fullname in sys.modules:
                del sys.modules[fullname]
            raise

    def is_package(self, fullname):
        """Return True if the extension module is a package."""
        file_name = os.path.split(self.path)[1]
        return any(
            file_name == "__init__" + suffix for suffix in EXTENSION_SUFFIXES
        )

    def get_code(self, fullname):
        """Return None as an extension module cannot create a code object."""
        return None

    def get_source(self, fullname):
        """Return None as extension modules have no source code."""
        return None


class TemporaryExtensionFolderLoader(TemporaryExtensionFileLoader):
    """An extension folder loader which takes a (fake) path and bytearray
    of data. The shared object (given in data) is written to a named
    temporary file before being loaded.
    Based upon `importlib.machinery.ExtensionFileLoader`.
    """

    def __init__(
        self, name, path, so_path, so_content, module_name, extra_libs
    ):
        self.folder = tempfile.TemporaryDirectory()

        pathlib.Path(
            os.path.join(self.folder.name, *so_path.split("/")[:-1])
        ).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(self.folder.name, so_path), "wb") as f:
            f.write(so_content)
            f.flush()

        for lib in extra_libs:
            pathlib.Path(
                os.path.join(self.folder.name, *lib[0].split("/")[:-1])
            ).mkdir(parents=True, exist_ok=True)

            os.symlink(lib[1], os.path.join(self.folder.name, lib[0]))

        self.data = open(os.path.join(self.folder.name, so_path), "rb")
        self.path = path
        self.name = name


def install():
    """Replace the zipimport.zipimporter path hook with PydZipImporter."""
    idx = sys.path_hooks.index(zipimport.zipimporter)
    sys.path_hooks[idx] = PydZipImporter
    sys.path_importer_cache.clear()


def uninstall():
    """Restore the original zipimport.zipimporter path hook."""
    idx = sys.path_hooks.index(PydZipImporter)
    sys.path_hooks[idx] = zipimport.zipimporter
    sys.path_importer_cache.clear()
