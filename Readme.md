## Microservice with framework Flask
I use synchronous  communication between users, games and auth microservices. I used a requests library to communicate between these services. Asynchronous communication i use for send newsletter and games ratings consumers. I have chosen nosql database - mongodb for data storage.

![Screenshot](microservices.png)

## Usage
Command to run application
```bash
docker-compose up --build -d
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
