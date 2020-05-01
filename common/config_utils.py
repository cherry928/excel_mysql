import os
from configobj import ConfigObj

current_path = os.path.dirname(__file__)
cfg_path = os.path.join(current_path, '../conf/config.ini')

class ConfigUtils:
    def __init__(self, conf_path=cfg_path):
        self.__conf = ConfigObj(conf_path, encoding='utf-8')
    def read_ini(self, sec, option):
        value = self.__conf[sec][option]
        return value
    @property
    def get_mysql_user(self):
        value_user = self.read_ini('mysql_datahub', 'user')
        return value_user
    @property
    def get_mysql_password(self):
        value_password = self.read_ini('mysql_datahub', 'password')
        return value_password
    @property
    def get_mysql_host(self):
        value_host = self.read_ini('mysql_datahub', 'host')
        return value_host
    @property
    def get_mysql_database(self):
        value_database = self.read_ini('mysql_datahub', 'database')
        return value_database
    @property
    def get_excel_path(self):
        value_excel_path = self.read_ini('data', 'excel_path')
        return value_excel_path
    @property
    def get_log_path(self):
        value_loh_path = self.read_ini('data','log_path')
        return value_loh_path
config = ConfigUtils()
if __name__=='__main__':
    config_u = ConfigUtils()
    print(config_u.get_excel_path)