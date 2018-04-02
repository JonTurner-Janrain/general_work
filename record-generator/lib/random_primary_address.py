#!/usr/bin/env python3

from faker import Faker
from random import randint, choice
from .random_date import random_date


def random_primary_address():
    fake = Faker()
    return {
        "address1": fake.street_address(),
        "address2": choice([None, "Suite " + str(randint(1, 99)), "Apt " + str(randint(1, 99))]),
        "city": fake.city(),
        "company": fake.company(),
        "country": fake.country(),
        "phone": choice([None, fake.phone_number()]),
        "zip": choice([None, fake.postcode()]),
        "zipPlus4": choice([None, None, None, str(randint(1000, 9999))])
        }
