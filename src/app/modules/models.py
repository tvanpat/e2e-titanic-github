import pickle
import os
from configparser import ConfigParser
from datetime import datetime

from modules.data_pre import gender_data_transform
from modules.data_pre import fare_transform
from modules.data_pre import embarked_transform
from modules.data_pre import age_transform

import uuid

config = ConfigParser()

path = os.getcwd()

if path == '/usr/src':
    with open(os.path.join(os.getcwd(), '/app/config.cfg'), 'r') as configfile:
        config.readfp(configfile)
    baseline_model_name = config.get('baseline', 'baseline_model_name')
    baseline_model_filename = config.get('baseline', 'baseline_model_file_loc_api')
    prod_model_name = config.get('production', 'prod_model_name')
    prod_model_filename = config.get('production', 'prod_model_file_loc_api')
    
else:
    with open('/home/jovyan/work/src/app/config.cfg','r') as configfile:       
        config.readfp(configfile)
    baseline_model_name = config.get('baseline', 'baseline_model_name')
    baseline_model_filename = config.get('baseline', 'baseline_model_file_loc_notebook')
    prod_model_name = config.get('production', 'prod_model_name')
    prod_model_filename = config.get('production', 'prod_model_file_loc_notebook')

baseline_model = pickle.load(open(baseline_model_filename, 'rb'))
prod_model = pickle.load(open(prod_model_filename, 'rb'))


def prediction_data_transform(status):
    pred_dict = {1: 'Survived', 0: 'Did Not Survive'}
    return (pred_dict.get(status))


def pro_model_pred(titanicpassinfo):
    gender = gender_data_transform(titanicpassinfo.sex)
    fare = fare_transform(titanicpassinfo.fare)
    embarked = embarked_transform(titanicpassinfo.embarked)
    age = age_transform(titanicpassinfo.age,
                        titanicpassinfo.pclass,
                        gender,
                        titanicpassinfo.sibsp,
                        titanicpassinfo.parch,
                        fare,
                        embarked)
    prod_data_dict = {'pclass': titanicpassinfo.pclass,
                       'gender': gender,
                       'sibsp': titanicpassinfo.sibsp,
                       'parch': titanicpassinfo.parch,
                       'fare' : fare,
                       'embarked' : embarked,
                       'age' : age}
    prod_data_list = [*prod_data_dict.values()]
    prod_pred_survive = prod_model.predict([prod_data_list])[0].tolist()
    prod_prediction_word = prediction_data_transform(prod_pred_survive)
    prod_results = {'model_name': prod_model_name,
                    'model_data_trans': prod_data_dict,
                    'pred_survive': prod_pred_survive,
                    'pred_word': prod_prediction_word}
    return prod_results
    
def base_model_pred(titanicpassinfo):
    gender = gender_data_transform(titanicpassinfo.sex)
    fare = fare_transform(titanicpassinfo.fare)
    embarked = embarked_transform(titanicpassinfo.embarked)
    age = age_transform(titanicpassinfo.age,
                        titanicpassinfo.pclass,
                        gender,
                        titanicpassinfo.sibsp,
                        titanicpassinfo.parch,
                        fare,
                        embarked)
    base_data_dict = {'pclass': titanicpassinfo.pclass,
                       'gender': gender,
                       'sibsp': titanicpassinfo.sibsp,
                       'parch': titanicpassinfo.parch,
                       'fare' : fare,
                       'embarked' : embarked,
                       'age' : age}
    base_data_list = [*base_data_dict.values()]
    base_pred_survive = prod_model.predict([base_data_list])[0].tolist()
    base_prediction_word = prediction_data_transform(base_pred_survive)
    base_results = {'model_name': baseline_model_name,
                    'model_data_trans': base_data_dict,
                    'pred_survive': base_pred_survive,
                    'pred_word': base_prediction_word}
    return base_results



def titanic_prediction(titanicpassinfo):
    if titanicpassinfo.passid == 'empty':
        passid = str(uuid.uuid4())
    else:
        passid = titanicpassinfo.passid
    base_results = base_model_pred(titanicpassinfo)
    prod_results = pro_model_pred(titanicpassinfo)
    
    return ({'dtg_gmt': datetime.now(), 
             'passid': passid,
             'input_data' : {'pclass': titanicpassinfo.pclass,
                             'sex': titanicpassinfo.sex,
                             'sibsp': titanicpassinfo.sibsp,
                             'parch': titanicpassinfo.parch,
                             'fare': titanicpassinfo.fare,
                             'embarked': titanicpassinfo.embarked,
                             'age': titanicpassinfo.age},
             'baseline_results': base_results,
             'prod_results': prod_results})