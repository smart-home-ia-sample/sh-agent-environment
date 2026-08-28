from typing import Protocol

# Scenario capability `switch_off_nonessential` still works off a fixed list —
# lights + the bedroom AC (the fridge/TV/coffee maker stay as they are).
NONESSENTIAL_DEVICES = ["living_room_light", "kitchen_light", "bedroom_light", "bedroom_ac"]


class McpClientLike(Protocol):
    async def call_tool(self, name: str, arguments: dict | None = None): ...
    async def read_resource(self, uri: str): ...


async def check_environment(mcp: McpClientLike) -> dict:
    return await mcp.read_resource("home://environment")


async def switch_off_nonessential(mcp: McpClientLike) -> dict:
    for device_id in NONESSENTIAL_DEVICES:
        await mcp.call_tool("turn_off", {"device_id": device_id})
    return await mcp.read_resource("home://environment")


async def device_command(mcp: McpClientLike, verb: str, device_id: str, value: float | int | None = None) -> dict:
    """Forward a generic verb ({turn_on, turn_off, set_brightness, set_temperature,
    open, close}) to the Home MCP. The MCP / BFF validate the verb against the
    device's announced capabilities."""
    args: dict = {"device_id": device_id}
    if value is not None:
        args["value"] = value
    return await mcp.call_tool(verb, args)
