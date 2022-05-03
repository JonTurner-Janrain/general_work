import csv, time, json, sys
from janrain.capture import Api, config
from collections import Counter


##################################
# passwordQuery.py
#

# credentials....
#
## jt-test-01-dev deets
#typeName = "ch4"
#target = 'jt-test-01-dev'
#mymod = 10

## ch4-int deets
#typeName = "user"
#target = 'ch4-int'
#mymod = 10000

## ch4-int deets
# typeName = "user"
# target = 'metadata-dashboard'
#mymod = 100000

## rogers-cc-dev deets
typeName = "user_fido_qa"
target = 'rogers-cc-dev'
targetUrl = 'https://rogers-fido-dev.janraincapture.com'
targetID = ''
targetSecret = ''

## jt-test
#typeName = 'user'
#target = 'jt-dev-app'
#targetUrl = 'https://akamai-security-product-development-lab-joturner.us-dev.janraincapture.com'
#targetID = ''
#targetSecret = ''
#mymod = 100000
########

timestr = time.strftime("%Y%m%d-%H%M%S")
with open("res//results-" + target + "-" + typeName + "-" + timestr + ".csv", "x", newline='') as csv_file:
    writer = csv.writer(csv_file)


#    creds = config.client(target)

#   api = Api(creds['apid_uri'], creds)
    defaults = {
        'client_id': targetID,
        'client_secret': targetSecret
    }

    api = Api(targetUrl, defaults)

    result = api.call('/entity.count', type_name=typeName)
    print("/entity.count == ", result)

    mycount = 0
    last_id = 0
    z = []
    while True:
#        if(mycount % mymod == 0):
        print("mycount = ", mycount)
        try:
            response = api.call('/entity.find',
                                type_name     =   typeName,
                                max_results   =   10000,
                                attributes    =   '["id", "uuid", "email", "password"]',
                                sort_on       =   '["id"]',
                                filter        =   "id > {}".format(last_id)
                        )
        except ValueError:
            print("ValueError occurred with id: ", repr(record['id']))
            raise
        except: 
            print("Unexpected Error wih API: ", str(sys.exc_info()))
            print("last ID processed: " + repr(record['id']))
        #    print(json.dumps(response, indent=4, sort_keys=True))
            raise

        if response['stat'] == 'ok' and response['result_count'] > 0:
            for record in response['results']:
#                print(type(record['password']).__name__)
#                z.append(type(record['password']).__name__)

#                last_id = record['id']
#                continue

                if(record['password'] != None):
#                    print(record['password']['type'])
                    try:
                        z.append(record['password']['type'])
#                        print(type(record['password']).__name__, " : ", record['password'])
                        writer.writerow([record['uuid'], record['password']['type']])
#                        last_id = record['id']
#                        continue
                    except KeyError:
                        z.append(record['password']['password']['type'])
#                        print(type(record['password']).__name__, " : ", record['password']['password']['type'])
                        writer.writerow([record['uuid'], record['password']['password']['type']])
#                        last_id = record['id']
#                        continue

                else:
                    z.append("None")
                    writer.writerow([record['uuid'], "None"])
                last_id = record['id']
            mycount += response['result_count']
#            if(mycount >= 100000):
#                break
            time.sleep(1.5)   # try a delay in processing to see if it helps get through the large volume of records...
        else:
            break

    print(Counter(z))

