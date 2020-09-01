from db_wrapper import *
import pymysql

def test_object_creation():
    database = DBInterface('test_')

def test_connection():
    database = DBInterface('test_')
    database.connect()

def test_get_latest_date_in_table():
    login_dict = yaml.safe_load(open('test_login.yml'))
    url = login_dict.get('mysql_url')
    user = login_dict.get('mysql_user')
    pw = login_dict.get('mysql_password')
    db = login_dict.get('mysql_db')
    test_db = pymysql.connect(url, user, pw, db)
    cursor = test_db.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS test_commits")
        test_db.commit()
    except:
        assert False
    sql = """CREATE TABLE test_commits (
             COMMIT_ID INT(20) NOT NULL, 
             AUTHOR_NAME VARCHAR(20) NOT NULL, 
             DATETIME VARCHAR(30) NOT NULL)"""
    try:
        cursor.execute(sql)
        test_db.commit()
    except:
        assert False
    
    sql = """INSERT INTO test_commits VALUES (
             1,
             'Mid',
             '2016-01-02T00:00:00')"""
    try:
        cursor.execute(sql)
        test_db.commit()
    except:
        test_db.rollback()
        assert False
    sql = """INSERT INTO test_commits VALUES (
             2,
             'Max',
             '2016-01-02T00:00:01')"""
    try:     
        cursor.execute(sql)
        test_db.commit()
    except:
        test_db.rollback()
        assert False
    sql = """INSERT INTO test_commits VALUES (
             3,
             'Min',
             '2016-01-01T23:59:59')"""
    try:
        cursor.execute(sql)
        test_db.commit()
    except:
        test_db.rollback()
        assert False

    database = DBInterface('test_')
    database.connect()
    latest = database.get_most_recent_record_date('DATETIME','test_commits')

    assert latest[0] == "2016-01-02T00:00:01"

    test_db.close()
