import configparser


def connect_parameter(config_path = ".", host = None, port = None, name = None, username = None, password = None):
	config = configparser.ConfigParser()
	config.read(config_path + '/datasource.conf')
	database = config["database"]

	Host = database.get("Host", "localhost")
	Port = database.get("Port", "5432")
	Name = database.get("Name", "postgres")
	Username = database.get("Username", "postgres")
	Password = database.get("Password", "")

	if host != None: Host = host
	if port != None: Port = port
	if name != None: Name = name
	if username != None: Username = username
	if password != None: Password = password

	return f"host='{Host}' port={Port} dbname={Name} user={Username} password='{Password}'"
