from .algorithm import Algorithm

class MyAlgorithm(Algorithm):

    def __init__(self, start_datetime, end_datetime):
        # Change the start_datetime and end_datetime to run test over
        # a custom period
        super().__init__(start_datetime, end_datetime)
        self.counter = 0

    def act(self):
        # Add your main algorithm code here
        pass
