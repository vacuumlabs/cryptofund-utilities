# Do your own crypto-investment-fund

With all the world becoming obsessed by cryptocurrencies, we've noticed that quite often people
invest on behalf of others - their families and close friends. For such purpose, one clearly needs
good accounting tools - Excel is far too error prone to do this right.

The aim of this project is to give you a set of accounting utilities you can use to run your own mini
cryptocurrency investment fund. We'll help you:

- keeping track of who owns what
- monitoring your portfolio (share price over time)
- issuing / destroying shares of the fund
- auditing (do we really own what we claim we do?)

This project is not:
- new coin
- wallet, where you can store your coins
- trading software, that would trade on your behalf

## Installation
[Quick guide](https://github.com/vacuumlabs/cryptofund-utilities/blob/master/install.md)

## Getting started

Alice and Bob are crypto fans, who spend a lot of time researching crypto-space and occasionally buy
some new hot stuff and occasionally cash out a little. Since they want to bring their families and
close friends to the business, they setup their own fund which they name ABCT (Alice and Bob's
Crypto Trust) (Bob wanted to name it 'Shitcoin Buffet', but Alice refused). To do this, they
allocate some assets to their portfolio:

```
1 BTC
10 ETH
10000 XLM
```

This portfolio should be stored on some exchange or hardware wallet - this repo is an accounting tool,
not a wallet. Such portfolio is worth (as of 2018-01-01) approximately 21637 EUR. A&B decide, that
they emit 30,000 shares, each of which is worth approx. 0.721 EUR.

Shares are the key concept for the fund: at any given time, one share represents one n-th of the current
portfolio value (in this case, one share represents 1/30,000 of the portfolio value). If the
portfolio cryptocurrencies do well and they get more valuable, the share price rises (and vice
versa). If (new) people make new investments, the portfolio value also increases - however in such a
case, also new shares must be emitted for these investments. New investment should not change share
price - we'll get to this later. Note that the number of shares A&B emitted at the beginning is
arbitrary. They could for example emit 100,000 shares each worth approx 0.216 EUR or 1,000,000
shares each worth 0.0216 EUR.

The fund initial state is put to `data.py`:

```
trades = [
    ('2018-01-01', f.ABCT,
        add_shares, o.Alice, 15000,
        add_shares, o.Bob, 15000,
        add, c.BTC, 1,
        add, c.ETH, 10,
        add, c.XLM, 10000),
]
```

Putting such data as a Python structure has several advantages for A&B:
- they can do code-review on (say) Github
- system keeps its history because of Git (thank you, Torvalds!)
- data are validated. If Alice types XLN instead of XLM she sees a nice error
- if one day Alice decides that she wants some additional feature, she can process such data MUCH
  faster compared to (say) excel.

Once the fund is set up, Alice can run:

```
python composition_summary.py
```

To get the general fund stats:

```
Fund: ABCT
Ticker      Quantity    Price [€]    Value [€]    Percent
--------  ----------  -----------  -----------  ---------
BTC                1   11424           11424      52.8829
ETH               10     638.14         6381.4    29.5403
XLM            10000       0.3797       3797      17.5768

Total value [€]: 21602.360
Price per share [€]: 0.720
```

and

```
python owners_report.py
```

To get information about how wealthy individual investors are:
```
Owner      ABCT [pc]    ABCT [€]
-------  -----------  ----------
Alice          15000     10818.7
Bob            15000     10818.7
```

Note: these commands print reports for the current date. For any other date, you can include it as a parameter:

```
python owner_report.py --date=2018-01-01
python composition_summary.py --date=2018-01-01
```

Finally, Alice and Bob can send a daily report to all investors:

```
python inform_slack.py
```

This generates the report and sends it to a specific Slack channel. Ideally, Alice should deploy
this somewhere and setup cronjob to run this on a daily basis (Investors shouldn't be exposed to more frequent
share-price updates. It corrupts one's mind.)

## Cecil wants to enter the fund

With such a great portfolio, who wouldn't! Cecil decides he'll contribute his 10 ETH (we discuss EUR
contributions later) - Cecil simply sends the ETH to the publicly announced fund's ETH address. In
that very moment, he enters the fund buying shares at the current share price. This is done so,
although actual accounting may happen later in time; we'll get to that later.

At the point of Cecil's investment, we have to emit new shares that'll get into his possession. Note
that we want Alice & Bob to be exactly as rich after Cecil's trade as before it. This means, we
don't want to change their number of shares, neither we want to change the share price. Since by
Cecil's contribution portfolio is 10 ETH bigger, we have to emit new shares - so that the final
share price stays the same. The new shares which are being emitted are exactly those shares that'll
Cecil own. All that Alice & Bob have to do is to calculate the exact number of shares they should emit and
assign to him.

Since scripts can work with historical prices, it's easy for Alice to do this weeks later. She uses
`calculate_shares.py`, where she puts all relevant info about Cecil's transaction. She's given
exactly the output she needs:

```
Date:        2018-01-07
Deposited:   10 ETH
Eur value:   8786.4
Share price: 0.945
Shares:      9293
```

This means, that by this transaction, fund is 10 ETH richer and in the return, it must emit 9293 shares for Cecil. She
can input this data to `data.py`:

```
    ('2018-01-07', f.ABCT,
        add_shares, o.Cecil, 9293,
        add, c.ETH, 10),
```

Note the date - although the accounting may happen later, all Alice has to do is to use the correct
(actual) day of the trade. This is great, because Cecil won't be (so) nervous about when A&B do the accounting.

Finally, Alice and Bob should:
- tell Cecil he'd bought X shares
- Cecil unbalanced the portfolio a little. Maybe A&B should rebalance a little (i.e. sell some ETH for BTC and XLM).

Note that if Cecil would send EUR instead of ETH, the process would look pretty much the same. From the perspective of the
code, c.EUR is currency just like any other.

## Cecil wants to exit the fund

After deciding how much and what currency does he want to withdraw, it's very much the same as
investing - only with 'remove_shares', and 'remove' verbs in the trades log.

## Alice wants to rebalance the portfolio

Say, she wants to buy ADA for 0.5 BTC. This basically means, that fund is 0.5 BTC poorer and 8775 ADA
(that's what she's got at her favorite exchange) richer. She simply adds a new trade:

```
    ('2018-01-14', f.ABCT,
        remove, c.BTC, 0.5,
        add, c.ADA, 8775)
```

That's it. Value of the portfolio and therefore also the number of shares stays intact.

# Related topics

## Secure storage

It's probably not a good idea to keep your funds on an exchange. Hardware wallets such as Trezor and
Ledger Nano do a decent job to keep your investment secure. TODO: describe primitive multisig - any
3 out of 5 maintainers can manipulate the funds.

## First sight rule

Imagine working with current (i.e. not historical) prices. You run the composition_summary script 5
times, and you get 5 different results (because of fluctuations on the markets). Naturally,
different results won't be equally good for different investors. Which one should you take?

Since Alice is an accountant and shareholder at the same time, she may be tempted to
choose the one (out of the 5) result, which she likes most. Even if she is a moral human being -
it's slippery slope and it's hard to be 100% objective.

To solve such issues, there's a simple rule: before doing the trade, run script once, and get all
the data you need. Even if the trade itself takes some time and prices change, don't re-run the
script. This way, the trades won't be accounted as precisely as possible, but the whole system will be
fair. System, which adds a bit of (fair) randomness to each trade is still quite a good system.

## Fees

Simply ignore them. If you find out, that you should have 10 ETH on your account, but you have only
9.5 ETH (damn, those fees are high!) create a correction trade. This way, fees are distributed to
individual investors in a fair manner.

## What to buy

Some general crypto-investing advice you may find useful:

- Read the white paper. If it looks like a powerpoint presentation, full of fluffy promises and no
  real solutions, don't buy.
- Be sure you understand the core concepts and a value proposition.
- Are the promises achievable? If someone promises zero fees, no inflation, instant transaction,
  100% anonymity, smart contracts at the same moment, then it's either superhuge Satoshi-prize
  worth concept, or pure scam. The latter is much more probable.
- Does this bring anything new? Or is it just coloured Bitcoin, Ethereum, whatever?
- Are you buying a promise or does it already work?
- Check out the major developers' history and contributions. For many currencies, the currency
  itself is the first real project of their developers (I was shocked, how many coins fall into this
  category). Advertising such people as 'skilled developers with lots of experience' is laughable.
  Don't buy.
- Don't buy coins/tokens designed for a specific industry. Shared workspaces, car renters, music producers,
  cloud services, bananas, IoT, sewer cleaners, IT freelancers, artist and many many other
  professions don't need a separate coin. Stability, security, tamper-resistancy, quick & cheap
  transactions, smart contracts, anonymity: these are universal qualities which can power any industry
  there is.
