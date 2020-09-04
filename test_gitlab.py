from gitlabMetrics import *
from datetime import datetime, timedelta
import pytest

testmode = 'test_'
gitlab_project_id = 278964

@pytest.fixture(scope="function")
def make_test_database():
    #setup
    login_dict = yaml.safe_load(open('test_login.yml'))
    table_name = login_dict.get('git_commit_table')
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


def test_object_creation():
    gl_metrics = GitlabMetrics(testmode)

def test_valid_connection_should_authorise(make_test_database):
    gl_metrics = GitlabMetrics(testmode)
    try:
        gl_metrics.connect()
    except Exception as e:
        assert False, "{}".format(e)

def test_load_project_gets_the_right_id(make_test_database):
    gl_metrics = GitlabMetrics(testmode)
    gl_metrics.connect()
    gl_metrics.load_project(gitlab_project_id)
    loaded = gl_metrics.get_project()
    assert loaded.id == gitlab_project_id

def test_load_project_commits(make_test_database):
    gl_metrics = GitlabMetrics(testmode)
    gl_metrics.connect()
    gl_metrics.load_project(gitlab_project_id)
    date_1_week_ago = datetime.now() - timedelta(days=7)
    gl_metrics.load_project_commits_since(date_1_week_ago)

def test_add_valid_commits_to_database_does_not_raise_exception():
    assert True
