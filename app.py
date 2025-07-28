from fastapi import FastAPI
from Models import Student
from momgodb import collection
from fastapi import HTTPException

app = FastAPI()

def serialize(student):
    serialized = {
        "id":str(student["_id"]),
        "name":student["name"],
        "roll_no":student["roll_no"],
        "phone":student["phone"],
        "location":student["location"]
        
    }
    return serialized

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/student-info")
def student_info():
    return {"message":"this is student info page"}

@app.post("/student")
async def add_student(student:Student):
    existing_student = await collection.find_one({"roll_no":student.roll_no})
    if existing_student:
        raise HTTPException(status_code=400, detail="Student already exists")
    result = await collection.insert_one(student.model_dump())
    new_student = await collection.find_one({"_id": result.inserted_id})
    
    return serialize(new_student)
    
@app.get("/students")
async def get_students():
    student_cursor = collection.find()
    students = [] 
    async for student in student_cursor:
        students.append(serialize(student))
    return students


@app.get("/students/{roll_no}")
async def find_student(roll_no:int):
    student = await collection.find_one({"roll_no":roll_no})
    if not student:
        raise HTTPException(status_code=400 , detail="student not found , enter a valid roll no ")
    
    return serialize(student)


@app.delete("/student/{roll_no}")
async def find_student_and_delete(roll_no:int):
    student = await collection.find_one({"roll_no":roll_no})
    if not student:
        raise HTTPException(status_code=404 , detail="User not found (unable to delete)")
    await collection.delete_one({"_id":student["_id"]})
    
    return serialize(student)
    
    

@app.put("/student/{roll_no}")
async def update_student(roll_no: int, updated_data: Student):
    student = await collection.find_one({"roll_no": roll_no})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if updated_data.roll_no != roll_no:
        raise HTTPException(
            status_code=400,
            detail="Roll number cannot be changed"
        )

    await collection.update_one(
        {"roll_no": roll_no},
        {"$set": updated_data.model_dump()}
    )
    updated_student = await collection.find_one({"roll_no": roll_no})
    return serialize(updated_student)