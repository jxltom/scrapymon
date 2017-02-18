# scrapymon

Simple management UI for scrapyd.

## Features

- Show all projects from a Scrapyd server
- Show all versions of each project
- Show all spiders in each project
- Show all pending, running and finished jobs from a Scrapyd server
- Schedule spiders run
- Cancel pending or running jobs
- Delete project or a specific version
- Http basic access authentication supported
- Served by [Gevent](https://github.com/gevent/gevent) for production use

## Getting Started

- Install by ```pip install scrapymon```.

- Run by ```scrapymon [--host=<host>] [--port=<port>] [--server=<address_with_port>] [--auth=<username:password>]```.
    
    - Default ```--host``` is ```0.0.0.0```
    - Default ```--port``` is ```5000```
    - Default ```--server``` is ```http://127.0.0.1:6800```
    - Default ```--auth``` is ```admin:admin```
    
- Or you can run by ```scrapymon``` with valid environment variables ```$HOST```, ```$PORT```, ```$SCRAPYD_SERVER``` and ```$BASIC_AUTH```.

## TODO

- Support logs
- Support schedule a spider run with arguments.
- Highlighted and formated logs
- Log catagory and searcharable logs
- Support create project via ```addversion.json```.
- Localize time
- Add Dockerfile

## Contributing

Contributions are welcomed!
