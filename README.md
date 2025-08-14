# Platform Infrastructure

Build Docker Images &amp; Deploy Docker Containers, Provides Development Environment with libraries needed.

## Build Ez Edge Pipeline Docker Images with Docker Bake

~~~bash
pushd ~/src/platform-infrastructure

# Builds Ez Edge Pipeline Backend Docker Image, other images
python scripts/build_image/build_ezedge_docker_image.py

popd
~~~

## Docker Container Deployment

## Deploy Ez Edge Pipeline Docker Container with Docker

~~~bash
pushd ~/src/platform-infrastructure

python scripts/deploy/docker/launch_ezedge_container.py

popd
~~~
