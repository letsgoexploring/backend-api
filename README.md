# backend-api

This is the code for the Python API service that calculates some of the more complex models on letsgoexploring.github.io.

# Running via Docker

This project includes a Dockerfile that you can use with [docker][] to run the service.

1. Install [docker][] for your platform
2. Build the image: `docker build -t letsgoexploring-api .`
3. Run the image: `docker run letsgoexploring-api`
4. Profit!

For now this is a very simple proof-of-concept that will run `example.py`, print the results, and exit. It will eventually be an HTTP API server.

[docker]: https://www.docker.com/community-edition
