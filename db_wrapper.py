import pymysql
import yaml

class DBInterface:
    def __init__(self, testmode):
        login_dict = yaml.safe_load(open('{}login.yml'.format(testmode)))
        self.url = login_dict.get('mysql_url')
        self.user = login_dict.get('mysql_user')
        self.pw = login_dict.get('mysql_password')
        self.db = login_dict.get('mysql_db')
    def connect(self):
        self.mydb = pymysql.connect(self.url, self.user, self.pw, self.db)
        self.cursor = self.mydb.cursor()
    def set_table(self,table):
        self.table = table
    def get_max_value(self, max_of):
        self.cursor.execute("select MAX({}) from {};".format(max_of,self.table))
        return self.cursor.fetchone()
    def insert(self, schema_tup):
        self.cursor.execute("INSERT INTO {} VALUES {}".format(self.table, schema_tup))
        try:
            self.cursor.execute("")
            self.mydb.commit
            result = True
        except:
            self.mydb.rollback()
            result = False
        return result # need to learn about exceptions in python.. this is a bit C programmery, probs

