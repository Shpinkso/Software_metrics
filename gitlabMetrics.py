import gitlab
import yaml
from datetime import datetime

class GitlabMetrics:
    def __init__(self):
        self.login_dict = yaml.safe_load(open('login.yml'))
        self.gl_server = self.login_dict.get('gitlab_url')
        self.api_key = self.login_dict.get('gitlab_api_key')
        self.project_id = self.login_dict.get('gitlab_project_id')
    def connect(self):
        self.gl = gitlab.Gitlab(self.gl_server, private_token=self.api_key)
    def get_project(self):
        self.project = self.gl.projects.get(self.project_id)
    def get_project_commits_since(self, date: datetime):
        commits = self.project.commits.list(since=date)
        for commit in commits:
            print(commit)
    def get_date_of_last_commit_in_database(self) -> datetime:
        return datetime.today()
