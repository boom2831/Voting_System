from fastapi import FastAPI, Request, Form, HTTPException # type: ignore
from fastapi.responses import HTMLResponse, RedirectResponse # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
import os
import mysql.connector # type: ignore
from mysql.connector import Error # type: ignore
import bcrypt # type: ignore
import random
import logging
import pymysql # type: ignore
from pydantic import BaseModel # type: ignore

logging.basicConfig(level=logging.INFO)

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

class VoteRequest(BaseModel):
    candidate_id: int

def voter_id_generate():
    voter_id=''
    for _ in range(6):
        random_digits = random.randint(0, 9)
        voter_id+=str(random_digits)
    voter_id = "UTC"+voter_id
    return voter_id

def db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="Boom2004",
        database="voting",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/voterlogin.html", response_class=HTMLResponse)
async def read_voterlogin(request: Request):
    return templates.TemplateResponse("voterlogin.html", {"request": request})

@app.post("/voter_login", response_class=HTMLResponse)
async def handle_voter_login(request: Request, voterId: str = Form(...), voterName: str = Form(...)):
    logging.info(f"Request method: {request.method}")
    
    connection = db_connection()
    cursor = connection.cursor()
    
    try:
        query = "SELECT * FROM voters WHERE Voter_id = %s AND Full_name = %s"
        cursor.execute(query, (voterId, voterName))
        user = cursor.fetchone()
        
        if user:
            logging.info("Login successful")
            return RedirectResponse(url='/candidateDetails_v.html?success=true', status_code=303)
        else:
            logging.info("Login failed - Invalid credentials")
            return RedirectResponse(url="/voterlogin.html?success=false", status_code=303)
        
    except Error as e:
        logging.error(f"Database error: {e}")
        return RedirectResponse(url="/voterlogin.html?success=error", status_code=303)
    
    finally:
        cursor.close()
        connection.close()

@app.get('/candidateDetails_a.html', response_class=HTMLResponse)
async def read_candidate(request: Request):
    return templates.TemplateResponse("candidateDetails_a.html", {"request": request})

@app.get('/candidateDetails_v.html', response_class=HTMLResponse)
async def read_candidate(request: Request):
    return templates.TemplateResponse("candidateDetails_v.html", {"request": request})

    
@app.get("/templates/register.html", response_class=HTMLResponse)
async def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register_voter", response_class=HTMLResponse)
async def handle_register(request: Request, fullName: str = Form(...), address: str = Form(...), 
    dateOfBirth: str = Form(...), email: str = Form(...), phone: str = Form(...), 
  aadhaar: str = Form(...)):

    connection = db_connection()
    cursor = connection.cursor()
    
    try:
        query = "SELECT * FROM voters WHERE  Aadhaar = %s"
        cursor.execute(query, (aadhaar,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return RedirectResponse(url="/templates/register.html?status=exists", status_code=303)
        
        voter_id=voter_id_generate()
        query = "INSERT INTO voters (Full_name, Address, Date_of_birth, Email, Phone, Aadhaar, Voter_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (fullName, address, dateOfBirth, email, phone, aadhaar, voter_id))
        connection.commit()
        redirect_url = f"/voterlogin.html?status=success&voterid={voter_id}"
        return RedirectResponse(url=redirect_url, status_code=303)
    
    except Error as e:
        print(f"Error: {e}")
        return RedirectResponse(url="/register.html?status=error", status_code=303)
    
    finally:
        cursor.close()
        connection.close()

@app.get("/adminlogin.html", response_class = HTMLResponse)
async def read_adminlogin(request: Request):
    return templates.TemplateResponse('adminlogin.html', {"request":request})

@app.post('/admin_login', response_class = HTMLResponse)
async def handle_admin_login(request: Request, adminUsername: str = Form(...), adminPassword: str = Form(...)):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM Admins WHERE Username = %s AND Password = %s"
        cursor.execute(query, (adminUsername, adminPassword))
        admin = cursor.fetchone()

        if admin:
            return RedirectResponse(url='/candidateDetails_a.html?status=true', status_code=303)
        else:
            return RedirectResponse(url='/adminlogin.html?status=false', status_code=303)
    except Error as e:
        print(f"Error: {e}")
        return RedirectResponse(url='/adminlogin.html?status=error', status_code=303)
    finally:
        cursor.close()
        connection.close()

@app.get('/templates/update_v.html', response_class=HTMLResponse)
async def read_update_details(request:Request):
    return templates.TemplateResponse('update_v.html', {'request':request})

@app.post('/update_voter', response_class=HTMLResponse )
async def handle_update_details(request:Request, fullname: str = Form(...), aadhaarNo: str = Form(...), VoterId: str = Form(...), newAddress: str = Form(...), newPhone: str = Form(...), newEmail: str = Form(...)):
    connection=db_connection()
    cursor=connection.cursor()

    try:
        query = "SELECT * FROM voters WHERE Aadhaar = %s AND Voter_id = %s AND Full_name = %s"
        cursor.execute(query, (aadhaarNo, VoterId, fullname))
        voter = cursor.fetchone()
        if voter:
            query = "UPDATE voters SET Address = %s, Phone = %s, Email = %s WHERE Aadhaar = %s AND Voter_id = %s AND Full_name = %s"
            cursor.execute(query, (newAddress, newPhone, newEmail, aadhaarNo, VoterId, fullname))
            connection.commit()
            return RedirectResponse(url="/voterlogin.html?update=true", status_code=303)
        else:
            return RedirectResponse(url="/templates/register.html?update=false", status_code=303)
    
    except Error as e:
        print(f"Error: {e}")
        return RedirectResponse(url="/templates/update_v.html?update=error", status_code=304)


@app.get('/templates/remove_v.html', response_class=HTMLResponse)
async def read_remove_details(request:Request):
    return templates.TemplateResponse('remove_v.html', {'request':request})

@app.post('/remove_voter', response_class=HTMLResponse )
async def handle_update_details(request:Request, VoterId: str = Form(...), VoterName: str = Form(...)):
    connection=db_connection()
    cursor=connection.cursor()

    try:
        query = "SELECT * FROM voters WHERE Voter_id = %s AND Full_name = %s"
        cursor.execute(query, ( VoterId, VoterName))
        voter = cursor.fetchone()
        if voter:
            query = "DELETE FROM voters WHERE Voter_id = %s AND Full_name = %s"
            cursor.execute(query, (VoterId, VoterName))
            connection.commit()
            return RedirectResponse(url="/voterlogin.html?remove=true", status_code=303)
        else:
            return RedirectResponse(url="/templates/register.html?remove=false", status_code=303)
    
    except Error as e:
        print(f"Error: {e}")
        return RedirectResponse(url="/templates/remove_v.html?remove=error", status_code=304)

@app.get('/registerCandidate.html', response_class=HTMLResponse)
async def read_remove_details(request:Request):
    return templates.TemplateResponse('registerCandidate.html', {'request':request})

@app.post('/register_candidate', response_class=HTMLResponse)
async def handle_register_candidates(request: Request, Name: str = Form(...), Address: str = Form(...), Party: str = Form(...), Gender: str = Form(...), Dob: str = Form(...)):
    connection = db_connection()
    cursor = connection.cursor()
    
    try:
        query = "SELECT * FROM candidates WHERE  Date_of_birth = %s AND Full_name = %s"
        cursor.execute(query, (Dob, Name))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return RedirectResponse(url='/candidateDetails_a.html?regstat=exists', status_code=303)
        
        query = "INSERT INTO candidates (Full_name, Address, Date_of_birth, Gender, Party) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (Name, Address, Dob, Gender, Party))
        connection.commit()
        
        return RedirectResponse(url='/candidateDetails_a.html?regstat=success', status_code=303)
    
    except Error as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    
    finally:
        cursor.close()
        connection.close()

@app.post("/cast_vote", response_class=HTMLResponse)
async def cast_vote(request: Request, voterId: str = Form(...), candidate_id: int = Form(...)):
    connection = db_connection()
    cursor = connection.cursor()
    
    try:
        query = "SELECT * FROM voters WHERE Voter_id = %s"
        cursor.execute(query, (voterId,))
        voter = cursor.fetchone()
        
        if not voter:
            return HTMLResponse("Voter Not Registered!", status_code=304)
        
        query = "SELECT * FROM votes WHERE Voter_id = %s"
        cursor.execute(query, (voterId,))
        existing_vote = cursor.fetchone()
        
        if existing_vote:
            return HTMLResponse("Vote Already Casted!", status_code=303)
        
        insert_vote_query = "INSERT INTO votes (voter_id, candidate_id) VALUES (%s, %s)"
        cursor.execute(insert_vote_query, (voterId, candidate_id))
        connection.commit()
        
        return HTMLResponse("Vote Casted Successfully!", status_code=303)
    
    except Error as e:
        print(f"Database Error: {e}")
        return HTMLResponse("Internal Server Error!", status_code=303)
    
    finally:
        cursor.close()
        connection.close()

@app.get("/result.html", response_class=HTMLResponse)
async def show_results(request: Request):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        update_query = """
            UPDATE candidates
            SET Vote_count = (SELECT COUNT(*) FROM votes WHERE votes.candidate_id = candidates.id)
        """
        cursor.execute(update_query)
        connection.commit()
        query = "SELECT Full_name, Vote_count FROM candidates"
        cursor.execute(query)
        candidates = cursor.fetchall()
        print(f"Fetched Candidates: {candidates}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()

    return templates.TemplateResponse("result.html", {
        "request": request,
        "candidates": candidates,
        "total_votes": sum(candidate['Vote_count'] for candidate in candidates)
    })