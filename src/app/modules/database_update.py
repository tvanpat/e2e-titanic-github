import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
mongo_client = os.getenv('mongo_client')
mongodb = os.getenv('mongodb')
mongocol = os.getenv('mongocol')


def mongo_single_add(mongodict):
    myclient = pymongo.MongoClient(f'mongodb:{mongo_client}')
    mydb = myclient[mongodb]
    mycol = mydb[mongocol]
    mycol.insert_one(mongodict)
    myclient.close()

def mongo_multi_add(mongolist):
    myclient = pymongo.MongoClient(f'mongodb:{mongo_client}')
    mydb = myclient[mongodb]
    mycol = mydb[mongocol]
    mycol.insert_many(mongolist)
    myclient.close()