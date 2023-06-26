#!/usr/bin/env python

from ics import Calendar
from crontab import CronTab
from datetime import datetime
import arrow
import requests
from pprint import pprint
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logging.debug('A debug message!')
# logging.info('We processed %d records', len(processed_records))

# URL of the "Services" calendar feed
url_services = "https://stcatherinechurch.onechurchsoftware.com/api/calendars/feed/7iWxebAmvU5PJQgQXh663Cut1ALT9Sz+j+xA==G8Mcb69uvXI0GK8adgGCPXVWnNPI/ni32/fj4/A30Pw==t7aqLeA2Q7ky2C"

# URL of the "Main" calendar feed
url_main = "https://stcatherinechurch.onechurchsoftware.com/api/calendars/feed/g0mxebAmvU5PJQWp4H4WrHywwZHCxjmSk7Rg==G8Mcb69uxvifTK8adgGCPXVWnNPI/ni32/fj4/A30Pw==t7aqLeA2Q7ieAM"

# Convert output times to local
timezone = "US/Mountain"

# How far out to retrieve events
event_window = 30

# One Church domain (this is used to strip out the event uid)
# INCLUDE THE '@' symbol!
oc_domain = "@stcatherinechurch.onechurchsoftware.com"

CRONFILE = './basecrontab.txt'
CRON_OUT = './outcrontab.txt'
START_COMMAND = '/home/stcatherine/streaming'
STOP_COMMAND = '/home/stcatherine/ending'


class StreamableEvent():
    def __init__(self, id, title, start, end):
        self.id = id        # ID of the event. We use the one generated by One Church to keep things consistent
        self.title = title
        self.start_time = start
        self.end_time = end
        self.cronStart = '' # The command we'll insert in crontab to start the stream or recording
        self.cronStop = ''   # The command we'll insert in crontab to stop the stream or recording

    def __repr__(self):
        return 'StreamableEvent(\n\tid:%s\n\tname:%s\n\t(%s to %s)\n)' % (
            self.id, self.title,
            self.start_time, self.end_time)


def UTC_to_local_datetime(event_time,tz):

    # Convert Arrow format to datetime before returning it.
    # Crontab wants everthing in legacy datetime format
    return(event_time.to(tz).datetime)


def get_stream_timeline(url, my_tz, window):

    try:
        calendar = Calendar(requests.get(url_services).text)
    except Exception as e:
        print(e)

    # initialize an empty list for the events
    event_list = []

    # populate the event list with just the components that we need to create crontab entries
    # Event ID, Event Name, and start/stop times
    # Use the ics 'timeline' iterator to return the events in chronological order
    for event in calendar.timeline:
        if arrow.utcnow() < event.begin < arrow.utcnow().shift(days=event_window):
            event_list.append(StreamableEvent(event.uid.removesuffix(oc_domain),
                                event.name,
                                UTC_to_local_datetime(event.begin,my_tz),
                                UTC_to_local_datetime(event.end,my_tz)
                                )
            )
    logging.info("Processed %d events", len(event_list))
    return(event_list)

def create_crontab_entries(events):

    for this_event in events:

        #Create cron entry for this_event START command
        job = crontab.new(command=START_COMMAND, comment = this_event.id+'::'+this_event.title)
        job.setall(this_event.start_time)

        #Create cron entry for this_event STOP command
        job = crontab.new(command=STOP_COMMAND, comment = this_event.id)
        job.setall(this_event.end_time)

        # Commit the job to the cron of the streamer username
        crontab.write_to_user(user='stcatherine')
        # Write to a file to confirm output
        #crontab.write(CRON_OUT)

if __name__ == '__main__':

     # Create or load the cron file (just a test file for now)
    try:
        crontab = CronTab(tabfile=CRONFILE)
        #crontab = CronTab(user='stcatherine')
    except:
        print ("Couldn't load cron file:", CRONFILE)

    upcoming_events = get_stream_timeline(url_services, timezone, event_window)

    create_crontab_entries(upcoming_events)
    
