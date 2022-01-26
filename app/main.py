from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
 
app = FastAPI()
 
 
class inputs(BaseModel):
    test_str:str
         
@app.get("/")
def read_root():
    return {"Word": "Replace"}
       
@app.get('/show_data/{test_str}')
def show_data(test_str):
    # initializing string 
    #test_str = str("We really like the new security features of Google Oracle Microsoft Deloitte Amazon  Cloud")
    res = str
    # printing original string 
    print("The original string is : " + str(test_str))
    
    # Using nested replace()
    # Replace multiple characters at once
    res = test_str.replace('Google', 'Google©').replace('Oracle', 'Oracle©').replace('Microsoft', 'Microsoft©').replace('Deloitte', 'Deloitte©').replace('Amazon', 'Amazon©')
    
    # printing result 
    print("The string after replacement of positions : " + res)
    return res