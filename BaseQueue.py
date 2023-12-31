# BaseQueue.py
import math
import numbers


class BaseQueue:
    """
    BaseQueue is a class for queueing theory and modeling with common
    properties and methods

    Key Attributes:
        lamda (float or tuple): is the arrival rate or a list of arrival rates for specified queue
        mu (float): is the service rate for the queue
    """
    def __init__(self, lamda, mu):
        """
        Initializes BaseQueue with lamda and mu

        Arguments:
            lamda (float or tuple): arrival rate or list of arrival rates
            mu (float): service rate for the queue
        """
        self.lamda = lamda
        self.mu = mu
        self._lq = None
        self._p0 = None
        self._recalc_needed = True

    @property
    def lamda(self):
        """
        Getter for lamda (arrival rate) property.

        :return:
            float or tuple: the arrival rate of a list of arrival rates
        """
        return self._lamda

    @lamda.setter
    def lamda(self, lamda):
        """
        Setter for lamda property. Only allows for valid values.

        Arguments:
            lamda (float or tuple): the arrival rate or a list of arrival rates
        """
        self._lamda = self._simplify_lamda(lamda)

        self._recalc_needed = True

    @property
    def mu(self):
        """
        Getter for mu (service rate) property.

        :return:
            float: service rate
        """
        return self._mu

    @mu.setter
    def mu(self, mu):
        """
        Setter for mu (service rate) property. Only allows for valid values.

        Arguments:
            mu (float): service rate
        """
        if isinstance(mu, numbers.Number) and mu > 0:
            self._mu = mu
        else:
            self._mu = math.nan

        self._recalc_needed = True

    def _calc_metrics(self):
        """
        Calculate and update our queueing metrics (Lq and p0)
        """
        self._lq = math.nan
        self._p0 = math.nan
        self._recalc_needed = False

    @property
    def p0(self):
        """
        Getter for p0 (probability of an empty queue)

        :return:
            float: p0
        """
        if self._recalc_needed:
            self._calc_metrics()
        return self._p0

    @property
    def lq(self):
        """
        Getter for Lq (average customers in the queue)

        :return:
            float: Lq
        """
        if self._recalc_needed:
            self._calc_metrics()
        return self._lq

    @property
    def l(self):
        """
        Getter for L (average number of customers in the system)

        :return:
            float: L
        """
        return self.lq + self.r

    @property
    def r(self):
        """
        Getter for R (average time a customer spends in the system)

        :return:
            float: R
        """
        return self.lamda / self.mu

    @property
    def ro(self):
        """
        Getter for ro (the utilization)

        :return:
            float: ro
        """
        return self.r

    @property
    def w(self):
        """
        Getter for W (average time a customer spends in the queue)

        :return:
            float: W
        """
        return self.wq + (1 / self.mu)

    @property
    def wq(self):
        """
        Getter for Wq (average time a customers waits in the queue)

        :return:
            float: Wq
        """
        return self.lq / self.lamda

    @property
    def utilization(self):
        """
        Getter for ro

        :return:
            float: ro
        """
        return self.ro

    def is_valid(self):
        """
        Check if the queueing parameters (lamda and mu) are valid.

        :return:
            True if parameters are valid and False if not
        """
        if math.isnan(self.lamda) or math.isnan(self.mu):
            return False

        return True

    def is_feasible(self):
        """
        Check if the queueing parameters (lamda and mu) are feasible

        :return:
            boolean: True if parameters are feasible and False if not
        """
        try:
            lamda = float(self.lamda)
            mu = float(self.mu)
        except ValueError:
            return False
        if mu == 0:
            return False
        return self.ro < 1

    def _simplify_lamda(self, lamda) -> numbers.Number:
        """
        Simplify the arrival rate (lamda) to a single value or tuple value

        Arguments:
            lamda (float or tuple): arrival rate or list of arrival rates
        :return:
            float: a simplified lamda
        """
        if isinstance(lamda, tuple):
            # validate every element of lamda, if all valid then return the sum of lamda
            if all([isinstance(l, numbers.Number) and l > 0 for l in lamda]):
                return sum(lamda)
            else:
                return math.nan
        else:
            # validate single value lamda, if valid return lamda
            if isinstance(lamda, numbers.Number) and lamda > 0:
                return lamda
            else:
                return math.nan

    def __str__(self):
        """
        String representation for the BaseQueue

        :return:
            a string representation with key properties
        """
        return (f"{type(self).__name__} instance"
                f"lamda: {self.lamda}, mu: {self.mu},"
                f"Lq: {self.lq}, P0: {self.p0}")