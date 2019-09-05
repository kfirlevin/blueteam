#!/bin/python
from requests.exceptions import HTTPError
from datetime import datetime
import requests

# hello


def getApi(port, api):
    try:
        response = requests.get('http://blue.develeap.com:' + port + api)
        response.raise_for_status()
    except HTTPError as http_err:
        # if api not found
        with open("errorLog.txt", "a+") as fh:
            fh.write("[{}] 'HTTP error occurred: {}'.format(http_err)\n".format(
                datetime.now(), http_err))
        return False
    except Exception as err:
        with open("erGETrorLog.txt", "a+") as fh:
            fh.write("[{}] 'Other error occurred: {}'.format(err)\n".format(
                datetime.now(), err))

        return False
    else:
        return True


def testAPI():
    health1 = getApi('8081/', 'health')
    health2 = getApi('8082/', 'health')
    # first checking health's api's
    if health1 == False or health2 == False:
        return False
    return True


if __name__ == "__main__":
    if testAPI():
        print("True")
    else:
        print("False")
