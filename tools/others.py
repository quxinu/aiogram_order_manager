from configobj import ConfigObj


def get_adm_user():
    config = ConfigObj('config.ini')
    ADM_USER = [int(user.strip()) for user in config['Credentials']['ADM_USER']]
    return ADM_USER


def get_token():
    config = ConfigObj('config.ini')
    ADM_USER = [config['Credentials']['TOKEN']]
    return ADM_USER


def get_connect_db():
    config = ConfigObj('config.ini')
    DB_NAME = [config['DBInfo']['DB_NAME']]
    USER = [config['DBInfo']['USER']]
    PASSWORD = [config['DBInfo']['PASSWORD']]
    HOST = [config['DBInfo']['HOST']]
    PORT = [config['DBInfo']['PORT']]
    
    return DB_NAME, USER, PASSWORD, HOST, PORT