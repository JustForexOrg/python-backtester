from .algorithm import Algorithm

class MyAlgorithm(Algorithm):

    def __init__(self, start_datetime, end_datetime):
        super().__init__(start_datetime, end_datetime)
        self.counter = 0

    def act(self):
        if self.counter == 0:
            print('The user\'s file was not sent)
        self.counter == 1
