import pymysql
import yaml

class DBInterface:
    def __init__(self):
        login_dict = yaml.safe_load(open('login.yml'))
        self.url = login_dict.get('mysql_url')
        self.user = login_dict.get('mysql_user')
        self.pw = login_dict.get('mysql_password')
        self.db = login_dict.get('mysql_db')
    def connect(self):
        self.mydb = pymysql.connect(self.url, self.user, self.pw, self.db)
        self.cursor = self.mydb.cursor()
        self.cursor.execute("SELECT VERSION()")
    def get_most_recent_record_date(self, date, table):
        self.cursor.execute("select MAX({}) from {};".format(date,table))
        return self.cursor.fetchone()
    def insert(self, 
