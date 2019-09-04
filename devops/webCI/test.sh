#!/bin/bash
prod_names=( prov-db-prod docker-prod_providers-server weight-db-prod docker-prod_weight-server)
test_names=( prov-db-test docker-test_providers-server weight-db-test docker-test_weight-server)

pushd .
cd /blueteam/devops/docker-test
git pull
docker-compose up --build -d

## Testing

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
##########################
status=$(python /app/Tests/e2e.py)
if [ $status == "True" ]
then
    docker-compose down
    for name in ${test_names[@]}
    do
        docker rmi $name -f
    done

    cd /blueteam/devops/docker-prod
    docker-compose down
    for name in ${prod_names[@]}
    do
        docker rmi $name -f
    done
    docker-compose up --build -d
else
    docker-compose down
    for name in ${test_names[@]}
    do
        docker rmi $name -f
    done
fi
docker volume prune -f
docker images -qf dangling=true | xargs docker rmi

popd