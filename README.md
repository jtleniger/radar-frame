# radar-frame
## Raspberry Pi powered e-ink weather display
### Server
`gunicorn --log-level=info --timeout 90 -b 0.0.0.0:8000 'main:create_server()'`

sudo apt-get install python3-dev