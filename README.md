# radar-frame
## Raspberry Pi powered e-ink weather display
### Server
`gunicorn --log-level=info -b 0.0.0.0:8000 'main:create_server()'`