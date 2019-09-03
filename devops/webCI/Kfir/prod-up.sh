#!/bin/bash
pushd .
cd /blueteam/devops/docker-prod
docker-compose up --build
popd