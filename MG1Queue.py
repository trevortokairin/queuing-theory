import math
from BaseQueue import BaseQueue

class MG1Queue(BaseQueue):
    """
    Represents an M/G/1 queue, which is a queueing system with a Poisson arrival rate (lamda),
    general service time distribution, and a single server.

    Args:
        lamda: Arrival rate
        mu: Service rate
        sigma_s: Standard deviation of the service time distribution.

    Methods:
        - __str__: Return a string representation of the M/G/1 queue.
        - is_valid: Check if the input parameters are valid for queue calculation.

    """

    def __init__(self, lamda, mu, sigma_s=0.0):
        super().__init__(lamda, mu)
        self.sigma_s = sigma_s

    def __str__(self):
        """
        Return a string representation of the M/G/1 queue.

        Returns:
            str: A formatted string with queue information.
        """
        return (f"{type(self).__name__} instance"
                f"lamda: {self.lamda}, mu: {self.mu},"
                f"Lq: {self.lq}, P0: {self.p0}")

    @property
    def sigma_s(self):
        """
        Get the standard deviation of the service time distribution.

        Returns:
            float: Standard deviation of the service time distribution.
        """
        return self._sigma_s

    @sigma_s.setter
    def sigma_s(self, sigma_s):
        """
        Set the standard deviation of the service time distribution.

        Args:
            sigma_s: Standard deviation of the service time distribution.
        """
        try:
            sigma_s = float(sigma_s)
        except ValueError:
            sigma_s = math.nan

        if sigma_s >= 0:
            self._sigma_s = sigma_s
            self._recalc_needed = True
        else:
            self._sigma_s = math.nan
            self._recalc_needed = True

    def _calc_metrics(self):
        """
        Calculate queueing metrics Lq (average number of customers in the queue) and P0 (probability of an empty system).
        """
        if not self.is_valid():
            self._lq = math.nan
            self._p0 = math.nan
        elif not self.is_feasible():
            self._lq = math.inf
            self._p0 = math.inf
        else:
            self._p0 = 1 - self.ro
            self._lq = (self.ro ** 2 + self.lamda ** 2 * self.sigma_s ** 2) / (2 * (1 - self.ro))
        self._recalc_needed = False

    def is_valid(self):
        """
        Check if the input parameters are valid for queue calculation.

        Returns:
            bool: True if the parameters are valid; False if any of them is NaN.
        """
        if math.isnan(self.lamda) or math.isnan(self.mu) or math.isnan(self.sigma_s):
            return False
        return True


