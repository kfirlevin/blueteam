#!/bin/bash

test_names=( docker-test_prov-db-test docker-test_providers-server docker-test_weight-db-test docker-test_weight-server)

pushd .
cd /blueteam/devops/docker-test
git checkout providers
git pull
docker-compose up --build -d

## Check if test servers are up
counter=0
urls_up=false
url1="http://blue.develeap.com:8081/health"
url2="http://blue.develeap.com:8082/health"
while [[ "$urls_up" == false && $counter -ne 120 ]]; do 
    if curl --output /dev/null --silent --head --fail "$url1"; then
        if curl --output /dev/null --silent --head --fail "$url2"; then
            urls_up=true
        else
            urls_up=false
        fi
    else
        urls_up=false
    fi
    sleep 1
    counter=$((counter+1))
done

status=$(python /app/Tests/e2e.py)
docker-compose down
for name in ${test_names[@]}
do
    docker rmi $name -f
done
docker volume prune -f
docker images -qf dangling=true | xargs docker rmi