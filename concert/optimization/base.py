"""
Optimization is a procedure to iteratively find the best possible match
to

.. math::
    y = f(x).

This module provides base classes for optimizer implementations.
"""

from concert.processes.base import Process
from concert.asynchronous import async, dispatcher
import logbook
from concert.base import LimitError


class Optimizer(Process):

    """The most abstract optimizer."""
    FINISHED = "optimization-finished"

    def __init__(self, function):
        """
        Create an optimizer for a *function*.
        """
        super(Optimizer, self).__init__(None)
        self.data = []
        self.function = function
        self._logger = logbook.Logger(__name__ + "." + self.__class__.__name__)

    def evaluate(self, x):
        """Execute y = f(*x*), save (x, y) pair and return y."""
        y = self.function(x)
        self.data.append((x, y))

        return y

    def _optimize(self):
        """Optimization executive code."""
        raise NotImplementedError

    @async
    def run(self):
        """
        run()

        Run the optimizer.
        """
        # Clear the saved values.
        self.data = []

        self._optimize()

        dispatcher.send(self, self.FINISHED)
        self._logger.debug("Optimization finished with x = {0}, y = {1}".
                           format(self.data[0][-1], self.data[1][-1]))

        return tuple(self.data)


class ParameterOptimizer(Optimizer):

    """
    An optimizer based on a :py:class:`.Parameter` and a callable feedback.
    The function to optimize is created as ::

        def function(x):
            param.set(x).wait()
            return feedback()
    """

    def __init__(self, param, feedback):
        """Create an optimizer for parameter *param* and *feedback*."""
        self.param = param
        self.feedback = feedback

        def function(x):
            try:
                self.param.set(x).wait()
            except LimitError:
                pass

            return self.feedback()

        super(ParameterOptimizer, self).__init__(function)
