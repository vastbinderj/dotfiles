#!/bin/bash

##
# new rig setup and configuration
##

WORKDIR=`pwd`
if ! [ $(id -u) = 0  ]; then
    INSTALLCMD="sudo apt-get install"
else
    INSTALLCMD="apt-get install"
fi

# create code dir if it doesn't exist
if [ ! -d "$HOME/code" ]; then
    mkdir -p $HOME/code
fi
CODEDIR="$HOME/code"


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

    # fix for iterm and terminal.app to use ctrl-h correctly for libterm and neovim
    infocmp $TERM | sed 's/kbs=^[hH]/kbs=\\177/' > $TERM.ti
    tic $TERM.ti

elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    # Found Linux

    if [ -f /etc/lsb-release  ]; then
        # Found Ubuntu
        . /etc/lsb-release

        # Add PPAs
        if [ $(id -u) = 0  ]; then
            add-apt-repository ppa:neovim-ppa/unstable -y
            curl -sL https://deb.nodesource.com/setup_0.12 | bash -
        else
            sudo add-apt-repository ppa:neovim-ppa/unstable -y
            curl -sL https://deb.nodesource.com/setup_0.12 | sudo bash -
        fi

        # Install stuff
        eval $INSTALLCMD \
            bash-completion \
            build-essential \
            bzr \
            checkinstall \
            cmake \
            curl \
            exuberant-ctags \
            git \
            binutils \
            bison \
            gawk \
            gcc \
            grc \
            libc6-dev \
            libpcre3 \
            libpcre3-dev \
            libssl-dev \
            mercurial \
            neovim \
            nodejs \
            python-software-properties \
            python-dev \
            python-setuptools \
            python3-dev \
            python3-setuptools \
            rbenv \
            ruby-build \
            silversearcher-ag \
            vim-nox \
            -y --reinstall

    elif [ -f /etc/os-release  ]; then
        # Found Debian
        . /etc/os-release

        # add add-apt-repository
        eval $INSTALLCMD software-properties-common -y

        # add PPAs
        if [ $(id -u) = 0  ]; then
            curl -sL https://deb.nodesource.com/setup_0.12 | bash -
        else
            curl -sL https://deb.nodesource.com/setup_0.12 | sudo bash -
        fi

        # Install stuff
        sudo apt-get install \
            bash-completion \
            binutils \
            bison \
            build-essential \
            bzr \
            bzip2 \
            checkinstall \
            cmake \
            curl \
            exuberant-ctags \
            gawk \
            git \
            gcc \
            grc \
            libc6-dev \
            libpcre3 \
            libpcre3-dev \
            libssl-dev \
            mercurial \
            nodejs \
            python-software-properties \
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


# symlinks!
#   put/move git credentials into ~/.gitconfig.local
#   http://stackoverflow.com/a/13615531/89484
./createSymLinks.sh

