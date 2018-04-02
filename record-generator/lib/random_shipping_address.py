#!/usr/bin/env python3

from faker import Faker
from random import randint, choice
from .random_date import random_date


def random_shipping_address():
    fake = Faker()
    return {
        "POBoxNbr": choice([None, str(randint(1,999))]),
        "address1": fake.street_address(),
        "address2": choice([None, "Suite " + str(randint(1, 99)), "Apt " + str(randint(1, 99))]),
        "address3": None,
        "aptNbr": choice([None, str(randint(1,999))]),
        "city": fake.city(),
        "country": fake.country(),
        "postalCategoryCode": None,
        "streetName":  choice([None, fake.street_name()]),
        "streetNbr": choice([None, str(randint(1,999))]),
        "territory": None,
        "zip": choice([None, fake.postcode()]),
        }
