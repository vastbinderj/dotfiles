#!/bin/bash

##
#  Install Vim, Golang binaries and YCM
##

WORKDIR=`pwd`

# create .vim if it doesn't exist
if [ ! -d "$HOME/.vim" ]; then
    mkdir -p $HOME/.vim
    mkdir -p $HOME/bundle
fi
# clone vundle in ~/.vim/bundle
git clone https://github.com/gmarik/Vundle.vim.git $HOME/.vim/bundle/Vundle.vim

# set up compatibility with neovim
if [ ! -d "$HOME/.config" ]; then
    mkdir -p ${XDG_CONFIG_HOME:=$HOME/.config}
    ln -s ~/.vim "$XDG_CONFIG_HOME/nvim"
    ln -s ~/.vimrc "$XDG_CONFIG_HOME/nvim/init.vim"
fi

# install vundle packages in vim
vim +PluginInstall +qall

# install golang binaries
vim +GoInstallBinaries +qall

# set up material theme
if [ -f $HOME/code/vim-hybrid-material  ]; then
    mkdir -p $HOME/.vim/colors
    cp $HOME/code/vim-hybrid-material/base16-material/base16-material-dark.vim $HOME/.vim/colors/
fi

