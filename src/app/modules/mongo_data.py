import pymongo
import os
from dotenv import load_dotenv

dotpath = '/home/jovyan/work/src/app/modules/.env'
load_dotenv(dotenv_path = dotpath, verbose=True)
mongo_client = os.getenv('mongo_client')
mongodb = os.getenv('mongodb')
mongocol = os.getenv('mongocol')

def mongo_access(func):
    def wrapper(*args, **kwargs):
        myclient = pymongo.MongoClient(f'mongodb:{mongo_client}')
        mydb = myclient[mongodb]
        mycol = mydb[mongocol]
        data = func(mycol, *args)
        myclient.close()
        return data
    return wrapper

@mongo_access
def input_datadf(mycol):
    temp_data = []
    for x in mycol.find():
        temp_d = {'passid': x.get('passid'), 'dtg_gmt': x.get('dtg_gmt'), 
              'input_pclass' : x.get('input_data').get('pclass'), 'input_sex' : x.get('input_data').get('sex'), 'input_sibsp' : x.get('input_data').get('sibsp'),
             'input_parch' : x.get('input_data').get('parch'), 'input_fare' : x.get('input_data').get('fare'), 'input_embarked': x.get('input_data').get('embarked'), 
              'input_age': x.get('input_data').get('age')}
        temp_data.append(temp_d)
    return temp_data

@mongo_access
def model_datadf(mycol, model):
    temp_data= []
    for x in mycol.find():
        temp_d = {'passid': x.get('passid'), 'dtg_gmt': x.get('dtg_gmt'), 'model_name' : x.get(model).get('model_name'),
                  'pred_survive': x.get(model).get('pred_survive'), 'pred_word': x.get(model).get('pred_word'),
                 'trans_pclass' : x.get(model).get('model_data_trans').get('pclass'), 'sex': x.get(model).get('model_data_trans').get('gender'),
                 'sibsp': x.get(model).get('model_data_trans').get('sibsp'), 'parch': x.get(model).get('model_data_trans').get('parch'),
                 'fare' : x.get(model).get('model_data_trans').get('fare'), 'embarked': x.get(model).get('model_data_trans').get('embarked'),
                 'age': x.get(model).get('model_data_trans').get('age')}
        temp_data.append(temp_d)
    return temp_data