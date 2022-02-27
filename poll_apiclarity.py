import time
import requests
from datetime import datetime, timedelta
from requests.exceptions import HTTPError

hosts = []


def poll_apiclarity():
    try:
        now = datetime.datetime.now()
        startTime = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        now_minus_10 = now - timedelta(minutes=10)
        endTime = now_minus_10.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        URL = "http://<APICLARITY IP ADDRESS>/api/apiEvents?startTime=" + startTime + "&endTime=" + endTime + "&showNonApi=false&page=1&pageSize=50&sortKey=time&sortDir=DESC"
        response = requests.get(URL)
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        for event in jsonResponse['items']:
            if event["specDiffType"] == "ZOMBIE_DIFF":
                if event["sourceIP"] not in hosts:
                    hosts.append(event["sourceIP"])

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def block_hosts():
    URL = "<Action host URL>"
    try:
        payLoad = {"hosts": hosts}
        response = requests.post(URL, data=payLoad)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    hosts.clear()

def main():
    while True:
        poll_apiclarity()
        block_hosts()
        time.sleep(10*60)

if __name__ == '__main__':
    main()
