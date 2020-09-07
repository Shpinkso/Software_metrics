from jiraMetrics import *
from datetime import datetime, timedelta
import pytest

testmode = 'test_'
jira_project_key = 'MM'

@pytest.fixture(scope="function")
def make_test_database():
    #setup
    login_dict = yaml.safe_load(open('test_login.yml'))
    table_name = login_dict.get('jira_task_table')
    url = login_dict.get('mysql_url')
    user = login_dict.get('mysql_user')
    pw = login_dict.get('mysql_password')
    db = login_dict.get('mysql_db')
    test_db = pymysql.connect(url, user, pw, db)
    cursor = test_db.cursor()
    sql = """CREATE TABLE {} (
             TASK_ID VARCHAR(20) NOT NULL,
             CREATED DATETIME NOT NULL,
             UPDATED DATETIME NOT NULL,
             DELTA_HOURS INT(20) NOT NULL)""".format(table_name)
    try:
        cursor.execute(sql)
    except:
        assert False
    sql = """INSERT INTO {} VALUES (
             'MM-1',
             '2020-09-07 11:28:55',
             '2020-09-07 11:28:56',
             '0')""".format(table_name)
    try:
        cursor.execute(sql)
        test_db.commit()
    except:
        test_db.rollback()
        assert False
    sql = """INSERT INTO {} VALUES (
             'MM-2',
             '2020-09-07 11:45:27',
             '2020-09-08 11:45:27',
             '24')""".format(table_name)
    try:
        cursor.execute(sql)
        test_db.commit()
    except:
        test_db.rollback()
        assert False
    sql = """INSERT INTO {} VALUES (
             'MM-3',
             '2020-08-01 11:45:27',
             '2020-08-05 11:45:27',
             '96')""".format(table_name)
    try:
        cursor.execute(sql)
        test_db.commit()
    except:
        test_db.rollback()
        assert False

    yield test_db
    #teardown
    cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))

def test_object_creation():
    jirametrics = JiraMetrics(testmode)

def test_connection(make_test_database):
    jirametrics = JiraMetrics(testmode)
    jirametrics.connect()

def test_load_valid_project_does_not_raise_exception(make_test_database):
    jirametrics = JiraMetrics(testmode)
    jirametrics.connect()
    try:
        jirametrics.load_project(jira_project_key)
    except Exception as e:
        assert False, "{}".format(e)

def test_load_done_project_issues_doesnt_get_prior_issues(make_test_database):
    jirametrics = JiraMetrics(testmode)
    jirametrics.connect()
    try:
        jirametrics.load_project(jira_project_key)
    except Exception as e:
        assert False, "{}".format(e)
    jirametrics.load_done_project_issues_since("2020-09-02T00:00:00.000")
    older_issues = ['MM-1','MM-2','MM-3','MM-4','MM-5']
    issues = jirametrics.get_loaded_issues()
    for issue in issues:
        assert issue.key not in older_issues
