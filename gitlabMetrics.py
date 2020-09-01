import gitlab
import yaml
from datetime import datetime

class GitlabMetrics:
    def __init__(self):
        login_dict = yaml.safe_load(open('login.yml'))
        self.gl_server = login_dict.get('gitlab_url')
        self.api_key = login_dict.get('gitlab_api_key')
        self.project_id = login_dict.get('gitlab_project_id')
        self.commits_tbl = login_dict.get('git_commits_table')
    def connect(self):
        self.gl = gitlab.Gitlab(self.gl_server, private_token=self.api_key)
    def get_project(self):
        self.project = self.gl.projects.get(self.project_id)
    def get_project_commits_since(self, time: datetime):
        self.commits = self.project.commits.list(since=time)
    def get_date_of_last_commit_in_database(self) -> datetime:
        print("moo")
    def add_commits_to_database(self):
        print("add")
