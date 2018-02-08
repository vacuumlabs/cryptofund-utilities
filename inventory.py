from tabulate import tabulate
from data import currency_constants as c
from aggregate import currencies

def totals(inventory):
    locations = sorted(list(inventory.keys()))
    headers = ['Currency', 'Total (want)', 'Total (have)'] + locations
    data = []
    currencies_by_funds = currencies()
    for cc in c.__all__:
        row = [inventory[l][cc] if cc in inventory[l] else 0 for l in locations]
        total_want = sum(f[cc] if cc in f else 0 for f in currencies_by_funds.values())
        data.append([cc, total_want, sum(row)] + row)
    return tabulate(data, headers)

inventory_2018_01_01 = {
    'Kraken': {
        c.BTC: 0.5,
        c.ETH: 20,
        c.XLM: 10000,
        c.ADA: 8775,
     }
    # Typically, more source of coins follow
}

print(totals(inventory_2018_01_01))
