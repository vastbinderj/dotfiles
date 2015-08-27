##
# Install Golang from source and configure GOPATH
##

WORKDIR=`pwd`

# first clean up soure dir if exists already
if [ -d  $HOME/go ]; then 
    rm -rf $HOME/go
fi

# install golang from the source repository
git clone https://go.googlesource.com/go $HOME/go
cd $HOME/go
# checkout go 1.4.2
git checkout go1.4.2
cd $HOME/go/src
# build from source
CMD="sudo ./all.bash"
eval $CMD
# back to working dir
cd $WORKDIR
unset CMD
