from gitlabMetrics import *
from jiraMetrics import *
import yaml
import argparse

prodmode = ''

def main():
    login_dict = yaml.safe_load(open('login.yml'))
    gl_project = login_dict['gitlab_project_id']
    jira_project_key = login_dict['jira_project_key']


    gl_metrics = GitlabMetrics(prodmode)
    gl_metrics.connect()
    gl_metrics.load_project(gl_project)

    jira_metrics = JiraMetrics(prodmode)
    jira_metrics.connect()
    try:
        jira_metrics.load_project(jira_project_key)
    except Exception as e:
        assert False, "{}".format(e)



    parser = argparse.ArgumentParser()
    parser.add_argument("--jdate", help="iso8601 date",type=str)
    parser.add_argument("--gdate", help="iso8601 date",type=str)
    args = parser.parse_args()
    if args.jdate == 'latest':
        print("Updating jira metrics from project {} since last entry..".format(jira_project_key))
        j_date = jira_metrics.get_date_of_last_done_issue_in_database()
    else:
        print("Updating jira metrics from project {} since {}".format(jira_project_key,args.jdate))
        j_date = args.jdate
    
    jira_metrics.load_done_project_issues_since(j_date)
    jira_metrics.add_issues_to_database()

    if args.gdate == 'latest':
        print("Updating gitlab metrics from project {} since last entry..".format(gl_project))
        gl_date = gl_metrics.get_date_of_last_commit_in_database()
    else:
        print("Updating gitlab metrics from project {} since {}".format(gl_project,args.gdate))
        gl_date = args.gdate
    
    gl_metrics.load_project_commits_since(gl_date)
    gl_metrics.add_commits_to_database()

if __name__ == "__main__":
    main()
