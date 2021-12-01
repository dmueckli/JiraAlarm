import requests
import time
import vlc

from secrets import user, password
from constants import *
from requests.auth import HTTPBasicAuth
from requests.models import HTTPError
from threading import Thread

# Variablen
alarm = False
tStart = time.time()

# Funktionen
def play():
    media = vlc.MediaPlayer('media/siren.wav')
    media.play()


def seconds_passed(tstmp, seconds):
    return time.time() - tstmp >= seconds


def alarm():
    T = Thread(name='Alarm', target=play)       # Thread erstellen...
    T.start()                                   # ...und starten

# TODO: Die JSON Abfrage als Funktion auslagern # <<-- Ist...
def getJSON(base_url, api_endpoint, headers, params, user, password):
    response = requests.get('{0}{1}'.format(base_url, api_endpoint),
                            auth=HTTPBasicAuth(user, password), headers=headers, params=params)
    response.raise_for_status()
    print('Return Code:', response.status_code)
    jsonResponse = response.json()
    return response.json()                      # ...das so richtig?! -->>


# Alle X Sekunden wird die Queue abgefragt.
while True:
    if seconds_passed(tStart, seconds=15) == True:
        try:

            # JSON Decoding
            jsonResponse = getJSON(base_url='https://service.muecklich.com', api_endpoint='/rest/servicedeskapi/servicedesk/1/queue/7',
                                   headers=headers, params={'includeCount': 'true'}, user=user, password=password)
            #jsonResponse = response.json()

            print("Queue Name:", jsonResponse["name"])
            print("Issue Count:", jsonResponse["issueCount"])

            # Wenn mindestens ein Vorgang in der Warteschlange ist, wird ein Alarm ausgelöst.
            if jsonResponse["issueCount"] >= 1:
                alarm()

        # Error handing...
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

        tStart = time.time()