from jira import JIRA
import yaml
from datetime import datetime
from db_wrapper import *
from datetime2epoch import *

class JiraMetrics:
    def __init__(self, testmode):
        login_dict = yaml.safe_load(open('{}login.yml'.format(testmode)))
        self.jira_server = login_dict.get('jira_url')
        self.my_username = login_dict.get('jira_username')
        self.api_key = login_dict.get('jira_api_key')
        self.tasks_tbl = login_dict.get('jira_task_table')
        self.db_connector = DBInterface(testmode);
    def connect(self):
        self.jira = JIRA(server=self.jira_server, basic_auth=(self.my_username,self.api_key))
        self.db_connector.connect()
        self.db_connector.set_table(self.tasks_tbl)
    def load_project(self, project_key):
        self.project = None
        projects = self.jira.projects()
        for project in projects:
            if project.key == project_key:
                self.project = project_key
                return
        raise ValueError("project key {} does not exist".format(project_key))
    def load_done_project_issues_since(self, dt: str):
        converter = Datetime2Epoch()
        datetime_obj = converter.string_to_datetime(dt)
        jira_dt_str = "{}-{}-{} {}:{}".format(datetime_obj.year,
                                              datetime_obj.month,
                                              datetime_obj.day,
                                              datetime_obj.hour,
                                              datetime_obj.minute)
        search_str = 'project = "{}" AND status = done AND updated > "{}"'.format(
                self.project,
                jira_dt_str)
        self.issues = self.jira.search_issues(search_str)
    def get_loaded_issues(self):
        return self.issues
    def get_date_of_last_done_issue_in_database(self):
        date_tup = self.db_connector.get_max_value('UPDATED')
        return date_tup[0]
    def add_issues_to_database(self):
        converter = Datetime2Epoch()
        for issue in self.issues:
            created = converter.string_to_datetime(issue.fields.created)
            updated = converter.string_to_datetime(issue.fields.updated)
            leadtime = updated - created
            lt_hours = leadtime.total_seconds() / 60 / 60
            schema_tup = (issue.key,
                          created.strftime('%Y-%m-%d %H:%M:%S'),
                          updated.strftime('%Y-%m-%d %H:%M:%S'),
                          lt_hours)
            print("add {}".format(schema_tup))
            self.db_connector.insert(schema_tup)
