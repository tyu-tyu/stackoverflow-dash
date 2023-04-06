def db_config():
	db_config_info = {
		'user':'edgehill',
		'password':'Edgehill2023',
		'host':'127.0.0.1', #127.0.0.1 Local | mariadb docker
		'port':5505,
		'database': 'dashboard_data'
	}
	return db_config_info

def redis_config():
	redis_config_info = {
		'host':'127.0.0.1', #127.0.0.1 Local | redis docker
		'port':6379, 
		'charset':'utf-8',
		'decode_responses':True
	}
	return redis_config_info