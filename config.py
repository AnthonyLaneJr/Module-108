import certifi
import pymongo



con_str = "mongodb+srv://TonyLane2017:nCfJDyOG36BvzcBf@cluster0.4yyhi.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("WeightTrainingGoods")