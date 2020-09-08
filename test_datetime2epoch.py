from datetime2epoch import *
from datetime import datetime

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

