from gitlabMetrics import *
from datetime import date

def test_object_creation():
    gl_metrics = GitlabMetrics()

def test_connection():
    gl_metrics = GitlabMetrics()
    gl_metrics.connect()

def test_get_project():
    gl_metrics = GitlabMetrics()
    gl_metrics.connect()
    gl_metrics.get_project()

def test_get_project_commits():
    gl_metrics = GitlabMetrics()
    gl_metrics.connect()
    gl_metrics.get_project()
    gl_metrics.get_project_commits_since(date(2020,8,20))
