# imports
import requests
from requests.structures import CaseInsensitiveDict
import json
import datetime
import time

# all neccesary variables
id_channel = ''
id_item = ''
jwt_token = ''
crypto_address = ''


def claim(channel_id, item_id, jwt, user_input):  # claim function which makes post requests and other stuff
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {jwt}"
    headers["Content-Type"] = "application/json"
    data = json.dumps({"input": [user_input]})  # headers settings and user input added

    claim_response = requests.post(
        f"https://api.streamelements.com/kappa/v2/store/{channel_id}/redemptions/{item_id}", headers=headers,
        data=data)  # post request - 'claim'

    time_to_retry = datetime.datetime.fromtimestamp(int(claim_response.headers["x-ratelimit-reset"]) / 1000.0)
    # variable to store when does number of posts per minute reset

    if claim_response.headers["x-ratelimit-remaining"] == '0':
        while (datetime.datetime.fromtimestamp(time.time())) <= time_to_retry:  # waiting for restriction to expire
            pass

    if claim_response.status_code == 200:  # checking response status - if 200 it means
        # script successfully claimed item
        print(claim_response.status_code)
        print("claimed", user_input)
        print(datetime.datetime.today())

    else:  # else show any other response statuses if it is not successful
        print(claim_response.status_code)
        print(claim_response.text)
        print(datetime.datetime.today())


while True:
    get_response = requests.get(
        f"https://api.streamelements.com/kappa/v2/store/{id_channel}/items")  # get request - checking store with items

    if get_response.status_code == 200:  # if response successful unpack data
        response = json.loads(get_response.text)
        wanted = [i for i in response if i["_id"] == id_item]  # there is stored my item I want to claim

        if wanted[0]['quantity']['current'] != 0:  # if item is in store (is not sold)
            claim(id_channel, id_item, jwt_token, crypto_address)  # claim it
            time.sleep(9.58)

    elif get_response.status_code == 503:  # server 'overheated' so we will wait a sec
        time.sleep(30)

    elif get_response.status_code == 524 or get_response.status_code == 520 or get_response.status_code == 502:  # with this type of error I do not want to show response text since
        # it shows whole html page
        print(get_response.status_code)
        print(datetime.datetime.today())
        continue

    else:  # else show any other response statuses if it is not successful
        print(datetime.datetime.today())
        print(get_response.status_code)
        print(get_response.text)
        continue  # and go on start of while cycle


def main():
    pass
    # call the function


if __name__ == '__main__':
    main()
