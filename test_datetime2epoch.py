from datetime2epoch import *
from datetime import datetime
import dateutil.tz

def test_object_creation():
    converter = Datetime2Epoch()

def test_date_to_epoch():
    converter = Datetime2Epoch()
    dt = datetime(2012,7,9,22,27,50) #"2012-07-09T22:27:50.272517"
    epoch = converter.d2e(dt)
    assert epoch == 1341872870

def test_epoch_to_date():
    converter = Datetime2Epoch()
    epoch = 1341872870
    correct_datetime = datetime(2012,7,9,23,27,50)
    dt = converter.e2d(epoch)
    assert dt == correct_datetime #"2012-07-09T22:27:50"

def test_epoch_to_date_at_time_zero():
    converter = Datetime2Epoch()
    epoch = 0
    correct_datetime = datetime(1970,1,1,1,0)
    dt = converter.e2d(epoch)
    assert dt == correct_datetime #"1970-01-01T00:00:00"

def test_string_to_datetime_deals_with_datetime():
    converter = Datetime2Epoch()
    test_dt = datetime(2010,11,20,14,23,0)
    dt = converter.string_to_datetime(test_dt)
    assert dt == test_dt

def test_string_to_datetime_deals_with_no_timezone():
    converter = Datetime2Epoch()
    time_str = "2012-07-09T22:27:50.272517"
    check = datetime(2012,7,9,22,27,50,272517)
    dt = converter.string_to_datetime(time_str)
    assert dt == check

def test_string_to_datetime_deals_with_plus_timezone():
    converter = Datetime2Epoch()
    time_str = "2020-09-08T10:01:44.000-04:00"
    check = datetime(2020,9,8,10,1,44, tzinfo=dateutil.tz.tzoffset(None, -14400))
    dt = converter.string_to_datetime(time_str)
    assert dt == check


def test_string_to_datetime_deals_with_minus_timezone():
    converter = Datetime2Epoch()
    time_str = "2020-09-08T10:01:44.000+04:00"
    check = datetime(2020,9,8,10,1,44, tzinfo=dateutil.tz.tzoffset(None, 14400))
    dt = converter.string_to_datetime(time_str)
    assert dt == check
