#! /usr/bin/env python
# URL to retrieve events in "Livestream" category:
#   https://stcatherinechurch.onechurchsoftware.com/api/events?category=710&active=true
# "active=true" means return only events that are occuring now or in the future

import requests
import arrow
import variables
from pprint import pprint
import json

# Convert output times to local
timezone = "US/Mountain"

headers = {"Content-Type": "application/json; charset=utf-8", "Ocs-Api-Key": variables.API_KEY}
# event_list = json.loads(requests.get(variables.EVENTLIST_URL, headers=headers).text)
event_list = requests.get(variables.EVENTLIST_URL, headers=headers).json()

class StreamableEvent():
    def __init__(self, id, title, start, end):
        self.id = id        # ID of the event. We use the one generated by One Church to keep things consistent
        self.title = title
        self.start_time = start
        self.end_time = end

    def __repr__(self):
        return 'StreamableEvent(\n\tid: %s\n\tname: %s\n\tstart: %s\n\tend: %s)\n)' % (
            self.id, self.title,
            self.start_time, self.end_time)

# Sample event names:
# Sunday After Nativity Liturgy of St. John Chrysostom Orthros 8:15am, Divine Liturgy 9:30am
# 12th Sunday of Luke-Orthros 8:15am, Divine Liturgy 9:30am
# Find the word "Orthros" and back off one letter, which is a hyphen or space
def shorten_title(title):
    return title[:title.find('Orthros')-1] if title.find('Orthros') > 0 else title


stream_event_list = []
for event in event_list["data"]:
    try:
        stream_event_list.append(
            StreamableEvent(
                event["id"],
                shorten_title(event["name"]),
                arrow.get(event["times"][0]["start"]).to(timezone).format(),
                arrow.get(event["times"][0]["end"]).to(timezone).format()))
    except:
        print("event not streamable or info not found")

pprint(stream_event_list)
                        

