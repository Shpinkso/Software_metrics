from datetime2epoch import *

def test_object_creation():
    converter = Datetime2Epoch()

def test_date_to_epoch():
    converter = Datetime2Epoch()
    datetime = "2012-07-09T22:27:50.272517"
    epoch = converter.d2e(datetime)
    assert epoch == 1341872870

def test_epoch_to_date():
    converter = Datetime2Epoch()
    epoch = 1341872870
    datetime = converter.e2d(epoch)
    assert datetime == "2012-07-09T22:27:50"

def test_epoch_to_date_at_time_zero():
    converter = Datetime2Epoch()
    epoch = 0
    datetime = converter.e2d(epoch)
    assert datetime == "1970-01-01T00:00:00"

