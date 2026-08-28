# sh-agent-environment

Environment A2A agent: `check_environment`, `switch_off_nonessential`, and the device verbs `turn_on`/`turn_off`/`set_brightness`/`set_temperature`/`open`/`close`.

Part of the **Smart Home AI** system — architecture, the full `docker compose`
stack and the end-to-end tests live in `sh-infra`.

## Run the tests
```
pip install -r requirements-dev.txt   # needs sh-common from the registry
pytest
```

## Build the image
```
docker build -t sh-agent-environment .
```
