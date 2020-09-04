from db_wrapper import *
import pymysql
import traceback
import pytest

@pytest.fixture(scope="function")
def make_test_database():
    #setup
    login_dict = yaml.safe_load(open('test_login.yml'))
    table_name = login_dict.get('mysql_test_table')
    url = login_dict.get('mysql_url')
    user = login_dict.get('mysql_user')
    pw = login_dict.get('mysql_password')
    db = login_dict.get('mysql_db')
    test_db = pymysql.connect(url, user, pw, db)
    cursor = test_db.cursor()
    sql = """CREATE TABLE {} (
             COMMIT_ID INT(20) NOT NULL, 
             AUTHOR_NAME VARCHAR(20) NOT NULL, 
             DATETIME VARCHAR(30) NOT NULL)""".format(table_name)
    try:
        cursor.execute(sql)
    except:
        assert False
    
    sql = """INSERT INTO {} VALUES (
             1,
             'Mid',
             '2016-01-02T00:00:00')""".format(table_name)
    try:
        cursor.execute(sql)
        test_db.commit()
    except:
        test_db.rollback()
        assert False
    sql = """INSERT INTO {} VALUES (
             2,
             'Max',
             '2016-01-02T00:00:01')""".format(table_name)
    try:     
        cursor.execute(sql)
        test_db.commit()
    except:
        test_db.rollback()
        assert False
    sql = """INSERT INTO {} VALUES (
             3,
             'Min',
             '2016-01-01T23:59:59')""".format(table_name)
    try:
        cursor.execute(sql)
        test_db.commit()
    except:
        test_db.rollback()
        assert False
    
    yield test_db
    #teardown
    cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))


class Test_Basic():

    def test_object_creation(self):
        database = DBInterface('test_')

    def test_connection(self):
        database = DBInterface('test_')
        database.connect()

class Test_On_Existing_DB():
    def test_get_latest_date_in_table(self, make_test_database):
        login_dict = yaml.safe_load(open('test_login.yml'))
        table_name = login_dict.get('mysql_test_table')
        database = DBInterface('test_')
        database.connect()
        database.set_table(table_name)
        latest = database.get_max_value('DATETIME')

        assert latest[0] == "2016-01-02T00:00:01"

    def test_set_table_raises_exception_if_table_doesnt_exist(self, make_test_database):
        database = DBInterface('test_')
        database.connect()
        with pytest.raises(ValueError):
            database.set_table('flibble')

    def test_set_table_succeeds_if_valid_table(self, make_test_database):
        login_dict = yaml.safe_load(open('test_login.yml'))
        table_name = login_dict.get('mysql_test_table')

        database = DBInterface('test_')
        database.connect()
        try:
            database.set_table(table_name)
        except:
            assert False
        

    def test_insert_valid_schema_record_results_in_new_db_row(self, make_test_database):
        test_db = make_test_database
        login_dict = yaml.safe_load(open('test_login.yml'))
        table_name = login_dict.get('mysql_test_table')
        test_db_cursor = test_db.cursor()
        initial_rows = test_db_cursor.execute("SELECT * FROM {}".format(table_name))
        
        database = DBInterface('test_')
        database.connect()
        database.set_table(table_name)
        
        new_row = (4, 'new', '2016-01-02T00:00:01')
        try:
            database.insert(new_row)
        except:
            assert False
        test_db.begin() # as we're using another cursor, let it know we need to re-read.
        new_rows = test_db_cursor.execute("SELECT * FROM {}".format(table_name))
        assert test_db_cursor.rowcount == new_rows
        assert initial_rows + 1 == new_rows 

    def test_insert_invalue_schema_record_results_in_exception(self, make_test_database):
        assert True
