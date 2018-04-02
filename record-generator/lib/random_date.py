"""return a date(time) string for the given the date-time format"""
import time
from random import randint

def random_date(date_format):
    """ Return a random(ish) date for use as birthdays and the like. """
    string = "{}-{}-{} {}:{}:{}".format(randint(1950, 2000),
                                        str(randint(1, 12)).zfill(2),
                                        # there's 28 days in every month, right?
                                        str(randint(1,28)).zfill(2),
                                        str(randint(0,23)).zfill(2),
                                        str(randint(0,59)).zfill(2),
                                        str(randint(0,59)).zfill(2))
    parsed_time = time.strptime(string, "%Y-%m-%d %H:%M:%S")
    return time.strftime(date_format, parsed_time)