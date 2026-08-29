import os

from fastapi import APIRouter, FastAPI

from app import domain
from app.skills import SKILLS
from smart_home_common import HomeMcpClient, IntentAgentExecutor, build_agent_card, mount_a2a

router = APIRouter()
mcp_client = HomeMcpClient(os.environ["BFA_URL"])

HANDLERS = {
    "check_environment": lambda input: domain.check_environment(mcp_client),
    "switch_off_nonessential": lambda input: domain.switch_off_nonessential(mcp_client),
    "turn_on": lambda input: domain.device_command(mcp_client, "turn_on", input["device_id"]),
    "turn_off": lambda input: domain.device_command(mcp_client, "turn_off", input["device_id"]),
    "set_brightness": lambda input: domain.device_command(
        mcp_client, "set_brightness", input["device_id"], input["value"]
    ),
    "set_temperature": lambda input: domain.device_command(
        mcp_client, "set_temperature", input["device_id"], input["value"]
    ),
    "open": lambda input: domain.device_command(mcp_client, "open", input["device_id"]),
    "close": lambda input: domain.device_command(mcp_client, "close", input["device_id"]),
}


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/ready")
def ready():
    return {"status": "ready"}


def mount(app: FastAPI) -> None:
    app.include_router(router)
    executor = IntentAgentExecutor(HANDLERS)
    card = build_agent_card("environment", skills=SKILLS)
    mount_a2a(app, card, executor)
