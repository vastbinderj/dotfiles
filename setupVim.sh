#!/bin/bash

##
#  Install Vim, Golang binaries and YCM
##

# create .vim if it doesn't exist
if [ ! -d "$HOME/.vim" ]; then
    mkdir -p "$HOME/.vim"
    mkdir -p "$HOME/bundle"
fi

# set up compatibility with neovim
if [ ! -d "$HOME/.config" ]; then
    mkdir -p "${XDG_CONFIG_HOME:=$HOME/.config}"
    ln -s ~/.vim "$XDG_CONFIG_HOME/nvim"
    ln -s ~/.vimrc "$XDG_CONFIG_HOME/nvim/init.vim"
fi

# clone vundle in ~/.vim/bundle
git clone https://github.com/gmarik/Vundle.vim.git "$HOME/.vim/bundle/Vundle.vim"


# install vundle packages in vim
vim +PluginInstall +qall

# install golang binaries
vim +GoInstallBinaries +qall

# build YouCompleteMe
if [ -f "$HOME/.vim/bundle/YouCompleteMe/install.sh"  ]; then
    "$HOME/.vim/bundle/YouCompleteMe/install.py" --clang-completer
fi

