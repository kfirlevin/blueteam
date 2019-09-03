#!/bin/bash
pushd .
cd /blueteam/devops/docker-prod
docker-compose down
docker-compose up --build -d
popd