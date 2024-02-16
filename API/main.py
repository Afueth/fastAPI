from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Pydantic model to define the expected request body schema
class LoginRequest(BaseModel):
    firstname: str
    secondname: str

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Ensure this matches the frontend's URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port=3306,
    database="db_sample"
)

# Endpoint to insert data using the LoginRequest model for automatic validation
@app.post("/insert/")
async def insert_text(login_request: LoginRequest):
    fname = login_request.firstname
    sname = login_request.secondname
    cursor = mydb.cursor()
    try:
        cursor.execute("INSERT INTO `tbl_name`(`firstname`, `secondname`) VALUES (%s, %s)", (fname, sname))
        mydb.commit()
        return {"message": "User inserted successfully"}
    except Exception as e:
        mydb.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        cursor.close()

