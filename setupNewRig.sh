#!/usr/bin/env bash

##
# new rig setup and configuration
##
CWD=$(pwd)
CODE_DIR="$HOME/code"


if ! [ "$(id -u)" = 0  ]; then
    INSTALLCMD="sudo apt-get install"
else
    INSTALLCMD="apt-get install"
fi

# create code dir if it doesn't exist
if [ ! -d "$CODE_DIR" ]; then
    mkdir -p "$CODE_DIR"
fi

# create jenv dir if it doesn't exist
if [ ! -d "$HOME/.jenv" ]; then
    mkdir -p "$HOME/.jenv"
    mkdir -p "$HOME/.jenv/versions"
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
    git clone https://github.com/thebitguru/play-button-itunes-patch "$CODE_DIR"/play-button-itunes-patch


    # change to bash 4 (installed by homebrew)
    BASHPATH=$(brew --prefix)/bin/bash
    sudo echo "$BASHPATH" >> /etc/shells
    chsh -s "$BASHPATH" # will set for current user only.
    echo "$BASH_VERSION" # should be 4.x not the old 3.2.X
    # Later, confirm iterm settings aren't conflicting.

    # fix for iterm and terminal.app to use ctrl-h correctly for libterm and neovim
    infocmp "$TERM" | sed 's/kbs=^[hH]/kbs=\\177/' > "$TERM.ti"
    tic "$TERM.ti"


elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    # Found Linux

    if [ -f /etc/lsb-release  ]; then
        # Found Ubuntu
        #. /etc/lsb-release

        # Add PPAs
        if [ "$(id -u)" = 0  ]; then
            add-apt-repository ppa:neovim-ppa/unstable -y
        else
            sudo add-apt-repository ppa:neovim-ppa/unstable -y
            sudo apt-get update
        fi


        # Install stuff
        eval "$INSTALLCMD" \
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
            python-pip \
            python3-dev \
            python3-setuptools \
            python3-pip \
            rbenv \
            ruby-build \
            silversearcher-ag \
            vim-nox \
            -y --reinstall

    elif [ -f /etc/os-release  ]; then
        # Found Debian
        #. /etc/os-release

        # add add apt-repositories
        echo "deb http://ppa.launchpad.net/neovim-ppa/unstable/ubuntu vivid main" | sudo tee -a /etc/apt/sources.list > /dev/null
        sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 55F96FCF8231B6DD
        sudo apt-get update
        eval "$INSTALLCMD" software-properties-common -y

        # add PPAs
        if [ "$(id -u)" = 0  ]; then
            curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -
        else
            curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -
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
            neovim \
            python-software-properties \
            python-dev \
            python-setuptools \
            python-pip \
            python3-dev \
            python3-setuptools \
            python3-pip \
            vim-nox \
            rbenv \
            ruby-build \
            silversearcher-ag \
            -y --reinstall

    fi

    # install neovim python support for 2/3
    sudo pip install neovim
    sudo pip3 install neovim

fi


# install google sdk
cd "$CODE_DIR"
curl https://sdk.cloud.google.com | bash
# install kubectl
$CODE_DIR/google-cloud-sdk/bin/gcloud components install kubectl
cd $CWD

# add node
if [ -d "$HOME/.nvm" ]; then
    # clean up .bashrc if node has been installed before
    sed '/NVM_DIR/d' $HOME/.bashrc
fi
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.6/install.sh | bash
source $HOME/.nvm/nvm.sh
nvm install node
nvm use node


# github.com/jamiew/git-friendly
# the `push` command which copies the github compare URL to my clipboard is heaven
bash < <( curl https://raw.github.com/jamiew/git-friendly/master/install.sh)


# github.com/rupa/z   - oh how i love you
git clone https://github.com/rupa/z.git "$CODE_DIR/z"
chmod +x "$CODE_DIR/z/z.sh"
# consider reusing your current .z file if possible. it's painful to rebuild :)
# z hooked up in .bash_profile

# Base16 Shell
git clone https://github.com/chriskempson/base16-shell.git "$HOME/.config/base16-shell"

# Base Material Theme
git clone https://github.com/kristijanhusak/vim-hybrid-material "$CODE_DIR/vim-hybrid-material"
cp "$CODE_DIR/vim-hybrid-material/base16-material/base16-material.dark.sh" "$HOME/.config/base16-shell"


# don't let ssh timeout locally
if [ -d "$HOME/.ssh" ]; then
echo "ServerAliveInterval 120" >> "$HOME/.ssh/config"
chmod 644 "$HOME/.ssh/config"
else
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
echo "ServerAliveInterval 120" >> "$HOME/.ssh/config"
chmod 644 "$HOME/.ssh/config"
fi


# install patched fonts for vim statusline
git clone https://github.com/powerline/fonts "$CODE_DIR/fonts"
$CODE_DIR/fonts/install.sh

# for the c alias (syntax highlighted cat)
sudo easy_install Pygments


# symlinks!
#   put/move git credentials into ~/.gitconfig.local
#   http://stackoverflow.com/a/13615531/89484
./createSymLinks.sh

