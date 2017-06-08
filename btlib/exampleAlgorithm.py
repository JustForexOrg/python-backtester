from .algorithm import Algorithm

class MyAlgorithm(Algorithm):

    def __init__(self, start_datetime, end_datetime):
        super().__init__(start_datetime, end_datetime)
        self.counter = 0

    def act(self):
        if self.counter % 100 == 0:
            self.buy('GBP', 'USD', 1)
            self.sell('GBP', 'EUR', 0.9)
        self.counter += 1
