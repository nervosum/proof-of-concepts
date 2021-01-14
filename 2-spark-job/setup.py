from setuptools import setup, find_packages

setup(
    name="poc-spark-job",
    packages=find_packages(),
    version="0.0.1",
    author="Nervosum",
	install_requires=["scikit-learn==0.23.2", "joblib==0.17.0", "pandas==1.1.3"],
	python_requires=">=3.7",
)
