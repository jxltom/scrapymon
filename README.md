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

## TODO

- Support logs
- Highlighted and formated logs
- Log catagory and searcharable logs
- Support schedule a spider run with arguments.
- Support create project via ```addversion.json```.
- Localize time
- Add Dockerfile

## Contributing

Contributions are welcomed! Pull Requests with relavant tests are recommended.
