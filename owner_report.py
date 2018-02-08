from data import fund_constants as f, owners
from aggregate import shares, shares_total
from composition_summary import total_value

def owner_report(fund, date):
    s = shares(date)
    st = shares_total(date)

    def owner_value(owner, fund):
        num_shares = s[fund][owner] if owner in s[fund] else 0
        return num_shares, total_value(fund, date) * num_shares / (st[fund] if st[fund] > 0 else 1)

    result = []
    for owner in owners.__all__:
        sgen, gen = owner_value(owner, fund)
        result.append((owner, sgen, gen))
    result.sort(key=lambda r: r[-1], reverse = True)
    return result

f.__all__


from tabulate import tabulate

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', dest='date', default=None)
    args = parser.parse_args()
    date = args.date
    for fund in f.__all__:
        headers = [
            'Owner',
            '%s [pc]' % fund,
            '%s [€]' % fund,
        ]
        print()
        print(tabulate(owner_report(fund, date), headers=headers))
        print()
