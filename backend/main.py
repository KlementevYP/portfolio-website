from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import engine, Blog, Person, About, Resume, Education, Experience, Skill, PortfolioProjects
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, date
from babel.dates import format_date

app = FastAPI()
templates = Jinja2Templates(directory='../templates/')
app.mount('/static', StaticFiles(directory='../assets'), name='static')

def format_date_ru(value: date, format: str = "long"):
    """Форматирует дату на русском"""
    return format_date(value, format=format, locale='ru_RU')

templates.env.filters['date'] = format_date_ru  # Регистрация фильтра


@app.get('/')
async def read_index(request: Request):
    with Session(engine) as session:
        person = session.query(Person).first()
        if person is None:
            return templates.TemplateResponse("error.html", {"request": request, "message": "person not found"}, status_code=404)
        about = session.query(About).all()
        blogs = session.query(Blog).all()
        resume = session.query(Resume).all()
        education = []
        experience = []
        skills = []
        for res in resume:
            education.extend(res.educations)
            experience.extend(res.experiences)
            skills.extend(res.skills)
        portfolio_projects = session.query(PortfolioProjects).all()
        blog = session.query(Blog).all()

    context = {
        'request': request,
        'person': person,
        'about': about,
        'blogs': blogs,
        'resume': resume,
        'education': education,
        'experience': experience,
        'skills': skills,
        'portfolio_projects': portfolio_projects,
        'blog': blog,
    }

    return templates.TemplateResponse("index.html", context)

@app.post("/contact")
async def handle_contact_form(
    fullname: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # Настройки SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "klementev712@gmail.com"
    smtp_password = "noxj kwcw jeby lxnc"

    # Создание сообщения
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = "klementev712@gmail.com"  # Ваш email
    msg["Subject"] = "Новое сообщение с сайта-портфолио"

    body = f"Имя: {fullname}\nEmail: {email}\nСообщение:\n{message}"
    msg.attach(MIMEText(body, "plain"))

    # Отправка письма
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return RedirectResponse(url="/", status_code=303)

@app.get('/edit')
async def edit_page(request: Request):
    return templates.TemplateResponse("edit_info.html", {"request": request})

# @app.get("/create-person", response_class=HTMLResponse)
# async def create_person_form(request: Request):
#     return templates.TemplateResponse("create_person.html", {"request": request})

# @app.post("/create-person")
# async def create_person(
#     name: str = Form(...),
#     age: int = Form(...),
#     profession: str = Form(...),
#     location: str = Form(...),
#     email: str = Form(...),
#     phone: str = Form(...),
#     birth_date: str = Form(...),
#     login: str = Form(...),
#     password: str = Form(...),
# ):
#     # Хешируем пароль
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#     # Преобразуем строку даты в объект date
#     birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()

#     with Session(engine) as session:
#         new_person = Person(
#             name=name,
#             age=age,
#             profession=profession,
#             location=location,
#             email=email,
#             phone=phone,
#             birth_date=birth_date_obj,  # Используем объект date
#             login=login,
#             password=hashed_password.decode('utf-8')
#         )
#         session.add(new_person)
#         session.commit()
#         session.refresh(new_person)

#     return {"message": "Person created successfully"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='192.168.0.200', port=8000)