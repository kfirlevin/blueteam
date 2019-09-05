#!/bin/bash
prod_names=( prov-db-prod docker-prod_providers-server weight-db-prod docker-prod_weight-server)
test_names=( prov-db-test docker-test_providers-server weight-db-test docker-test_weight-server)

pushd .
cd /blueteam/devops/docker-test
git pull
docker-compose up --build -d

## Testing
status=$(python /app/Tests/e2e.py)
if [ $status == "True" ]
then
    docker-compose down
    for name in ${test_names[@]}
    do
        docker rmi $name -f
    done

    # cd /blueteam/devops/docker-prod
    # docker-compose down
    # for name in ${prod_names[@]}
    # do
    #     docker rmi $name -f
    # done
    # docker-compose up --build -d
# else
#     docker-compose down
#     for name in ${test_names[@]}
#     do
#         docker rmi $name -f
#     done
fi
docker images -qf dangling=true | xargs docker rmi

popd