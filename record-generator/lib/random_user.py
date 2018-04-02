#!/usr/bin/env python3

import string
from random import randint, choice
from faker import Faker

from .random_date import random_date
from .random_dependents import random_dependents
from .random_identifier import random_identifier
from .random_primary_address import random_primary_address
from .random_shipping_address import random_shipping_address
from .random_trait import random_trait

from .options_clients import clients
from .options_leagacceptances import legalacceptances


def random_user(gender):
    fake = Faker()
    name_method = getattr(fake, 'name_' + gender)
    prefix_method = getattr(fake, 'prefix_' + gender)
    suffix_method = getattr(fake, 'suffix_' + gender)
    name = name_method()
    return {
        "clients": [choice(clients)],
        "displayName": name,
        "email": fake.email(),
        "emailVerified": choice([None, random_date("%Y-%m-%d %H:%M:%S +0000")]),
        "familyName": name.split(' ')[1],
        "gender": gender[0].upper(),
        "givenName": name.split(' ')[0],
        "lastLogin": choice([None, random_date("%Y-%m-%d %H:%M:%S +0000")]),
        "middleName": choice([None, fake.first_name(), fake.last_name()]),
        "primaryAddress": random_primary_address(),
        "profiles": [],
    }
