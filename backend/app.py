from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Any
import sqlite3
import os
import secrets

DB_PATH = os.path.join(os.path.dirname(__file__), "backend.db")

app = FastAPI(title="Learning UI Backend")

# Pydantic models
class AuthRequest(BaseModel):
    email: str
    role: Optional[str] = None
    password: Optional[str] = None

class AuthResponse(BaseModel):
    authToken: str

class UserDetailsRequest(BaseModel):
    role: str
    name: Optional[str] = None
    email: Optional[str] = None

class TrainingCreate(BaseModel):
    title: str
    category: Optional[str] = None
    duration: Optional[str] = None

class Training(BaseModel):
    id: int
    title: str
    category: Optional[str]
    duration: Optional[str]

class MyTrainingsRequest(BaseModel):
    email: str

class QuizGenerateRequest(BaseModel):
    course_id: int
    text: Optional[str] = None

# DB helpers
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if os.path.exists(DB_PATH):
        return
    conn = get_conn()
    cur = conn.cursor()
    # users: id, name, email, role, department, status
    cur.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            role TEXT,
            department TEXT,
            status TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE trainings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            duration TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE user_trainings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            training_id INTEGER,
            progress INTEGER DEFAULT 0
        )
    ''')
    cur.execute('''
        CREATE TABLE tokens (
            token TEXT PRIMARY KEY,
            email TEXT,
            role TEXT
        )
    ''')
    # seed users
    users = [
        ("Alice Turner","alice@company.com","trainee","Engineering","Active"),
        ("Bob Martinez","bob@company.com","trainee","Marketing","Active"),
        ("Carol White","carol@company.com","trainee","Sales","Active"),
        ("Daniel Kim","daniel@company.com","trainee","Product","Inactive"),
        ("Eva Chen","eva@company.com","trainee","Engineering","Active"),
        ("Frank Nguyen","frank@company.com","trainee","HR","Active"),
        ("Sarah Johnson","sarah@company.com","trainer",NULL,"Active"),
        ("Michael Chen","michael@company.com","trainer",NULL,"Active"),
        ("Emily Rodriguez","emily@company.com","trainer",NULL,"Active"),
        ("David Park","david@company.com","trainer",NULL,"Active"),
        ("Michael Scott","michael.scott@company.com","manager",NULL,"Active")
    ]
    cur.executemany('INSERT INTO users (name,email,role,department,status) VALUES (?,?,?,?,?)', users)
    # seed trainings
    trainings = [
        ("AI Fundamentals","AI/ML","8 hours"),
        ("Machine Learning Basics","AI/ML","12 hours"),
        ("Python for Data Science","Programming","10 hours"),
        ("Advanced ML Techniques","AI/ML","15 hours"),
        ("Data Visualization","Analytics","6 hours"),
        ("Deep Learning Fundamentals","AI/ML","20 hours")
    ]
    cur.executemany('INSERT INTO trainings (title,category,duration) VALUES (?,?,?)', trainings)
    # sample user trainings
    user_trainings = [
        ("alice@company.com", 1, 30),
        ("bob@company.com", 2, 100),
        ("eva@company.com", 3, 50),
        ("sarah@company.com", 1, 0)
    ]
    cur.executemany('INSERT INTO user_trainings (user_email,training_id,progress) VALUES (?,?,?)', user_trainings)
    conn.commit()
    conn.close()

# initialize DB on import
init_db()

# Routes
@app.post('/auth/token', response_model=AuthResponse)
def auth_token(req: AuthRequest):
    """Return a simple auth token for any existing user. This is a demo token generator (not JWT)."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT email,role,name FROM users WHERE email = ?', (req.email,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = secrets.token_urlsafe(32)
    cur.execute('INSERT INTO tokens(token,email,role) VALUES (?,?,?)', (token, row['email'], row['role']))
    conn.commit()
    conn.close()
    return {"authToken": token}

@app.post('/user/details')
def user_details(req: UserDetailsRequest):
    """Return user details for the provided role/email/name. If manager role provided without email, return manager's info."""
    conn = get_conn()
    cur = conn.cursor()
    if req.email:
        cur.execute('SELECT name,email,role,department,status FROM users WHERE email = ?', (req.email,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail='User not found')
        return dict(row)
    # fallback: search by role/name
    if req.name:
        cur.execute('SELECT name,email,role,department,status FROM users WHERE name = ?', (req.name,))
        row = cur.fetchone()
        if row:
            return dict(row)
    if req.role:
        cur.execute('SELECT name,email,role,department,status FROM users WHERE role = ?', (req.role,))
        rows = cur.fetchall()
        if rows:
            # if multiple, return list
            return [dict(r) for r in rows]
    raise HTTPException(status_code=400, detail='Provide email, name or role')

@app.post('/users/trainees')
def list_trainees():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,department,status FROM users WHERE role = 'trainee'")
    rows = cur.fetchall()
    resp = []
    for r in rows:
        # compute dummy enrolled/completed/lastActive/trainer fields for compatibility with example
        resp.append({
            "id": r['id'],
            "name": r['name'],
            "email": r['email'],
            "department": r['department'],
            "enrolledCourses": 1,
            "completedCourses": 0,
            "lastActive": "Recently",
            "status": r['status'],
            "trainer": None
        })
    return resp

@app.post('/users/trainers')
def list_trainers():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email FROM users WHERE role = 'trainer'")
    rows = cur.fetchall()
    return [{"id": r['id'], "name": r['name']} for r in rows]

@app.get('/trainings', response_model=List[Training])
def get_trainings():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id,title,category,duration FROM trainings')
    rows = cur.fetchall()
    return [Training(id=r['id'], title=r['title'], category=r['category'], duration=r['duration']) for r in rows]

@app.post('/trainings')
def create_training(req: TrainingCreate):
    # for demo, accept role via query param? Here we accept any creation but in realistic app check token/role
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO trainings (title,category,duration) VALUES (?,?,?)', (req.title, req.category, req.duration))
    conn.commit()
    tid = cur.lastrowid
    cur.execute('SELECT id,title,category,duration FROM trainings WHERE id = ?', (tid,))
    row = cur.fetchone()
    return dict(row)

@app.post('/my/trainings')
def my_trainings(req: MyTrainingsRequest):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
        SELECT t.id,t.title,t.category,t.duration,ut.progress
        FROM trainings t JOIN user_trainings ut ON t.id = ut.training_id
        WHERE ut.user_email = ?
    ''', (req.email,))
    rows = cur.fetchall()
    if not rows:
        return []
    return [
        {"id": r['id'], "title": r['title'], "category": r['category'], "duration": r['duration'], "progress": r['progress']} for r in rows
    ]

@app.post('/quizzes/generate')
def generate_quiz(req: QuizGenerateRequest):
    # Return static example quiz items (from learning_ui_backend_routes.txt) as a prototype for trainer review.
    sample = [
      {
        "question": "Which of the following best describes supervised learning?",
        "options": ["Learning without labels", "Learning from labeled examples", "Learning purely by trial and error", "Learning by clustering similar points"],
        "correctAnswer": 1,
        "complexity": "moderate",
        "explanation": "Supervised learning trains on labeled input-output pairs to predict outputs for new inputs."
      },
      {
        "question": "What is the primary purpose of a validation set?",
        "options": ["To train the model weights", "To tune hyperparameters and detect overfitting", "To deploy the model to production", "To label the raw data"],
        "correctAnswer": 1,
        "complexity": "moderate",
        "explanation": "A validation set is held out from training to tune hyperparameters and gauge generalization."
      },
      {
        "question": "What does L2 regularization primarily help with?",
        "options": ["Speeding up data loading", "Reducing overfitting by penalizing large weights", "Increasing the model size", "Automatically labeling data"],
        "correctAnswer": 1,
        "complexity": "moderate",
        "explanation": "L2 adds a penalty on large weights, discouraging complexity and improving generalization."
      }
    ]
    return sample

# simple health check
@app.get('/ping')
def ping():
    return {"ping": "pong"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
