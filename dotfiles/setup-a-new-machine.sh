##
## new machine setup.
##

WORKDIR=`pwd`
GOSYSTEMVERSION=`go version`

# create code dir if it doesn't exist
if [ ! -d "$HOME/code" ]; then
    mkdir -p $HOME/code
fi
CODEDIR="$HOME/code"

# create GOPATH dirs
if [ ! -d "$HOME/code/go" ]; then
    mkdir -p $CODEDIR/go
    mkdir -p $CODEDIR/go/{src,pkg,bin}
fi


if [[ "$OSTYPE" == "darwin"* ]]; then
    # Found Mac OSX

    #
    # homebrew!
    #
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

    # then install things
    ./brew.sh


    # github.com/thebitguru/play-button-itunes-patch
    # disable itunes opening on media keys
    git clone https://github.com/thebitguru/play-button-itunes-patch ~/code/play-button-itunes-patch


    # change to bash 4 (installed by homebrew)
    BASHPATH=$(brew --prefix)/bin/bash
    sudo echo $BASHPATH >> /etc/shells
    chsh -s $BASHPATH # will set for current user only.
    echo $BASH_VERSION # should be 4.x not the old 3.2.X
    # Later, confirm iterm settings aren't conflicting.

elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    # Found Linux

    if [ -f /etc/lsb-release  ]; then
        # Found Ubuntu
        . /etc/lsb-release

        # Add PPAs
        sudo add-apt-repository ppa:neovim-ppa/unstable -y
        curl -sL https://deb.nodesource.com/setup_0.12 | sudo bash -
        sudo apt-get update

        # Install stuff
        sudo apt-get install \
            bash-completion \
            build-essential \
            mercurial \
            curl \
            git \
            binutils \
            bison \
            gcc \
            libc6-dev \
            bzr \
            exuberant-ctags \
            cmake \
            grc \
            neovim \
            python-dev \
            python-setuptools \
            python3-dev \
            python3-setuptools \
            vim-nox \
            rbenv \
            ruby-build \
            silversearcher-ag \
            -y --reinstall

    elif [ -f /etc/os-release  ]; then
        # Found Debian
        . /etc/os-release

        # add the Nodesource 0.12 repo to apt
        sudo add-apt-repository ppa:neovim-ppa/unstable -y
        curl -sL https://deb.nodesource.com/setup_0.12 | sudo bash -
        sudo apt-get update

        # Install stuff
        sudo apt-get install \
            bash-completion \
            build-essential \
            mercurial \
            curl \
            git \
            binutils \
            bison \
            gcc \
            libc6-dev \
            bzr \
            exuberant-ctags \
            cmake \
            grc \
            python-dev \
            python-setuptools \
            python3-dev \
            python3-setuptools \
            vim-nox \
            rbenv \
            ruby-build \
            silversearcher-ag \
            -y --reinstall
    fi


    # go.googlesource.com/go
    # install golang from the source repository

    # first clean up soure dir if exists already
    if [ -d  $HOME/go ]; then 
        rm -rf $HOME/go
    fi
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
fi


# github.com/jamiew/git-friendly
# the `push` command which copies the github compare URL to my clipboard is heaven
bash < <( curl https://raw.github.com/jamiew/git-friendly/master/install.sh)


# github.com/rupa/z   - oh how i love you
git clone https://github.com/rupa/z.git $HOME/code/z
chmod +x ~/code/z/z.sh
# consider reusing your current .z file if possible. it's painful to rebuild :)
# z hooked up in .bash_profile


# Base16 Shell
git clone https://github.com/chriskempson/base16-shell.git $HOME/.config/base16-shell


# for the c alias (syntax highlighted cat)
sudo easy_install Pygments


# clone vundle in ~/.vim/bundle
git clone https://github.com/gmarik/Vundle.vim.git $HOME/.vim/bundle/Vundle.vim


# install vundle packages in vim
vim +PluginInstall +qall

# build YouCompleteMe
if [ -f $HOME/.vim/bundle/YouCompleteMe/install.sh  ]; then
    $HOME/.vim/bundle/YouCompleteMe/install.sh --clang-completer
fi


# symlinks!
#   put/move git credentials into ~/.gitconfig.local
#   http://stackoverflow.com/a/13615531/89484
./symlink-setup.sh

