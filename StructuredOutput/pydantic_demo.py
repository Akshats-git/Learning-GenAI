from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Student(BaseModel):
    name: str = 'Akshat' # setting default value
    age: Optional[int] = None
    email: EmailStr
    cgpa: float = Field(gt=0, le=10, default=5,description="CGPA must be between 0 and 10")

new_student = {'name':'Akshat','email':'abc@gmail.com','cgpa':10.0}
student = Student(**new_student)

print(student) # throws error if name is not string

student_dict = dict(student)
student_json = student.model_dump_json()