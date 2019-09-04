#!/bin/bash
prod_names=( docker-prod_providers-db docker-prod_providers-server docker-prod_weight-db docker-prod_weight-server)

pushd .
cd /blueteam/devops/docker-prod
docker-compose down

for name in ${prod_names[@]}
do
    docker rmi $name -f
done

popd