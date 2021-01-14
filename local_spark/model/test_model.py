from .model import predict


def test_predict():
    assert predict([[1, 2, 3, 4]])[0] == 2
