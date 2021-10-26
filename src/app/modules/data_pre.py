import numpy as np
from random import randint
import pickle
import yaml

# read in imputation models
try:
    age_lin_model_filename = '/app/assets/models/data_preprocessing_models/age_lin_model_11_30_2020.sav'
    age_lin_model = pickle.load(open(age_lin_model_filename, 'rb'))
    config_filename = '/app/assets/config.yaml'
    config_yaml = yaml.safe_load(open(config_filename))

except:
    age_lin_model_filename = '/home/jovyan/work/src/app/assets/models/data_preprocessing_models/age_lin_model_11_30_2020.sav'
    age_lin_model = pickle.load(open(age_lin_model_filename, 'rb'))
    config_filename = '/home/jovyan/work/src/app/assets/config.yaml'
    config_yaml = yaml.safe_load(open(config_filename))


def rand_age(cell_value, age_min, age_max):
    if np.isnan(cell_value) is True:
        return randint(age_min, age_max)
    else:
        return cell_value


def lin_model_age(data):
    if np.isnan(data['Age']) is True:
        xnew = [[data['Pclass'], data['Sex'], data['SibSp'], data['Parch'], data['Fare'], data['Embarked']]]
        pred_age = age_lin_model.predict(xnew)[0]
        return pred_age

    else:
        return data['Age']


def sto_lin_model_age(data, std_error):
    if np.isnan(data['Age']) is True:
        xnew = [[data['Pclass'], data['Sex'], data['SibSp'],data['Parch'], data['Fare'], data['Embarked']]]
        pred_age = age_lin_model.predict(xnew)[0]
        sto_age = round(np.random.normal(loc=pred_age, scale=std_error))
        return(sto_age)

    else:
        return data['Age']


def most_common(cell_value, mf_value):
    if np.isnan(cell_value) is True:
        return mf_value
    else:
        return cell_value


def gender_data_transform(gender):
    gender_dict = {'male': 1, 'female': 0}
    return (gender_dict.get(gender))


def fare_transform(fare):
    if fare == -1:
        new_fare = config_yaml['most_common_fare']
    else:
        new_fare = fare
    return new_fare


def embarked_transform(embark):
    if embark == 'NA':
        new_embark = config_yaml['most_common_embarked']
    else:
        embark_code = {'S': 1, 'C': 2, 'Q': 3}
        new_embark = embark_code.get(embark)
    return new_embark


def age_transform(age, pclass, sex, sibsp, parch, fare, embarked):
    if age == -1:
        xnew = [[pclass, sex, sibsp, parch, fare, embarked]]
        new_age = age_lin_model.predict(xnew)[0]
    else:
        new_age = age
    return new_age
