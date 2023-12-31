import math

from BaseQueue import BaseQueue

class MM1Queue(BaseQueue):
    """
    MM1Queue is a class for finding the metrics of a queue that follows the M/M/1 model. The arrival time is Poisson,
    the service time is exponential, and it only has 1 server.
    """
    def _calc_metrics(self):
        """
        Used to calculate and update metrics (p0 and lq)
        """
        if self.lamda <= 0 or self.mu <= 0:
            """
            Checks the validity of lamda and mu as inputs. If valid, calculates p0.
            """
            self._lq = math.nan
            self._l = math.nan
            self._wq = math.nan
            self._w = math.nan
            self._p0 = math.nan
        else:
            self._p0 = 1 - self.ro
            if self.ro == 1:
                """
                Checks the feasibility of ro. If feasible, calculates the rest of the metrics associated with 
                an MM1 Queue.
                """
                self._lq = math.inf
                self._l = math.inf
                self._wq = math.inf
                self._w = math.inf
                self._p0 = math.inf
            else:
                self._lq = (self.lamda**2) / (self.mu * (self.mu - self.lamda))
                self._l = self.lamda / (self.mu - self.lamda)
                self._wq = self._lq / self.lamda
                self._w = self._l / self.lamda

