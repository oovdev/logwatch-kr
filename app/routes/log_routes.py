from datetime import datetime
from fastapi import APIRouter, Request
from app.models.log_model import Log, SessionLocal
from app.services.alert_service import send_alert

router = APIRouter()

@router.post("/logs/upload")
async def upload_log(request: Request):
    data = await request.json()

    # 문자열 → datetime 객체로 파싱
    timestamp_str = data.get("timestamp")
    timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.utcnow()

    log = Log(
        timestamp=timestamp,
        hostname=data.get("hostname"),
        log_level=data.get("log_level"),
        message=data.get("message"),
    )

    db = SessionLocal()
    db.add(log)
    db.commit()

    log_message = log.message
    hostname = log.hostname

    db.close()

    if "Disk" in log_message and "90%" in log_message:
        send_alert(hostname, log_message)

    return {"status": "saved", "log": log_message}

