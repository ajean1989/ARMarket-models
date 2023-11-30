# Mongo DB

adresse_mongo = "5.196.7.246"
port_mongo = 27017
user_mongo = "root"
pass_mongo = "MongoMongo_O_O"


# maria DB

adresse_maria = "5.196.7.246"
port_maria = 3306
user_maria = "root"
pass_maria = "MariAMaria_A_A_A"
base_maria = "ARMarket"

SQLALCHEMY_DATABASE_URL = f"mariadb+mariadbconnector://{user_maria}:{pass_maria}@{adresse_maria}/{base_maria}"
