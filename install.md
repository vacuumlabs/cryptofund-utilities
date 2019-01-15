# Quick install
- clone the repo
- get python3. All `python` commands means python3.
- optional - create and activate [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
- (sudo) `pip install requests`
- [get a CoinMarketCap API KEY](https://coinmarketcap.com/api/documentation/v1/#section/Quick-Start-Guide) and hardcode it in `currency_info.py`

# Slack setup
- `pip install slackclient`
- create the Slack's [legacy token](https://get.slack.help/hc/en-us/articles/215770388-Create-and-regenerate-API-tokens)
- hardcore the token into the `inform_slack.py`
- setup cronjob, sending reports periodically


