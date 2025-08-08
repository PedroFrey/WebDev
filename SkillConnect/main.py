import nest_asyncio
import uvicorn
from fastapi import FastAPI, Form, Request,  Depends
from fastapi.responses import HTMLResponse, RedirectResponse , JSONResponse, ORJSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

# Apply asyncio patch for Colab
nest_asyncio.apply()

# Initialize FastAPI
app = FastAPI(default_response_class = ORJSONResponse)
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
templates = Jinja2Templates(directory="/templates")

# Function to fetch user from the database
def get_user(email: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email, pass FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user  # Returns (name, pass) tuple or None

# Function to add user to the database
def add_user(name, email, password):
    # Conectar ao banco de dados
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Inserir usuário no banco de dados
    cursor.execute('INSERT INTO users (name, email, pass) VALUES (?, ?, ?)',
                    (name, email, password))
    conn.commit()  # Confirmar a transação
    conn.close()   # Fechar a conexão

# Function to add user to the database
def add_appointment(date, time, latitude, longitude):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO appointment (date, time, latitude, longitude) VALUES (?, ?, ?, ?)',
                   (date, time, latitude, longitude))
    conn.commit()
    conn.close()

# Define templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("/landing.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("/register.html", {"request": request})

@app.post("/register")
async def register(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Adicionar usuário ao banco
    add_user(name, email, password)
    # Retornar mensagem de sucesso
    return {"message": "User registered successfully", "name": name, "email": email}

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("/login.html", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = get_user(email)
    if user and user[1] == password:  # user[1] is the 'pass' column
        request.session["user"] = user[0]  # Store name in session
        return RedirectResponse(url="/dashboard.html", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})



@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("/dashboard.html", {"request": request, "user": user})

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.get("/underdevelopment", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("/underdevelopment.html", {"request": request})

# Endpoint to submit an appointment
@app.post("/submit_appointment")
async def submit_appointment(request: Request,
    date: str = Form(...),
    time: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...)):

    # Adicionar usuário ao banco
    add_appointment(date,time,latitude,longitude)
    # Retornar mensagem de sucesso
    return {"message": "Appointment registered successfully", "date": date, "time": time}

    return JSONResponse(content={"message": "Appointment saved successfully!"})