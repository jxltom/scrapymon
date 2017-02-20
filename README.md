# scrapymon

Simple management UI for scrapyd. The demo is available at [http://scrapymon.demo.jxltom.me/](http://scrapymon.demo.jxltom.me/) with ```admin``` for both username and password. Note that the demo will reset every 10 minutes and it may take some time to spin up if no one has accessed it for a while. 

## Features

- Show all projects from a Scrapyd server
- Show all versions of each project
- Show all spiders in each project
- Show all pending, running and finished jobs from a Scrapyd server
- Show logs of each job
- Schedule spiders run
- Cancel pending or running jobs
- Delete project or a specific version
- Http basic access authentication supported
- Served by [Gevent](https://github.com/gevent/gevent) for production use

## Screenshots

![projects_dash](https://github.com/jxltom/scrapymon/blob/master/docs/_static/projects_dash.png)
![jobs_dash](https://github.com/jxltom/scrapymon/blob/master/docs/_static/jobs_dash.png)
![logs_dash](https://github.com/jxltom/scrapymon/blob/master/docs/_static/logs_dash.png)

## Getting Started

- Install by ```pip install scrapymon```.

- Run by ```scrapymon [--host=<host>] [--port=<port>] [--server=<address_with_port>] [--auth=<username:password>]```.
    
    - Default ```--host``` is ```0.0.0.0```
    - Default ```--port``` is ```5000```
    - Default ```--server``` is ```http://127.0.0.1:6800```
    - Default ```--auth``` is ```admin:admin```
    
- Or you can run by ```scrapymon``` with valid environment variables ```$HOST```, ```$PORT```, ```$SCRAPYD_SERVER``` and ```$BASIC_AUTH```.

## TODO

- Support schedule a spider run with arguments.
- Highlighted and searcharable logs with catagories
- Logs auto refresh and pagination
- Create project via ```addversion.json```.
- Time Localization
- Add Dockerfile

## Contributing

Contributions are welcomed!
