import uvicorn
from fastapi import FastAPI
from fastapi_pagination import Page, paginate, Params, add_pagination
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from AutomationFramework.common.db.database import Base, engine
from AutomationFramework.router import base, login, interface,testcase

app = FastAPI()
# 添加分页
add_pagination(app)
app.include_router(base.router)
app.include_router(login.router)
app.include_router(interface.router)
app.include_router(testcase.router)

origins = [
    "http://localhost",
    "http://localhost:8000/",
    "http://localhost:8001/",
    "http://0.0.0.0:8001/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 添加分页
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
