from collections import namedtuple
from tabulate import tabulate
from data import fund_constants
from aggregate import currencies, shares_total
from currency_info import get_price

def composition_summary(fund, date=None):
    amounts = currencies(date)[fund]
    amounts_eur = {}

    for ticker, amount in amounts.items():
        #print(ticker, date, get_price(ticker, date))
        amounts_eur[ticker] = amount * get_price(ticker, date)
    total_eur = sum(amounts_eur.values())

    rows = []
    Cell = namedtuple('Cell', ['id', 'name', 'value'])
    for ticker in amounts:
        rows.append((
            Cell('ticker', 'Ticker', ticker),
            Cell('quantity', 'Quantity', amounts[ticker]),
            Cell('price', 'Price [€]', get_price(ticker, date)),
            Cell('eur_value', 'Value [€]', amounts_eur[ticker]),
            Cell('percent', 'Percent', amounts_eur[ticker] / total_eur * 100), # percentage of total fund value
        ))
    # sort descendingly by eur_value
    rows.sort(key=lambda row: [c.value for c in row if c.id == 'eur_value'][0], reverse=True)

    return rows, total_eur

def total_value(fund, date=None):
    fund_summary, total = composition_summary(fund, date)
    return total

def share_price(fund, date=None):
    return total_value(fund, date) / shares_total(date)[fund]

def tabulate_selection(fund_summary, selection=None):
    if not fund_summary:
        return ''

    row = fund_summary[0]

    if selection == None:
        selection = [cell.id for cell in row]

    headers = [cell.name for cell in row if cell.id in selection]

    selected = []
    for row in fund_summary:
        selected.append([cell.value for cell in row if cell.id in selection])
    return tabulate(selected, headers)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--date', dest='date', default=None)
    args = parser.parse_args()
    date = args.date

    for fund in fund_constants.__all__:
        fund_summary, total = composition_summary(fund, date)

        print()
        print('Fund: %s' % fund)
        print(tabulate_selection(fund_summary))
        print()
        print('Total value [€]: %.3f' % total)
        print('Price per share [€]: %.3f' % share_price(fund, date))
        print()
