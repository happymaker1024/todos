from fastapi import FastAPI, Form, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn
from database import Base, SessionLocal, engine
import models

app = FastAPI()

# DB 엔진 연결
# -> models.py에 정의한 클래스를 통해 db에 테이블 생성
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except :
        print("db연결 오류")
    finally:
        db.close()

# html 문서를 위한 객체
templates = Jinja2Templates(directory="templates")

# 정적파일을 위한 설정
## 정적파일(static) 종류(image, css, js)
app.mount("/static", StaticFiles(directory="static"), name="static")

# localhost:8000/
@app.get("/")
async def home(request: Request):
    # 비즈니스 로직 처리
    data = 100
    data2 = "fastapi 잘하고 싶다."
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "todos": data, "data2": data2}
        )

@app.post("/add")
async def add(request: Request, task: str = Form(...), 
              db_ss: Session = Depends(get_db)):
    # 클라이언트에서 textarea에서 입력 데이터 넘어온것 확인
    print(task)
    # 클라이언트에서 넘어온 task를 Todo 객체로 생성
    todo = models.Todo(task=task)
    # 의존성 주입에서 처리함 Depends(get_db) : 엔진객체생성, 세션연결
    # db 테이블에 task 저장하기
    db_ss.add(todo)
    # db에 실제 저장, commit
    db_ss.commit()
    return task

    
    # 결과를 html에 랜더링에서 리턴

    pass

# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

# CLI명령 : uvicorn main:app --reload