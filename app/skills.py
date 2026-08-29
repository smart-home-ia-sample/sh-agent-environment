# One entry per A2A skill, served on the agent card. `tags` / `examples` let the
# BFA rank the skill in /resolve straight from the card — no self-registration.
# Tuples: (id, name, description, tags, examples).
SKILLS = [
    ("check_environment", "Check environment",
     "Reports the current environment state (lights, AC, curtains, windows)",
     ["environment", "status"], ["como está o ambiente da casa?", "as luzes estão ligadas?"]),
    ("switch_off_nonessential", "Switch off nonessential", "Turns off nonessential lights and AC",
     ["environment", "energy"], ["desliga o que não é essencial", "apaga tudo que não precisa ficar ligado"]),
    ("turn_on", "Turn on", "Turns a device on (light, TV, coffee maker, AC, ...)",
     ["light", "tv", "appliance", "ac"],
     ["acende a luz da sala", "liga a TV", "liga a cafeteira", "liga o ar-condicionado"]),
    ("turn_off", "Turn off", "Turns a device off (light, TV, coffee maker, AC, ...)",
     ["light", "tv", "appliance", "ac"],
     ["apaga a luz da cozinha", "desliga a TV", "desliga a cafeteira", "desliga o ar"]),
    ("set_brightness", "Set brightness", "Sets a dimmable light's brightness (0-100)",
     ["light", "brightness"], ["diminui o brilho da luz", "coloca a luz em 30%"]),
    ("set_temperature", "Set temperature", "Sets an AC's target temperature (16-30)",
     ["ac", "temperature"], ["ajusta a temperatura para 22", "esfria o quarto"]),
    ("open", "Open", "Opens a curtain or a window",
     ["curtain", "window"], ["abre a cortina da sala", "abre a janela do quarto"]),
    ("close", "Close", "Closes a curtain or a window",
     ["curtain", "window"], ["fecha a cortina do quarto", "fecha a janela"]),
]
