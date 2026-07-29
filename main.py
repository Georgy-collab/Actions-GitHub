from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="Time API", description="Простой тестовый бэкенд")


@app.get("/")
def root():
    return {"message": "Time API is running"}


@app.get("/time")
def get_server_time():
    now = datetime.now(timezone.utc)
    return {
        "utc": now.isoformat(),
        "unix": now.timestamp(),
        "timezone": "UTC",
    }


@app.get("/date")
def get_server_date():
    today = datetime.now(timezone.utc).date()
    return {
        "date": today.isoformat(),
        "year": today.year,
        "month": today.month,
        "day": today.day,
        "weekday": today.strftime("%A"),
        "timezone": "UTC",
    }
