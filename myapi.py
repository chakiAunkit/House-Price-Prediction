from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
import json
import pickle
import numpy as np
import warnings
warnings.filterwarnings("ignore") 

app = FastAPI()

student = {
    1: {'name' : 'Agni', 
        'age' : 22, 
        'hobby' : 'dancing'
    }
}

class Student(BaseModel) :
    name : str
    age : int
    hobby : str

class UpdateStudent(BaseModel) : 
    name : Optional[str] = None
    age : Optional[int] = None
    hobby : Optional[str] = None

@app.get("/")
def index():
    return {"name" : "Agni"}

@app.get("/students")
def getAllStudents():
    return student

@app.get("/student/{student_id}")
def getstudent(student_id : int = Path(None, description = 'The id of student to get', gt=0)) :
    return (student.get(student_id))

@app.get ("/student-name")
def getstudentname(*, name : Optional[str] = None, test : int) :
    for student_id in student:
        if student[student_id]["name"] == name :
            return student[student_id]
    return {"msg" : "No student"}      
         
@app.post("/student/{student_id}")
def create_student(student_id : int, studentinfo : Student) :
    if student_id in student :
        return {"error" : "Already Exists"}
    student[student_id] = studentinfo
    return student.get(student_id)

@app.put("/update-student/{student_id}")
def update_student(student_id : int, studentinfo : UpdateStudent) :
    if student_id not in student :
        return {"error" : "Doesn't Exist"}
    m=studentinfo.dict();
    for attr in m.keys():
        student[student_id][attr] = m[attr]
    return student.get(student_id)










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

@app.get("/predict")
def get_prediction(data : PredictionModel ) : 
    load()
    return predict_price(data.location, data.sqfoot, data.bath, data.bed)

