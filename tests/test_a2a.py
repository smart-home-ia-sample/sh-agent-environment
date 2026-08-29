import asyncio
import os
import threading
import time

import httpx
import pytest
import uvicorn
from fastapi import FastAPI

BFA_PORT = 9711
AGENT_PORT = 9712

os.environ["BFA_URL"] = f"http://127.0.0.1:{BFA_PORT}"
os.environ["PORT"] = str(AGENT_PORT)

from app.main import app  # noqa: E402
from smart_home_common.a2a_client import call_agent  # noqa: E402


def _build_fake_bfa_app() -> FastAPI:
    fake = FastAPI()

    @fake.post("/resolve/agents")
    def resolve_agents(body: dict):
        return [{
            "kind": "agent",
            "service": "environment",
            "url": f"http://127.0.0.1:{AGENT_PORT}",
            "id": body.get("query", "").replace(" ", "_"),
            "score": 1.0,
        }]

    return fake


def _run(app_, port):
    uvicorn.run(app_, host="127.0.0.1", port=port, log_level="warning")


@pytest.fixture(scope="module", autouse=True)
def servers():
    threading.Thread(target=_run, args=(_build_fake_bfa_app(), BFA_PORT), daemon=True).start()
    threading.Thread(target=_run, args=(app, AGENT_PORT), daemon=True).start()
    time.sleep(1.5)
    yield


def test_health_and_ready():
    assert httpx.get(f"http://127.0.0.1:{AGENT_PORT}/health").status_code == 200
    assert httpx.get(f"http://127.0.0.1:{AGENT_PORT}/ready").status_code == 200


def test_agent_card_lists_expected_skills():
    response = httpx.get(f"http://127.0.0.1:{AGENT_PORT}/.well-known/agent-card.json")

    assert response.status_code == 200
    skill_ids = [s["id"] for s in response.json()["skills"]]
    assert skill_ids == [
        "check_environment",
        "switch_off_nonessential",
        "turn_on",
        "turn_off",
        "set_brightness",
        "set_temperature",
        "open",
        "close",
    ]


def test_unknown_intent_returns_explicit_error():
    result = asyncio.run(
        call_agent(f"http://127.0.0.1:{BFA_PORT}", "turn_on", "does_not_exist", {}, sender="tester")
    )

    assert result["status"] == "error"
    assert "does_not_exist" in result["result"]
