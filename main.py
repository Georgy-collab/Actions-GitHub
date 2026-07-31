from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import FastAPI, HTTPException, Query

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


@app.get("/convert")
def convert_timezone(
    to_tz: str = Query(..., description="Целевой часовой пояс, например Europe/Moscow"),
    from_tz: str = Query("UTC", description="Исходный часовой пояс"),
    time: str | None = Query(
        None,
        description="Время в ISO 8601 (например 2026-07-31T15:30:00). Если не указано — текущее",
    ),
):
    try:
        source_zone = ZoneInfo(from_tz)
        target_zone = ZoneInfo(to_tz)
    except ZoneInfoNotFoundError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Неизвестный часовой пояс: {exc.args[0]}",
        ) from exc

    if time is None:
        source_dt = datetime.now(source_zone)
    else:
        try:
            parsed = datetime.fromisoformat(time)
        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail="Некорректный формат time. Используйте ISO 8601, например 2026-07-31T15:30:00",
            ) from exc

        if parsed.tzinfo is None:
            source_dt = parsed.replace(tzinfo=source_zone)
        else:
            source_dt = parsed.astimezone(source_zone)

    target_dt = source_dt.astimezone(target_zone)

    return {
        "from": {
            "timezone": from_tz,
            "time": source_dt.isoformat(),
        },
        "to": {
            "timezone": to_tz,
            "time": target_dt.isoformat(),
        },
        "unix": source_dt.timestamp(),
    }
