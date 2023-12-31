import math

from BaseQueue import BaseQueue


class MMcQueue(BaseQueue):
    def __init__(self, lamda, mu, c=1):
        super().__init__(lamda, mu)
        self.c = c
        self.ro = self.r

    """
    MMcQueue is a class for finding the metrics of a queue that follows an MMC model. This means that the arrival 
    rates follow a poisson distribution, the service rates follow an exponential distribution, and it can accept 
    multiple servers.
    """

    @property
    def c(self) -> int:
        return self._c

    """
    Getter for c (# of servers) property.

    :return:
    int: the # of servers for an MMC Queue
    """

    @c.setter
    def c(self, c):
        if c <= 0:
            self._c = math.nan
        else:
            self._c = c
        self._recalc_needed = True

    """
    Setter for c property. Only allows for valid values.

    Arguments:
        c (int): the number of servers in a queue
    """

    @property
    def ro(self):
        return self._ro

    """
    Getter for ro property.

    :return:
        ro: the utilization of the system found between the arrival rate and service rate
    """

    @ro.setter
    def ro(self, r):
        if self.c > 1:
            self._ro = self.lamda / (self.mu * self.c)
        else:
            self._ro = r
        self._recalc_needed = True
        """
        Setter for ro property. 

        Arguments:
            ro (float): the utilization of the system 
        """

    def _calc_metrics(self):
        """
        Used to calculate and update metrics (p0 and lq) for a multi-server queue
        """
        if not self.is_valid():
            self._lq = math.nan
            self._p0 = math.nan
            self._recalc_needed = False

            return None
        #Determine the validity of the function

        elif not self.is_feasible():
            self._lq = math.inf
            self._p0 = math.inf

            self._recalc_needed = False

            return None
        #Determines the feasibility of the function

        if self.c > 1:
            term1 = 0
            for n in range(self.c):
                term1 = term1 + self.r ** n / math.factorial(n)
                term2 = self.r ** self.c / (math.factorial(self.c) * (1 - self.ro))
                self._p0 = 1 / (term1 + term2)

            num = self.r ** self.c * self.ro
            den = (math.factorial(self.c) * (1 - self.ro) ** 2)
            self._lq = self._p0 * (num / den)
            #Determines if the Queue has multiple servers. If yes, it calculates Lq and P0 in the way shown above

        elif self.c == 1:
            self._lq = (self.lamda ** 2) / (self.mu * (self.mu - self.lamda))
            self._p0 = 1 - self.ro
        #If its a single server queue, then it calculates Lq and P0 in this way shown above

        self._recalc_needed = False
