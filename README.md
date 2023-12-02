This repo contains all of the scripts and references to other github repos that are used for the St Catherine website.

**Calendar Events**

ical_to_crontab will pull a ical feed, grab a user-defined number of days of events in the future, and create crontab entries to start and stop the audio streamer. This audio feed is then streamed with Icecast.

**in_current_event**

in_current_event is written as a Google Cloud Function and is deployed directly from Cloud Source Repository, which is read-only synced to this git repo.
When called, the function will pull the defined calendar URL, make a timeline-ordered list of events, and check if the current time falls into a defined event. It will return True or False in a JSON structure along with the current function execution time, the event start time, and a shortened version of the event title. Our current usage of this function is to rename a sermon recording once it completes and is copied from Google Drive to our YouTube channel.

**Incognito Mode**

We embed events, calendars, and other objects from One Church, but the embeds break in incognito mode. This script will do its best to detect that the user is in an incognito or private window and will notify them that the site may not work correctly.

Detect Incognito mode repo:
https://github.com/Joe12387/detectIncognito

CDN-based script

```<script src="https://cdn.jsdelivr.net/gh/Joe12387/detectIncognito@v1.3.0/dist/es5/detectIncognito.min.js"></script>```

Test with https://detectincognito.com/
