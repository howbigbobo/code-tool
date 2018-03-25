A very very simple http static file server.

## Installation
```bash
$ npm install
```

## Modify the config.json
```bash
    {
        "port": 8520,
        "serveDirs": [
            {
                "name": "English related files",
                "path": "/e",
                "dir": "E:/doc/EnglishTraining"
            },
            {
                "name": "data",
                "path": "/data",
                "dir": "./data"
            }
        ]
    }
```

## Run
```bash
$ node app.js
```
## Done
```bash
$ http://localhost:8520
```