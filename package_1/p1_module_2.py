import numpy as np
from numpy.typing import NDArray


class ArrayMathematics:
    """ A class that perform basic array operations.
    """
    @staticmethod
    def addition(x: NDArray, y: NDArray) -> NDArray:
        """ A method for adding two integers together.

        Args:
             x (NDArray): The first integer.
             y (NDArray): The second integer.

        Returns:
            NDArray: The sum of the two integers.
        """
        x = np.array(x)
        y = np.array(y)
        return x + y

    @staticmethod
    def subtraction(x: NDArray, y: NDArray) -> NDArray:
        """ A method for subtracting two integers.

        Args:
            x (NDArray): The first integer.
            y (NDArray): The second integer.

        Returns:
            NDArray: The difference of the two integers.
        """
        x = np.array(x)
        y = np.array(y)
        return x - y

    @staticmethod
    def multiplication(x: NDArray, y: NDArray) -> NDArray:
        """ A method for multiplying two integers.

        Args:
            x (NDArray): The first integer.
            y (NDArray): The second integer.

        Returns:
            NDArray: The product of the two integers.
        """
        x = np.array(x)
        y = np.array(y)
        return x * y

    @staticmethod
    def division(x: NDArray, y: NDArray) -> NDArray:
        """ A method for dividing two integers.

        Args:
            x (NDArray): The first integer.
            y (NDArray): The second integer.

        Returns:
            NDArray: The quotient of the two integers.
        """
        x = np.array(x)
        y = np.array(y)
        return x / y
