import csv, time, json
from janrain.capture import Api, config


##################################
# getUserRecordIds.py
#

# credentials....
#
## jt-test-01-dev deets
#type_name = "ch4"
#target = 'jt-test-01-dev'

## ch4-int deets
typeName = "user"
target = 'ch4-int'

## ch4-int deets
#typeName = "user"
#target = 'ch4-stage'
########

timestr = time.strftime("%Y%m%d-%H%M%S")
csv_file = open("results-" + target + "-" + typeName + "-" + timestr + ".csv", "x", newline='')
writer = csv.writer(csv_file)


creds = config.client(target)

api = Api(creds['apid_uri'], creds)

result = api.call('/entity.count', type_name=typeName)
print(result)
print("\n")

last_id = 0
while True:
    response = api.call('/entity.find',
                        type_name     =   typeName,
                        max_results   =   1000,
                        attributes    =   '["id", "uuid", "email", "lastUpdated"]',
                        sort_on       =   '["id"]',
                        filter        =   "id > {}".format(last_id)
                )

#    print(json.dumps(response, indent=4, sort_keys=True))

    if response['stat'] == 'ok' and response['result_count'] > 0:
        for record in response['results']:
#            print(record)
            writer.writerow([record['id'], record['uuid'], record['email']])
            last_id = record['id']
    else:
        break



