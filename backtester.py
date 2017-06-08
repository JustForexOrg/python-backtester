from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import http.client

API_BASE_URL = 'justforex.xyz:3020'
step = timedelta(seconds=3600)  # hour step
conn = http.client.HTTPConnection(API_BASE_URL)


def format_datetime_string(dt):
    return dt.isoformat()


def get_price(target_curr, base_curr, time):
    prices = {
        'GBP': 50.0,
        'EUR': 37.0,
        'JPY': 1.0,
        'USD': 31.0,
        'CHF': 0.5,
        }
    return prices[target_curr] / prices[base_curr]


def get_prices_in_period(
    target_curr,
    base_curr,
    now,
    period_length,
    ):
    start_of_period = now - period_length
    prices = []
    dt = start_of_period
    while dt - start_of_period < period_length:
        prices.append(get_price(target_curr, base_curr, dt))
        dt += step
    return prices


def get_economic_indicator(indicatorType, indicator, time):
    http_request_str = '/userapi-backend/economicIndicator/' \
        + indicatorType + '?'
    http_request_str += 'indicator=' + indicator
    http_request_str += '&time=' + format_datetime_string(time)
    conn.request('GET', http_request_str)
    resp = conn.getresponse()
    data = resp.read()
    return data


def get_economic_indicators_in_period(
    indicatorType,
    indicator,
    now,
    period_length,
    ):
    start_of_period = now - period_length
    values = []
    dt = start_of_period
    while dt - start_of_period < period_length:
        values.append(get_economic_indicator(indicatorType, indicator,
                      dt))
        dt += step
    return values


class Algorithm(ABC):

    def __init__(self, start_datetime, end_datetime):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.current_time = self.start_datetime

    # Wallet of different currencies - all start off at 1000 US Dollars

        self.wallet = {
            'USD': 1000.0,
            'GBP': 0,
            'EUR': 0,
            'CHF': 0,
            'JPY': 0,
            }

    # List of transactions - (is_buy, target_curr, base_curr, volume, time, wallet state after)

        self.successful_transactions = []

    # List of transactions - (is_buy, target_curr, base_curr, volume, time, deficit in base_curr)

        self.unsuccessful_transactions = []

    def wallet_state(self):
        return list(self.wallet.values())

    def get_price_period_high(
        self,
        target_curr,
        base_curr,
        period_length,
        ):
        return max(get_prices_in_period(target_curr, base_curr,
                   self.current_time, period_length))

    def get_price_period_low(
        self,
        target_curr,
        base_curr,
        period_length,
        ):
        return min(get_prices_in_period(target_curr, base_curr,
                   self.current_time, period_length))

    @abstractmethod
    def act(self):
        pass

    def run(self):
        while self.current_time < self.end_datetime:
            self.act()
            self.current_time += step

    def get_time(self):
        return self.current_time

    def get_inventory(self):
        return self.wallet

  # buy target_curr_volume worth of target_curr using base_curr

    def buy(
        self,
        target_curr,
        base_curr,
        target_curr_volume,
        ):
        exchange_rate = get_price(target_curr, base_curr,
                                  self.current_time)
        price_in_base_curr = target_curr_volume * exchange_rate
        if price_in_base_curr > self.wallet[base_curr]:
            deficit = price_in_base_curr - self.wallet[base_curr]
            self.unsuccessful_transactions.append([
                True,
                target_curr,
                base_curr,
                target_curr_volume,
                self.current_time,
                deficit,
                ])
            return
        self.wallet[base_curr] -= price_in_base_curr
        self.wallet[target_curr] += target_curr_volume
        self.successful_transactions.append([
            True,
            target_curr,
            base_curr,
            target_curr_volume,
            self.current_time,
            self.wallet_state(),
            ])

  # sell base_curr_volume worth of base_curr for target_curr

    def sell(
        self,
        base_curr,
        target_curr,
        base_curr_volume,
        ):
        if base_curr_volume > self.wallet[base_curr]:
            deficit = base_curr_volume - self.wallet[base_curr]
            self.unsuccessful_transactions.append([
                False,
                target_curr,
                base_curr,
                base_curr_volume,
                self.current_time,
                deficit,
                ])
            return
        exchange_rate = get_price(base_curr, target_curr,
                                  self.current_time)
        amount_in_target_curr = base_curr_volume * exchange_rate
        self.wallet[base_curr] -= base_curr_volume
        self.wallet[target_curr] += amount_in_target_curr
        self.successful_transactions.append([
            False,
            target_curr,
            base_curr,
            base_curr_volume,
            self.current_time,
            self.wallet_state(),
            ])


class MyAlgorithm(Algorithm):

    def __init__(self, start_datetime, end_datetime):
        super().__init__(start_datetime, end_datetime)

    def act(self):
        if self.counter % 100 == 0:
            self.buy('GBP', 'USD', 1)
            self.sell('GBP', 'EUR', 0.9)


dummystart = datetime(
    2012,
    4,
    5,
    21,
    4,
    9,
    )
dummyend = datetime(
    2013,
    1,
    30,
    1,
    33,
    22,
    )
ma = MyAlgorithm(dummystart, dummyend)
ma.run()
print 'Successful: '
for a in ma.successful_transactions:
    print a
print ('Number of transactions: ', len(ma.successful_transactions))
print ('Unsuccessful: ', ma.unsuccessful_transactions)
conn.close()

# 2007-12-03T10:15:30
