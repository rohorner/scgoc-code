import ics
import requests
from pprint import pprint

# URL of the "Services" calendar feed
url_services = "https://stcatherinechurch.onechurchsoftware.com/api/calendars/feed/7iWxebAmvU5PJQgQXh663Cut1ALT9Sz+j+xA==G8Mcb69uvXI0GK8adgGCPXVWnNPI/ni32/fj4/A30Pw==t7aqLeA2Q7ky2C"
# URL of the "Main" calendar feed
url_main = "https://stcatherinechurch.onechurchsoftware.com/api/calendars/feed/g0mxebAmvU5PJQWp4H4WrHywwZHCxjmSk7Rg==G8Mcb69uxvifTK8adgGCPXVWnNPI/ni32/fj4/A30Pw==t7aqLeA2Q7ieAM"

calendar = ics.Calendar(requests.get(url_services).text)
# print(calendar.__dict__)

# Get the events from the calendar
pprint(calendar.events)

# # Print the events
# for event in events:
#     pprint.pprint(event.__dict__)
#     print("\n\n")