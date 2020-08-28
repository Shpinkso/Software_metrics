from datetime import datetime
import calendar

class Datetime2Epoch:
    def d2e(self, dt):
        return calendar.timegm(datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f").timetuple())
    def e2d(self, e):
        return datetime.fromtimestamp(e).isoformat();
