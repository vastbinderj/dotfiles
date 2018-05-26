#!/usr/bin/env bash

CWD=`pwd`
CODEDIR="$HOME/code"

# change to code dir
cd "$CODEDIR"
# download docker
wget https://download.docker.com/linux/static/stable/x86_64/docker-18.03.0-ce.tgz

# extract
tar -zcvf docker-*.tgz
rm docker-*.tgz

# create symlink into /usr/local/bin
if [ -f /usr/local/bin/docker ]; then
    sudo rm /usr/local/bin/docker
fi
sudo ln -s "$CODEDIR/docker/docker" /usr/local/bin/docker

# add docker-compose
cd docker
if [ -f /usr/local/bin/docker-compose ]; then
    sudo rm /usr/local/bin/docker-compose
fi
if [ -f docker-compose ]; then
    sudo rm docker-compose
fi

curl -sL https://github.com/docker/compose/releases/download/1.20.1/docker-compose-`uname -s`-`uname -m` > docker-compose
chmod +x docker-compose
sudo ln -s "$CODEDIR/docker/docker-compose" /usr/local/bin/docker-compose

# add bash-completion
if [ -f /etc/bash_completion.d/docker ]; then
    sudo rm /etc/bash_completion.d/docker
elif [ -f /etc/bash_completion.d/docker-compose ]; then
    sudo rm /etc/bash_completion.d/docker-compose
fi
curl -sL https://raw.githubusercontent.com/docker/docker-ce/master/components/cli/contrib/completion/bash/docker > docker_bash-completion
sudo mv docker_bash-completion /etc/bash_completion.d/docker
curl -sL https://raw.githubusercontent.com/docker/compose/$(docker-compose version --short)/contrib/completion/bash/docker-compose > docker-compose_bash_completion
sudo mv docker-compose_bash_completion /etc/bash_completion.d/docker-compose
