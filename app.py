from __future__ import print_function
import requests
import json
import datetime
from flask import Flask, request
from dateutil import parser
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools



app = Flask(__name__)
app.debug = True





"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""


# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('credentials.json')


flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=10, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])


@app.route('/', methods=['POST'])
def get_next_arrival_time():
    json_dict = request.get_json(force=True)
    print(json_dict)

    when = None
    where = None
    name = None


    if 'where' in json_dict["queryResult"]["parameters"]:
        where = json_dict["queryResult"]["parameters"]["where"]
    if 'when' in json_dict["queryResult"]["parameters"]:
        when = json_dict["queryResult"]["parameters"]["when"]
    if 'name' in json_dict["queryResult"]["parameters"]:
        name = json_dict["queryResult"]["parameters"]["name"]




    return str(when) + str(where) + str(name)



        

#print get_next_arrival_time('BROOKHAVEN STATION')

'''if __name__ == "__main__":  
    app.run()'''
