import json

def jdump(var):
    var = json.dumps(var, indent=4, sort_keys=True)
    return var
