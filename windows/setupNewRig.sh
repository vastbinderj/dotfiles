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

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    # Found Linux

    if [ -f /etc/lsb-release  ]; then
        # Found Ubuntu
        #. /etc/lsb-release

        # Install stuff
        eval "$INSTALLCMD" \
            bash-completion \
            build-essential \
            bzr \
            checkinstall \
            cmake \
            curl \
            dos2unix \
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
            python-software-properties \
            python-dev \
            python-setuptools \
            python-pip \
            python3-dev \
            python3-setuptools \
            python3-pip \
            silversearcher-ag \
            software-properties-common \
            -y --reinstall

        # install neovim python support for 2/3
        sudo pip install neovim
        sudo pip3 install neovim
    fi
fi


# add node
if [ -d "$HOME/.nvm" ]; then
    # clean up .bashrc if node has been installed before
    sed '/NVM_DIR/d' $HOME/.bashrc
fi
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
source $HOME/.nvm/nvm.sh
nvm install node
nvm use node


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
./createWSLSymLinks.sh

