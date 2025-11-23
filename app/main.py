from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import teams, users, pull_requests, stats
from app.exceptions import AppException

app = FastAPI(title="PR Reviewer Assignment Service")


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


app.include_router(teams.router)
app.include_router(users.router)
app.include_router(pull_requests.router)
app.include_router(stats.router)

