import os


def activate_docker(environment='Testing'):
    cmd = 'docker-compose '
    # if environment == 'Production':
    #     cmd += '-f ../docker-prod/docker-compose.yml up -d'
    #     os.system(cmd)
    # else:
    cmd += '-f /app/blueteam/devops/docker-test/docker-compose.yml up --build'
    os.system(cmd)


def update_repo(path):
    if not os.path.isdir(path):
        os.system(
            'git clone https://github.com/tomikonio/blueteam.git {}'.format(path))
    os.chdir(path)
    os.system('git pull')
