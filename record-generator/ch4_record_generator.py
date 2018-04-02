#!/usr/bin/env python3
from __future__ import print_function

from random import randint, choice
from sys import stdout

from janrain.capture import Api, cli

from lib.pprint import pprint
from lib.random_user import random_user
from lib.random_date import random_date


def main():
    parser = init_parser()
    args = parser.parse_args()
    api = parser.init_api()
    batch = []

    for i in range(int(args.record_count)):

        attributes = random_user(choice(['male', 'female']))

        if args.verified:
            attributes['emailVerified'] = random_date("%Y-%m-%d %H:%M:%S")

        if args.password:
            attributes['password'] = args.password

        batch.append(attributes)

        if ((i + 1) % int(args.batch_size) == 0):
            batch_create(api, batch, args.type_name)
            batch = []
            print("{} of {}...\r".format(i + 1, args.record_count))


    if batch:
        batch_create(api, batch, args.type_name)

    print("\nDone")


def batch_create(api, batch, type_name):
    pprint(api.call('entity.bulkCreate', type_name=type_name,
             timeout=20, all_attributes=batch))


def init_parser():
    parser = cli.ApiArgumentParser()
    parser.add_argument('-c', '--record-count', default=1,
                        help="number of dummy records to load")
    parser.add_argument('-t', '--type-name', default=None, required=True,
                        help="entity type name")
    parser.add_argument('-p', '--password', default=None,
                        help="If set this password value will be used for ALL dummy records")
    parser.add_argument('--verified', action='store_true',
                        help="If set dummy records will be created with verified emails")
    parser.add_argument('-b','--batch-size', default=50,
                        help="size of entity.bulkCreate batches")
    return parser


if __name__ == "__main__":
    main()
