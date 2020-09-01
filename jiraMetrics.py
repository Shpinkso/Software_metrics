from jira import JIRA
import yaml

class JiraMetrics:
    def __init__(self):
        login_dict = yaml.safe_load(open('login.yml'))
        self.jira_server = login_dict.get('jira_url')
        self.my_username = login_dict.get('jira_username')
        self.api_key = login_dict.get('jira_api_key')
    def connect(self):
        self.jira = JIRA(server=self.jira_server, basic_auth=(self.my_username,self.api_key))
