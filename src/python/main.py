import uvicorn
from fastapi import FastAPI
from database.api import db
from authentication.router import auth

app = FastAPI()

app.include_router(auth)


# @app.on_event("startup")
# async def startup():
#     await db.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await db.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
