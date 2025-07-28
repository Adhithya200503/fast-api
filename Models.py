from pydantic import BaseModel

class Student(BaseModel):
    name:str
    roll_no:int
    phone:int
    location:str
    
    
    