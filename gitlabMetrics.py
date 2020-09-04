import gitlab
import yaml
from datetime import datetime
from db_wrapper import *

class GitlabMetrics:
    def __init__(self, testmode):
        login_dict = yaml.safe_load(open('{}login.yml'.format(testmode)))
        self.gl_server = login_dict.get('gitlab_url')
        self.api_key = login_dict.get('gitlab_api_key')
        self.commits_tbl = login_dict.get('git_commit_table')
        self.db_connector = DBInterface(testmode);
    def connect(self):
        self.gl = gitlab.Gitlab(self.gl_server, private_token=self.api_key)
        try:
            self.gl.auth()
        except:
            raise
        self.db_connector.connect()
        self.db_connector.set_table(self.commits_tbl)
    def load_project(self, project_id):
        self.project = self.gl.projects.get(project_id)
    def get_project(self):
        return self.project
    def load_project_commits_since(self, time: datetime):
        self.commits = self.project.commits.list(since=time)
    def get_date_of_last_commit_in_database(self) -> datetime:
        date_tup = self.db_connector.get_max_value()
        return date_tup[0]
    def add_commits_to_database(self):
        for commit in self.commits:
            schema_tup = (commit.id, commit.committer_name, commit.committed_date)
            self.db_connector.insert(schema_tup)
          
