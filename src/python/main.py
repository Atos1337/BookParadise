import uvicorn
from fastapi import FastAPI
from authentication.router import auth as authentication
from authorization.router import auth as authorization
from quotes.router import quotes
from portfolio.router import port


def create_app():
    app = FastAPI()
    app.include_router(authentication, prefix="/users")
    app.include_router(authorization, prefix="/auth")
    app.include_router(quotes, prefix="/quotes")
    app.include_router(port, prefix="/portfolio")

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
