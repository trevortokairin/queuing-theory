import math
from BaseQueue import BaseQueue

class MD1Queue(BaseQueue):
    """
    Represents an M/D/1 queue, which is a queueing system with a Poisson arrival rate (lamda),
    deterministic service time, and a single server.

    Methods:
        - _calc_metrics: Calculate queueing metrics Lq (average number of customers in the queue) and
          P0 (probability of an empty system).

    Attributes (inherited from BaseQueue):
        - lamda: Arrival rate (Poisson process parameter).
        - mu: Service rate (average service time).
    """

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
            self._lq = 0.5 * (self.lamda / self.mu) ** 2 / (1 - self.ro)

        self._recalc_needed = False

