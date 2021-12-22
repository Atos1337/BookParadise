import uvicorn
from fastapi import FastAPI
from authentication.router import auth


def create_app():
    app = FastAPI()
    app.include_router(auth, prefix="/users")

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
