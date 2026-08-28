import httpx

from smart_home_common.registration_client import ServiceInfo, register_with_retry

SKILLS = [
    ("check_environment", "Check environment",
     "Reports the current environment state (lights, AC, curtains, windows)",
     ["como está o ambiente da casa?", "as luzes estão ligadas?"]),
    ("switch_off_nonessential", "Switch off nonessential", "Turns off nonessential lights and AC",
     ["desliga o que não é essencial", "apaga tudo que não precisa ficar ligado"]),
    ("turn_on", "Turn on", "Turns a device on (light, TV, coffee maker, AC, ...)",
     ["acende a luz da sala", "liga a TV", "liga a cafeteira", "liga o ar-condicionado"]),
    ("turn_off", "Turn off", "Turns a device off (light, TV, coffee maker, AC, ...)",
     ["apaga a luz da cozinha", "desliga a TV", "desliga a cafeteira", "desliga o ar"]),
    ("set_brightness", "Set brightness", "Sets a dimmable light's brightness (0-100)",
     ["diminui o brilho da luz", "coloca a luz em 30%"]),
    ("set_temperature", "Set temperature", "Sets an AC's target temperature (16-30)",
     ["ajusta a temperatura para 22", "esfria o quarto"]),
    ("open", "Open", "Opens a curtain or a window", ["abre a cortina da sala", "abre a janela do quarto"]),
    ("close", "Close", "Closes a curtain or a window", ["fecha a cortina do quarto", "fecha a janela"]),
]

CAPABILITIES = [skill_id for skill_id, *_ in SKILLS]
CATALOG = [
    {"id": sid, "name": name, "description": desc, "tags": ["environment"], "examples": examples}
    for sid, name, desc, examples in SKILLS
]


def register_with_bfa(bfa_url: str, port: int, version: str = "0.1.0", max_attempts: int = 10) -> dict:
    service = ServiceInfo(
        name="environment", port=port, capabilities=CAPABILITIES, protocol="http", version=version, catalog=CATALOG
    )
    with httpx.Client(timeout=5.0) as client:
        return register_with_retry(client, bfa_url, service, kind="agents", max_attempts=max_attempts)
