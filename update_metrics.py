from gitlabMetrics import *
import yaml
import argparse

prodmode = ''

def main():
    login_dict = yaml.safe_load(open('login.yml'))
    gl_project = login_dict['gitlab_project_id']
    gl_metrics = GitlabMetrics(prodmode)
    gl_metrics.connect()
    gl_metrics.load_project(gl_project)

    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="iso8601 date",type=str)
    args = parser.parse_args()
    if args.date == 'latest':
        print("Updating gitlab metrics from project {} since last entry..".format(gl_project))
        date = gl_metrics.get_date_of_last_commit_in_database()
    else:
        print("Updating gitlab metrics from project {} since {}".format(gl_project,args.date))
        date = args.date
    
    gl_metrics.load_project_commits_since(date)
    gl_metrics.add_commits_to_database()

if __name__ == "__main__":
    main()
