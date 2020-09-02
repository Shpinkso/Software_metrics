from gitlabMetrics import *
from datetime import datetime, timedelta

testmode = 'test_'
gitlab_project_id = 278964

def test_object_creation():
    gl_metrics = GitlabMetrics(testmode)

def test_connection():
    gl_metrics = GitlabMetrics(testmode)
    gl_metrics.connect()

def test_load_project_gets_the_right_id():
    gl_metrics = GitlabMetrics(testmode)
    gl_metrics.connect()
    gl_metrics.load_project(gitlab_project_id)
    loaded = gl_metrics.get_project()
    assert loaded.id == gitlab_project_id

def test_load_project_commits():
    gl_metrics = GitlabMetrics(testmode)
    gl_metrics.connect()
    gl_metrics.load_project(gitlab_project_id)
    date_1_week_ago = datetime.now() - timedelta(days=7)
    gl_metrics.load_project_commits_since(date_1_week_ago)

