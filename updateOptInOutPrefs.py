#!/usr/bin/env python3
#from sys import stdout
from datetime import datetime

from janrain.capture import Api, cli
import csv, json, sys, time

alpha = '[{"name":"C4_Data_Matching",'
bravo = '{"name":"C4_Targeted_Ads",'
charlie = '{"name":"C4_Personalised_Ads",'

#xray = '{"optedOut":"false},{"setDate":"created"}]'
#yankee = '{"optedOut":"true},{"setDate":"dateTime.now"}]'
xray = '"optedOut":"false","setDate":"'
yankee = '"optedOut":"true","setDate":"'

Ax = alpha + xray
Ay = alpha + yankee
Bx = bravo + xray
By = bravo + yankee
Cx = charlie + xray
Cy = charlie + yankee

timestr = time.strftime("%Y%m%d-%H%M%S")

def main():
    parser = init_parser()
    args = parser.parse_args()
    api = parser.init_api()
    try:
        csv_success = open("Success-{}-{}-{}.csv".format(args.config_key, args.type_name, timestr), 'wt')
        csv_error = open("Error-{}-{}-{}.csv".format(args.config_key, args.type_name, timestr), 'wt')
        successwriter = csv.writer(csv_success)
        errorwriter = csv.writer(csv_error)
    except:
        print("Unable to open log files: ", str(sys.exc_info()))
        return

    with open(args.input_file, 'rt') as csvfile:
        csvreader = csv.DictReader(csvfile, fieldnames=['userId', 'uuid'])
        for row in csvreader:
            filt = """uuid = '""" + row['uuid'] + """'"""
            try:
                result = api.call('/entity.find', type_name=args.type_name,
                                    filter=filt,
                                    attributes='["optInOutPreferences", \
                                                "email", \
                                                "dataSharingStatus", \
                                                "targetedAdsStatus", \
                                                "lastUpdated",\
                                                "created"]')
            except KeyboardInterrupt:
                raise
            except:
                print("Unexpected Error wih entity.find API: ", str(sys.exc_info()))
                print("last ID processed: " + repr(row['uuid']))
                errorwriter.writerow([row['uuid'], 'entity.find', str(sys.exc_info())])

            if(result['stat'] == 'ok'):
                record = result['results'][0]
                if not record['optInOutPreferences']:   # if this record has not been updated with optInOutPrefs
                    datestr = str(datetime.now())
                    attr = []
                    attr.append('{"optInOutPreferences":')
                    if record['dataSharingStatus'] == None:
                        attr.append(Ax)
                        attr.append('{}"}}'.format(record['created']))
                    elif record['dataSharingStatus'] == OPTED_OUT:
                        attr.append(Ay)
                        attr.append('{}"}}'.format(datestr))

                    if record['targetedAdsStatus'] == None:
                        attr.append(', ')
                        attr.append(Bx)
                        attr.append('{}"}},'.format(record['created']))
                        attr.append(Cx)
                        attr.append('{}"}}'.format(record['created']))
                    elif record['targetedAdsStatus'] == OPTED_OUT:
                        attr.append(', ')
                        attr.append(By)
                        attr.append('{}"}},'.format(datestr))
                        attr.append(Cy)
                        attr.append('{}"}}'.format(datestr))

#                    attr.append('], "profiles": [{}]}')
                    attr.append(']}')
                    #print('Processing: ', row['userId'], '\t', ''.join(attr))

                    try:
                        upd_result = api.call('/entity.update',
                                                type_name=args.type_name,
                                                uuid=row['uuid'],
                                                attributes=''.join(attr))
                    except KeyboardInterrupt:
                        raise
                    except:
                        print("Unexpected Error with entity.update API: ", str(sys.exc_info()))
                        print("last ID processed: " + repr(row['uuid']))
                        errorwriter.writerow([row['uuid'], 'entity.update', str(sys.exc_info())])
                    
                    # writerow to success log
                    successwriter.writerow([row['uuid'], 'updated'])

                else:   # record has already been updated, bail out
                    print("Skipping: {}, no changes needed".format(row[uuid]))
                    successwriter.writerow([row['uuid'], 'no changes needed'])

                csv_success.flush()
            else:
                print("Error: user record not found - uuid: ", row['uuid'])
                errorwriter.writerow([row['uuid'], 'entity.find', "User record not found"])
                csv_error.flush()

    csv_success.close()
    csv_error.close()

    print("\nDone!")

def init_parser():
    parser = cli.ApiArgumentParser()
    parser.add_argument('-f', '--input_file', default=None, required=True,
                        help="file with list of IDs to process")
    parser.add_argument('-t', '--type-name', default=None, required=True,
                        help="entity type name")
#    parser.add_argument('-b','--batch-size', default=100,
#                        help="size of entity.bulkCreate batches")
    return parser


if __name__ == "__main__":
    main()
