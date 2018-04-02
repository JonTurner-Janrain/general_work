#!/usr/bin/env python3

from random import randint, choice
from .random_date import random_date


def random_trait():
    return {
        "traitDate": random_date("%Y-%m-%d"),
        "traitNumber": "TRAIT_NUMBER_HERE",
        "traitSequenceNumber": "TRAIT_SEQUENCE_NUMBER_HERE",
        "traitType": "TRAIT_TYPE_HERE",
        "traitValue": choice([None, 'True', 'False'])
    }
