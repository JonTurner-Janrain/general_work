#!/usr/bin/env python3

from faker import Faker
from random import randint, choice
from .random_date import random_date

def random_dependents(num):
    fake = Faker()
    dependents = []
    for _ in range(num):
        dependents.append({
            "age": str(randint(1, 18)),
            "birthday": random_date("%Y-%m-%d"),
            "gender": choice(['M', 'F']),
            "idNumber": str(randint(1,99)),
            "name": fake.name(),
            "relationship": choice(["child", "mother", "father", "grandparent", "grandchild"]),
            "traitEyeColor": {
                "traitDate": random_date("%Y-%m-%d"),
                "traitNumber": str(randint(1,99)),
                "traitSequenceNumber": str(randint(1,99)),
                "traitType": fake.word(),
                "traitValue": fake.word(),
            }
        })
    return dependents
