import numpy as np

X = 2 * np.random.randn(100, 5)
y = 45 * np.exp(np.cos(X[:, 3])) + X[:, 0] ** 2 - 10.5


from pysr import PySRRegressor

model = PySRRegressor(
    maxsize=20,
    niterations=40,  # < Increase me for better results
    binary_operators=["+", "*"],
    unary_operators=[
        "cos",
        "exp",
        "sin",
        "inv(x) = 1/x",
        # ^ Custom operator (julia syntax)
    ],
    extra_sympy_mappings={"inv": lambda x: 1 / x},
    # ^ Define operator for SymPy as well
    elementwise_loss="loss(prediction, target) = (prediction - target)^2",
    # ^ Custom loss function (julia syntax)
)

model.fit(X, y)


# model = PySRRegressor.from_file("hall_of_fame.2022-08-10_100832.281.pkl")

print(model)
