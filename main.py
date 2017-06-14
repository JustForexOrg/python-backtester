from datetime import datetime, timedelta
from btlib.myalgorithm import MyAlgorithm

DEFAULT_START_TIME = datetime(
    2012,
    4,
    5,
    21,
    4,
    9,
    )
DEFAULT_END_TIME = datetime(
    2013,
    1,
    30,
    1,
    33,
    22,
    )
ma = MyAlgorithm(DEFAULT_START_TIME, DEFAULT_END_TIME)


def backtest_algorithm():
    ma.run()
    return ma.wallet_value_usd_list
    #print('Successful: ')
    #for a in ma.successful_transactions:
    #    print(a)
    #print ('Number of transactions: ', len(ma.successful_transactions))
    #print ('Unsuccessful: ', ma.unsuccessful_transactions)
