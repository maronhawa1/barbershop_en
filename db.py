from pymongo import MongoClient

# הכנס כאן את ה-URI שלך ממונגו אטלס או מקומי
MONGO_URI = "mongodb+srv://maronhawa:maron12345@barbershop-db.a7xwgix.mongodb.net/?retryWrites=true&w=majority&appName=barbershop-db"

client = MongoClient(MONGO_URI)
db = client["barbershop_db"]

appointments = db["appointments"]
services = db["services"]
users = db["users"]
