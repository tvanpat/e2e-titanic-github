from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

from modules.database_update import mongo_single_add, mongo_multi_add
from modules.models import titanic_prediction



app = FastAPI()


class TitanicPassInfo(BaseModel):
    pclass: int
    sex: str
    sibsp: int
    parch: int
    fare: float = -1
    embarked: str = 'Q'
    age: float = -1
    passid: str = 'empty'


class MultiPassInfo(BaseModel):
    passengers: list


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/singletitanicpred/")
def predict_single_titanic(titanicpassinfo: TitanicPassInfo):
    results = titanic_prediction(titanicpassinfo)
    
    mongo_single_add(results)
    return{"passid": titanicpassinfo.passid,
           "prod_prediciton_binary": results.get('prod_results', {}).get('pred_survive'),
           "prod_prediction_word": results.get('prod_results', {}).get('pred_word')}


@app.post("/multititanicpred2/")
def predict_mulit_titanic2(titanicpassinfos: List[TitanicPassInfo]):
    api_results = []
    mongo_list = []
    for passinfo in titanicpassinfos:
        single_result = titanic_prediction(passinfo)
        temp_result = {"passid": passinfo.passid,
           "prod_prediciton_binary": single_result.get('prod_results', {}).get('pred_survive'),
           "prod_prediction_word": single_result.get('prod_results', {}).get('pred_word')}
        mongo_list.append(single_result)
        api_results.append(temp_result)

    mongo_multi_add(mongo_list)

    return{'results': api_results}
