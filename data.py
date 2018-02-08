from create_enum import create_enum

f = fund_constants = create_enum('ABCT')

c = currency_constants = create_enum('BTC', 'ETH', 'XLM', 'ADA')

operations = create_enum('add', 'remove', 'add_shares', 'remove_shares')

add = operations.add
remove = operations.remove
add_shares = operations.add_shares
remove_shares = operations.remove_shares

o = owners = create_enum(
  'Alice',
  'Bob',
  'Cecil',
)

trades = [
    ('2018-01-01', f.ABCT,
        add_shares, o.Alice, 15000,
        add_shares, o.Bob, 15000,
        add, c.BTC, 1,
        add, c.ETH, 10,
        add, c.XLM, 10000),

    ('2018-01-07', f.ABCT,
        add_shares, o.Cecil, 9293,
        add, c.ETH, 10),

    ('2018-01-14', f.ABCT,
        remove, c.BTC, 0.5,
        add, c.ADA, 8775)
]

