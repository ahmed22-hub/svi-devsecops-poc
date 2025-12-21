from __future__ import annotations

import json
import logging
import os
import time
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import JSONResponse

APP_NAME = "svi-devsecops-poc"
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

logger = logging.getLogger("app")


def setup_logging() -> None:
    """
    Basic structured logging (JSON) to stdout.
    This is enough for later integration with monitoring/log shipping.
    """
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(message)s",
    )


setup_logging()

app = FastAPI(title=APP_NAME, version=APP_VERSION)


@app.get("/health")
def health() -> dict:
    # Simple liveness endpoint
    return {"status": "ok"}


@app.get("/version")
def version() -> dict:
    return {"name": APP_NAME, "version": APP_VERSION}


@app.post("/generate-log")
def generate_log(level: str = "info") -> JSONResponse:
    """
    Generate an event log to test monitoring pipeline.
    level: info|warning|error
    """
    event = {
        "event_id": str(uuid.uuid4()),
        "ts": datetime.now(timezone.utc).isoformat(),
        "service": APP_NAME,
        "version": APP_VERSION,
        "level": level.lower(),
        "message": "generated test event",
        "latency_ms": int(time.time() * 1000) % 250,  # simple pseudo-latency
    }

    msg = json.dumps(event, ensure_ascii=False)

    lvl = event["level"]
    if lvl == "warning":
        logger.warning(msg)
    elif lvl == "error":
        logger.error(msg)
    else:
        logger.info(msg)

    return JSONResponse(content=event)
