
from fastapi import FastAPI
from apis.todo_api import router as todo_router
from apis.user_api import router as user_router
from apis.ml_api import router as ml_router
from apis.ping_api import router as ping_router
from exception.handlers import register_exception_handlers

app = FastAPI(title="Practice API", version="1.0.0")
app.include_router(todo_router)
app.include_router(user_router)
app.include_router(ml_router)
app.include_router(ping_router)

register_exception_handlers(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7701)
# python3 -m uvicorn main:app --host 0.0.0.0 --port 7701 --reload