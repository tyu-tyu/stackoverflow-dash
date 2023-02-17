def db_config():
	db_config_info = {
		'user':'tyu',
		'password':'tyudb99',
		'host':'127.0.0.1', #127.0.0.1 Local mariadb docker
		'port':5505, #5505 Local 3306 Docker
		'database': 'dashboard_data'
	}
	return db_config_info