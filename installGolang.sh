#!/bin/bash

##
# Install Golang from source and configure GOPATH
##

WORKDIR=$(pwd)

# first clean up soure dirs if they exist already
if [ -d  "$HOME/go" ]; then
    rm -rf "$HOME/go"
fi

# clean up go 1.4 - just in case
if [ -d  "$HOME/go1.4" ]; then
    rm -rf "$HOME/go1.4"
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
    cd "$HOME" || exit
    brew install go
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    # install Go1.4.2 binaries
    if [ "$(uname -m)" == 'x86_64' ]; then
        cd "$HOME" || exit
        wget -qO- https://storage.googleapis.com/golang/go1.4.3.linux-amd64.tar.gz | tar --transform 's/^go/go1.4/' -xvz
    else
        cd "$HOME" || exit
        wget -qO- https://storage.googleapis.com/golang/go1.4.3.linux-386.tar.gz | tar --transform 's/^go/go1.4/' -xvz
    fi
fi

# create GOPATH dirt
if [ ! -d "$HOME/code/go" ]; then
    mkdir -p "$HOME/code/go"
    mkdir -p "$HOME/code/go/"{src,pkg,bin}
fi


# install golang from the source repository
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    git clone https://github.com/golang/go "$HOME/go"
    cd "$HOME/go" || exit


    # checkout go 1.5
    git checkout go1.7.1
    cd "$HOME/go/src" || exit


    # build from source
    CMD="./make.bash"
    eval $CMD
fi

# install additional tools
go get golang.org/x/tools/cmd/...

# back to working dir
cd "$WORKDIR" || exit
unset CMD
