import pymysql
import yaml

class DBInterface:
    def __init__(self, testmode):
        login_dict = yaml.safe_load(open('{}login.yml'.format(testmode)))
        self.url = login_dict.get('mysql_url')
        self.user = login_dict.get('mysql_user')
        self.pw = login_dict.get('mysql_password')
        self.db = login_dict.get('mysql_db')
        self.string_len_max = 40
    def connect(self):
        self.mydb = pymysql.connect(self.url, self.user, self.pw, self.db)
        self.cursor = self.mydb.cursor()
    def set_table(self,table):
        self.cursor.execute('USE {}'.format(self.db))
        self.cursor.execute('SHOW TABLES')
        table_tup = (table,)
        tables_in_db = [c for c in self.cursor]
        if table_tup in tables_in_db:
            self.table = table
        else:
            raise ValueError("table {} does not exist in {}".format(table,self.db))
    def get_max_value(self, max_of):
        self.cursor.execute("select MAX({}) from {};".format(max_of,self.table))
        return self.cursor.fetchone()
    def __truncate_strings(self, schema_tup):
        truncated_tup = ()
        for value in schema_tup:
            if isinstance(value, str):
                truncated_tup = truncated_tup + (value[:self.string_len_max-1],)
            else:
                truncated_tup = truncated_tup + (value,)
        return truncated_tup
    def insert(self, values_tup):
        schema_tup =self. __truncate_strings(values_tup)
        try:
            self.cursor.execute("INSERT INTO {} VALUES {}".format(self.table, schema_tup))
            self.mydb.commit()
        except:
            self.mydb.rollback()
            raise 

