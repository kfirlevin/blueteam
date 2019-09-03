#!/bin/bash
pushd .
cd /blueteam/devops/docker-test
docker-compose up --build -d

## Testing 
status=$(python)

popd