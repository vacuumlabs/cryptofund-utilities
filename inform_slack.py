from slackclient import SlackClient
from data import fund_constants as f
from composition_summary import composition_summary, tabulate_selection
from composition_summary import share_price

def report(fund):
    fund_summary, total = composition_summary(fund)
    data = tabulate_selection(fund_summary, ['ticker', 'price', 'percent'])

    return '*Price per share [€]: %.3f*' % share_price(fund) + \
        '\n\n```%s```' % data

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--channel', dest='channel', default=None)
    parser.add_argument('--fund', dest='fund', default=None)
    args = parser.parse_args()
    channel = args.channel
    fund = args.fund

    # This should be in a config file. This being said, everyone can see I'm a sensible developer
    # who knows what the best practices are, so I don't have to actually do this. Great!
    slack_token = "TODO: put the token here"
    sc = SlackClient(slack_token)

    sc.api_call(
      "chat.postMessage",
      channel=channel,
      text=report(fund),
    )
