#!/bin/bash
prod_names=( docker-prod_providers-db docker-prod_providers-server docker-prod_weight-db docker-prod_weight-server)
test_names=( docker-test_providers-db docker-test_providers-server docker-test_weight-db docker-test_weight-server)

pushd .
cd /blueteam/devops/docker-test
docker-compose up --build -d

## Testing
status=$(python3 health)
if [ $status == "True"]
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

popd