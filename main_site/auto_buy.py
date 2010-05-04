"""
auto_buy.py
This script can be used to automate gift buying for Persons. All Persons who 
have not received a gift within their gift frequency (one week, two weeks, or
one month) will matched with a gift and billed for that gift. This script
should be automated using cron.
"""


#Makes this file into an executable script
#Usage: python autobuy.py
if __name__ == "__main__":
    auto_buy()