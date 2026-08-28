import asyncio

from app import domain


class FakeMcpClient:
    def __init__(self, responses: dict):
        self.responses = responses
        self.calls: list[tuple] = []

    async def call_tool(self, name, arguments=None):
        self.calls.append(("call_tool", name, arguments))
        return self.responses.get(name, {})

    async def read_resource(self, uri):
        self.calls.append(("read_resource", uri, None))
        return self.responses.get(uri, {})


def test_check_environment_reads_resource():
    fake = FakeMcpClient({"home://environment": {"living_room": {"light": {"on": True}}}})

    result = asyncio.run(domain.check_environment(fake))

    assert fake.calls == [("read_resource", "home://environment", None)]
    assert result["living_room"]["light"]["on"] is True


def test_switch_off_nonessential_turns_everything_off_with_one_verb():
    fake = FakeMcpClient({"home://environment": {"bedroom": {"ac": {"on": False}}}})

    result = asyncio.run(domain.switch_off_nonessential(fake))

    tool_calls = [(c[1], c[2]["device_id"]) for c in fake.calls if c[0] == "call_tool"]
    assert ("turn_off", "living_room_light") in tool_calls
    assert ("turn_off", "kitchen_light") in tool_calls
    assert ("turn_off", "bedroom_light") in tool_calls
    assert ("turn_off", "bedroom_ac") in tool_calls
    assert result["bedroom"]["ac"]["on"] is False


def test_device_command_turn_on_and_off():
    fake = FakeMcpClient({"turn_on": {"on": True}, "turn_off": {"on": False}})

    on = asyncio.run(domain.device_command(fake, "turn_on", "living_room_light"))
    off = asyncio.run(domain.device_command(fake, "turn_off", "kitchen_coffee_maker"))

    assert on["on"] is True
    assert off["on"] is False
    assert ("call_tool", "turn_off", {"device_id": "kitchen_coffee_maker"}) in fake.calls


def test_device_command_forwards_a_value():
    fake = FakeMcpClient({"set_brightness": {"brightness": 42}, "set_temperature": {"temperature": 20}})

    b = asyncio.run(domain.device_command(fake, "set_brightness", "bedroom_light", 42))
    t = asyncio.run(domain.device_command(fake, "set_temperature", "bedroom_ac", 20))

    assert fake.calls == [
        ("call_tool", "set_brightness", {"device_id": "bedroom_light", "value": 42}),
        ("call_tool", "set_temperature", {"device_id": "bedroom_ac", "value": 20}),
    ]
    assert b["brightness"] == 42 and t["temperature"] == 20


def test_device_command_open_and_close():
    fake = FakeMcpClient({"open": {"open": True}, "close": {"open": False}})

    opened = asyncio.run(domain.device_command(fake, "open", "bedroom_window"))
    closed = asyncio.run(domain.device_command(fake, "close", "living_room_curtain"))

    assert opened["open"] is True
    assert closed["open"] is False
