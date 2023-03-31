import csv, time, json, sys
from janrain.capture import Api, config


##################################
# getUserEmails.py
#

# credentials....
#
## jt-test-01-dev deets
#typeName = "user"
#target = 'jt-test-01-dev'
#maxres = 10

## metadata-dashbaord deets
typeName = "user"
target = 'metadata-dashboard'
maxres = 1000

timestr = time.strftime("%Y%m%d-%H%M%S")
with open("results-" + target + "-" + typeName + "-" + timestr + ".csv", "x", newline='') as csv_file:
    writer = csv.writer(csv_file)


    creds = config.client(target)

    api = Api(creds['apid_uri'], creds)

    result = api.call('/entity.count', type_name=typeName)
    print(result)

    mycount = 0
    last_id = 0
    while True:
#        if(mycount % mymod == 0):
        print(mycount)
        try:
            response = api.call('/entity.find',
                                type_name     =   typeName,
                                max_results   =   maxres,
                                attributes    =   '["id", "email"]',
                                sort_on       =   '["id"]',
                                filter        =   "email is not null and id > {}".format(last_id)
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
        #            print(record)
                try:
                    writer.writerow([record['email']])
                except ValueError:
                    print("writerow - ValueError occurred with id: ", repr(record['id']))
                    print(str(sys.exc_info()))
    #                print(json.dumps(response, indent=4, sort_keys=True))
                    raise
                except:
                    print("Unexpected Error: ", str(sys.exc_info()))
                    print("last ID processed: " + repr(record['id']))
                    csv_file.closed
                    raise
                    break
                last_id = record['id']
            mycount += response['result_count']
#            if(mycount >= 100000):
#                break
#            time.sleep(1.5)   # try a delay in processing to see if it helps get through the large volume of records...
        else:
            break

