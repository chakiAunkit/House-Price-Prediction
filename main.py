from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import json
import pickle
import numpy as np
import warnings
warnings.filterwarnings("ignore") 

app=FastAPI()

origins = [
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

__locations = None
__data_columns = None
__model = None

def predict_price(location, sqft, bath, bhk):

    try:
        loc_idx = __data_columns.index(location.lower())
    except:
        loc_idx = -1
    
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_idx >= 0:
        x[loc_idx] = 1
        
    return round(__model.predict([x])[0], 2)

def get_location_names():
    return __locations

def load():
    global __data_columns
    global __locations
    global __model

    with open('columns.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    with open('home_price_model.pickle', 'rb') as f:
        __model = pickle.load(f)

# if __name__ == '__main__':
#     load()
#     #print(get_location_names())
#     print(predict_price('1st Phase JP Nagar', 2000, 5, 4))

class PredictionModel(BaseModel) :
    location : str
    sqfoot : int
    bath : int
    bed : int


@app.get('/')
def init() :
    load()
    return {"msg": "Load Successful"}

@app.post("/predict")
def get_prediction(data : PredictionModel ) : 
    load()
    return predict_price(data.location, data.sqfoot, data.bath, data.bed)

