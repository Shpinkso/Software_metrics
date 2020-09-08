from datetime import datetime
import calendar
import time
from dateutil import parser
''' 
Partial credit to https://gist.github.com/squioc/3078803 although there seems to be
a bug related to timezones. Converting an ISO 8601 time string to epoch and back again
caused an hour to be added on somewhere along the line, so my unit tests failed.
Given that I want to use the same timezone in both directions, I glued together some
other code to keep everything in GM time. Original code from the website was:

def epoch_to_iso8601(timestamp):
    return datetime.fromtimestamp(timestamp).isoformat()

def iso8601_to_epoch(datestring):
    return calendar.timegm(datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%S.%f").timetuple())
'''

class Datetime2Epoch:
    def string_to_datetime(self, dt):
        if type(dt) is datetime:
            result = dt
        else:
            result = parser.parse(dt)
#        removed_zone = dt.split('+',1)[0] # We're removing the timezone to simplify. We only care about days for now
#        result = datetime.strptime(removed_zone, '%Y-%m-%dT%H:%M:%S.%f')
        print("converted {} {} to {} {}".format(type(dt),dt, type(result),result))
        return result
    def d2e(self, dt: datetime) -> int:
        return calendar.timegm(dt.timetuple())
    def e2d(self, e: int) -> datetime:
        return datetime.fromtimestamp(e)
