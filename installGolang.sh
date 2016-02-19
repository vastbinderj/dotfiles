#!/bin/bash

##
# Install Golang from source and configure GOPATH
##

WORKDIR=$(pwd)

# first clean up soure dir if exists already
if [ -d  "$HOME/go" ]; then
    rm -rf "$HOME/go"
fi

# install Go1.4.2 binaries
if [[ "$OSTYPE" == "darwin"* ]]; then
    cd "$HOME" || exit
    wget -qO- https://storage.googleapis.com/golang/go1.4.2.darwin-amd64-osx10.8.tar.gz | tar --transform 's/^go/go1.4/' -xvz
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    if [ $(uname -m) == 'x86_64' ]; then
        cd "$HOME" || exit
        wget -qO- https://storage.googleapis.com/golang/go1.4.2.linux-amd64.tar.gz | tar --transform 's/^go/go1.4/' -xvz
    else
        cd "$HOME" || exit
        wget -qO- https://storage.googleapis.com/golang/go1.4.2.linux-386.tar.gz | tar --transform 's/^go/go1.4/' -xvz
    fi
fi

# create GOPATH dirt
if [ ! -d "$HOME/code/go" ]; then
    mkdir -p "$HOME/code/go"
    mkdir -p "$HOME/code/go/{src,pkg,bin}"
fi


# install golang from the source repository
git clone https://github.com/golang/go "$HOME/go"
cd "$HOME/go" || exit


# checkout go 1.5
git checkout release-branch.go1.6
cd "$HOME/go/src" || exit


# build from source
CMD="./all.bash"
eval $CMD


# back to working dir
cd "$WORKDIR" || exit
unset CMD
