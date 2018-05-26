#!/usr/bin/env bash

CWD=`pwd`
CODEDIR="$HOME/code"

# change to code dir
cd "$CODEDIR"
# download docker
wget https://download.docker.com/linux/static/stable/x86_64/docker-18.03.0-ce.tgz

# extract
tar -zcvf docker-*.tgz

# symlink into /usr/local/bin
sudo ln -s "$CODEDIR/docker/docker" /usr/local/bin/docker

# add bash-completion
sudo curl -L https://raw.githubusercontent.com/docker/docker-ce/master/components/cli/contrib/completion/bash/docker > /etc/bash_completion.d/docker
sudo curl -L https://raw.githubusercontent.com/docker/compose/$(docker-compose version --short)/contrib/completion/bash/docker-compose > /etc/bash_completion.d/docker-compose
