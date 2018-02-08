import math
from data import currency_constants as c, fund_constants as f
from composition_summary import share_price
from currency_info import get_price

# Helper used to calculate number of shares for owner who deposits some currency
# to the fund
def print_payment_to_shares_calculation(date, fund, payment):
    sp = share_price(fund, date)
    eur_value = 0
    for ticker, amount in payment.items():
        eur_value += amount * get_price(ticker, date)
    result = math.floor(eur_value / sp)
    print('Date:        %s' % date)
    print('Deposited:   %s' % ', '.join('%s %s' % (a, t) for t, a in payment.items()))
    print('Eur value:   %s' % eur_value)
    print('Share price: %s' % sp)
    print('Shares:      %s' % result)

if __name__ == '__main__':

    print_payment_to_shares_calculation(
            '2018-01-07',
            f.ABCT,
            {c.ETH: 10})
