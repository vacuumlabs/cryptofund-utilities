import dateutil.parser
from data import trades as trades_raw
from data import owners, owners as o
from data import currency_constants, currency_constants as c
from data import fund_constants, fund_constants as f
from data import operations

add = operations.add
remove = operations.remove
add_shares = operations.add_shares
remove_shares = operations.remove_shares

def process_trades_raw(trades_raw):
    """
    Validate action data and output them as a list of tuples (date, fund,
    operation, ...operation_args)
    Input is expected to be a list of tuples in form
    (date, fund, op1, ...op1_args, op2, ...op2_args, ...)
    """

    result = []

    for d in trades_raw:
        it = iter(d)

        date = dateutil.parser.parse(next(it))

        fund = next(it)

        if fund not in fund_constants.__all__:
            raise Exception('Unknown fund %s in action record' % fund)

        while True:
            try:
                operation = next(it)
            except StopIteration:
                break
            if operation not in operations.__all__:
                raise Exception('Unknown operation %s in action record' % operation)
            if operation in [add, remove]:
                ticker, quantity = next(it), next(it)
                if ticker not in currency_constants.__all__:
                    raise Exception('Unknown ticker %s in action record' % ticker)
                result.append((date, fund, operation, ticker, quantity))
            if operation in [add_shares, remove_shares]:
                owner, quantity = next(it), next(it)
                if owner not in owners.__all__:
                    raise Exception('Unknown owner %s in action record' % owner)
                result.append((date, fund, operation, owner, quantity))

    return result

trades = process_trades_raw(trades_raw)

def aggregate(trades, date=None):
    """
    Return tuple (currency_amounts, share_counts) as of date `date` (or as of
    now if date == None).

    Input:
    trades  [(date, fund, operation, ...operation_args)]
    date        datetime or string

    Output:
    currencies  Currency amounts present in the fund at the given date
                {fund: {ticker: quantity}}
    shares      Shares in the fund held by each owner at the given date
                {fund: {owner: quantity}}
    """

    if type(date) == str:
        date = dateutil.parser.parse(date)

    currencies = {}
    shares = {}

    for fund in f.__all__:
        currencies[fund] = {k: 0 for k in c.__all__}
        shares[fund] = {k: 0 for k in o.__all__}

    for action in trades:
        action_date, fund, operation = action[:3]
        args = action[3:]

        if date != None and date < action_date:
            continue

        if operation == operations.add:
            ticker, quantity = args
            currencies[fund][ticker] += quantity
        elif operation == operations.remove:
            ticker, quantity = args
            currencies[fund][ticker] -= quantity
        elif operation == operations.add_shares:
            owner, quantity = args
            shares[fund][owner] += quantity
        elif operation == operations.remove_shares:
            owner, quantity = args
            shares[fund][owner] -= quantity
        else:
            raise Exception('Unknown operation %s in action record' % operation)

    def prune(data):
        for k in list(data.keys()):
            if data[k] == 0:
                del data[k]

    for fund in f.__all__:
        prune(currencies[fund])
        prune(shares[fund])

    return currencies, shares


def currencies(date=None):
    c, s = aggregate(trades, date)
    return c

def shares(date=None):
    c, s = aggregate(trades, date)
    return s

def shares_total(date=None):
    s = shares(date)
    return {fund: sum(s[fund].values()) for fund in f.__all__}

if __name__ == '__main__':
    print('Currencies:\n%s' % currencies())
    print('Shares:\n%s' % shares())
    print('Total shares:\n%s' % shares_total())
