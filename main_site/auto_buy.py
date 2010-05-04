"""
auto_buy.py
This script can be used to automate gift buying for Persons. All Persons who 
have not received a gift within their gift frequency (one week, two weeks, or
one month) will matched with a gift and billed for that gift. This script
should be automated using cron.
"""

#Load Django environment
from django.core.management import setup_environ
import settings
setup_environ(settings)

from datetime import *
from myrchme.main_site.helpers import *
from myrchme.main_site.models import *


def shadow_buy():
    """
    shadow_buy:
    Auto-purchases gifts for all Persons who are due.
    """
    # checks to make sure there are active products
    if Products.objects.filter(is_active=True).count()==0:
        raise NoMerchAtAll

    persons = Person.objects.all()

    # loops through our persons to shop for those who are due merchandise
    for person in persons:
        # sets freq to a timedelta instance from preferences
        if person.gift_freq == "WEEK":
            freq = datetime.timedelta(7)
        elif person.gift_freq =="BIWK":
            freq = datetime.timedelta(14)
        elif person.gift_freq == "MNTH":
            freq = datetime.timedelta(30)
        else:
            freq = datetime.timedelta.max  #for users with freq='OFF'

        # stores most recent gift
        most_recent_gift = Transactions.objects.filter(buyer = person
                                              ).latest('create_date')
        # compares today, the date of last purchase and frequency to
        # conditionally buy a gift
        if datetime.today() - most_recent_gift.create_date > freq:
            try:
                buy(person, get_random_product())
            except NoMerchForPerson:
                #TODO: Alert user by email
                continue
                

#Makes this file into an executable script
#Usage: python autobuy.py
if __name__ == "__main__":
    auto_buy()