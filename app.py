from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import mysql.connector
from mysql.connector import Error
import bcrypt  # For hashing passwords

# Initialize FastAPI app
app = FastAPI()

# Get the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static files directory (for CSS, JavaScript, images etc.)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Set up templates directory
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Database connection function
def get_db_connection():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="127.0.0.1",       # Change this to your MySQL host
            user="root",            # Your MySQL username
            password="aniketh@2005",    # Your MySQL password
            database="voting_system"  # Your database name
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

# Route for the home page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Render the index.html template
    return templates.TemplateResponse("index.html", {"request": request})

# Route for the voter login page
@app.get("/voterlogin.html", response_class=HTMLResponse)
async def voter_login_page(request: Request):
    # Render the voterlogin.html template
    return templates.TemplateResponse("voterlogin.html", {"request": request})

# Route for the register page
@app.get("/templates/register.html", response_class=HTMLResponse)
async def register_page(request: Request):
    # Render the register.html template
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/adminlogin.html", response_class=HTMLResponse)
async def read_adminlogin(request: Request):
    return templates.TemplateResponse("adminlogin.html", {"request":request})


@app.post("/voterlogin.html", response_class=HTMLResponse)
async def handle_voter_login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Query the database to check if the user exists
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):  # Check if password matches (hashed password)
            # Successful login, redirect to voter dashboard
            return HTMLResponse(content="Login Successfull", status_code=401), RedirectResponse(url="/voter_dashboard", status_code=303)
        else:
            # If login fails, return an error message
            return HTMLResponse(content="Invalid credentials", status_code=401)
    
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# POST route for handling voter registration
@app.post("/templates/register.html", response_class=HTMLResponse)
async def handle_register(request: Request, fullName: str = Form(...), address: str = Form(...), 
    dateOfBirth: str = Form(...), email: str = Form(...), phone: str = Form(...), 
  aadhaar: str = Form(...), username: str = Form(...), password: str = Form(...)):
    
    # Hash the password before storing it in the database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Check if the username already exists in the database
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            # If the username already exists, return an error message
            return HTMLResponse(content="Username already taken, please choose another.", status_code=400)
        
        # Insert the new user into the database
        query = """
            INSERT INTO userss (username, password, full_name, address, date_of_birth, email, phone, aadhaar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (username, hashed_password.decode('utf-8'), fullName, address, dateOfBirth, email, phone, aadhaar))
        connection.commit()
        
        # Redirect to the login page after successful registration
        return RedirectResponse(url="/voterlogin", status_code=303)
    
    except Error as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database error during registration")
    
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# Dummy route for the voter dashboard page (after successful login)
@app.get("/voter_dashboard", response_class=HTMLResponse)
async def voter_dashboard(request: Request):
    return templates.TemplateResponse("voter_dashboard.html", {"request": request})

# Static files handler (CSS, JS, images, etc.)
@app.get("/static/{path_name}")
async def static_files(path_name: str):
    return StaticFiles(directory="static", html=True)