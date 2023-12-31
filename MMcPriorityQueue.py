import math
import numbers
from MMcQueue import MMcQueue

class MMcPriorityQueue(MMcQueue):
    """
    Represents an M/M/c priority queue system.
    This class calls the MMcQueue class and allows for multiple priority levels.
    """

    def __init__(self, lamda, mu, c=1):
        """
        Initialize the MMcPriorityQueue.

        Args:
            lamda: Arrival rate or tuple of arrival rates for different priority levels.
            mu: Service rate.
            c: Number of servers
        """
        super().__init__(lamda, mu, c)
        self.lamda_k = lamda

    @property
    def lamda_k(self):
        """
        Get the arrival rates for different priority levels.

        Returns:
            float or tuple: Arrival rate or tuple of arrival rates.
        """
        return self._lamda_k

    @MMcQueue.lamda.setter
    def lamda(self, lamda):
        """
        Set the overall arrival rate for the system.

        Args:
            lamda (float or tuple): Arrival rate or tuple of arrival rates for different priority levels.
        """
        # Validate lamda and store aggregate value
        self._lamda = self._simplify_lamda(lamda)

        # Also save lamda tuple here
        self._lamda_k = lamda

    @lamda_k.setter
    def lamda_k(self, lamda_k):
        """
        Set the arrival rate for different priority levels.

        Args:
            lamda_k: Arrival rate or tuple of arrival rates for different priority levels.
        """
        if not isinstance(lamda_k, (list, tuple)):
            lamda_k = (lamda_k,)  # Make it a tuple

        if all(isinstance(l, numbers.Number) and l > 0 for l in lamda_k):
            self._lamda_k = lamda_k
        else:
            self._lamda_k = (math.nan,)

    def get_lamda_k(self, k=None):
        """
        Get the arrival rate for a specific priority level.

        Args:
            k: Priority level. Default is None for the overall arrival rate.

        Returns:
            float: Arrival rate for the specified priority level.
        """
        if k is None:
            return self.lamda
        elif 0 < k <= len(self._lamda_k):
            return self._lamda_k[k - 1]
        else:
            return math.nan

    def get_lq_k(self, k):
        """
        Get the number of customers in the queue for a specific priority level.

        Args:
            k: Priority level.

        Returns:
            float: Number of customers in the queue for the specified priority level.
        """
        if not self.is_valid():
            return math.nan

        lqk = self.lamda_k[k - 1] * self.get_wq_k(k)
        return lqk

    def get_l_k(self, k):
        """
        Get the number of customers in the system for a specific priority level.

        Args:
            k: Priority level.

        Returns:
            float: Number of customers in the system for the specified priority level.
        """
        lq_k = self.get_lq_k(k)
        if math.isnan(lq_k):
            return math.nan

        lamda_k = self.get_lamda_k(k)
        if lamda_k == 0:
            return math.nan

        return lq_k + lamda_k / self.mu

    def get_b_k(self, k):
        """
        Get the utilization factor for a specific priority level.

        Args:
            k: Priority level.

        Returns:
            float: Utilization factor for the specified priority level.
        """
        if k < 0 or k > len(self._lamda_k):
            return math.nan

        if self.lamda == self.mu:
            return math.inf

        if k == 0:
            return 1

        ro_k = self.get_ro_k(k)

        if ro_k > 1:
            return math.inf

        b_k = 1 - ro_k
        return b_k

    def get_ro_k(self, k):
        """
        Get the traffic intensity for a specific priority level.

        Args:
            k: Priority level.

        Returns:
            float: Traffic intensity for the specified priority level.
        """
        lamda_k = sum(self.get_lamda_k(k) for k in range(1, k + 1))
        return lamda_k / (self.c * self.mu)

    def get_w_k(self, k):
        """
        Get the time a customer spends in the system for a specific priority level.

        Args:
            k: Priority level.

        Returns:
            float: Time a customer spends in the system for the specified priority level.
        """
        if self.lamda == self.mu:
            return math.inf

        l_k = self.get_l_k(k)
        if math.isnan(l_k):
            return math.nan

        lamda_k = self.get_lamda_k(k)
        if lamda_k == 0:
            return math.nan

        return l_k / lamda_k

    def get_wq_k(self, k):
        """
        Get the time a customer spends waiting in the queue for a specific priority level.

        Args:
            k: Priority level.

        Returns:
            float: Time a customer spends waiting in the queue for the specified priority level.
        """
        if self.lamda == self.mu:
            return math.inf

        wqk = (1 - self.ro) * self.wq / (self.get_b_k(k) * self.get_b_k(k-1))
        return wqk
