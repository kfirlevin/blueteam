import os


def activate_docker(environment='Testing'):
    cmd = 'docker-compose '
    # if environment == 'Production':
    #     cmd += '-f ../docker-prod/docker-compose.yml up -d'
    #     os.system(cmd)
    # else:
    cmd += '-f ../docker-test/docker-compose.yml up -d'
    os.system(cmd)
