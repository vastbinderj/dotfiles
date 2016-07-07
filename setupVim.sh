#!/usr/bin/env bash

##
#  Install Vim, Golang binaries and YCM
##

# create .vim if it doesn't exist
if [ ! -d "$HOME/.vim" ]; then
    mkdir -p "$HOME/.vim"
    mkdir -p "$HOME/bundle"
fi

# set up material theme
if [ -f "$HOME/code/vim-hybrid-material"  ]; then
    mkdir -p "$HOME/.vim/colors"
    cp "$HOME/code/vim-hybrid-material/base16-material/base16-material-dark.vim" "$HOME/.vim/colors/"
else
    git clone https://github.com/kristijanhusak/vim-hybrid-material "$HOME/code/vim-hybrid-material"
    mkdir -p "$HOME/.vim/colors"
    cp "$HOME/code/vim-hybrid-material/base16-material/base16-material-dark.vim" "$HOME/.vim/colors/"
fi

# clone vundle in ~/.vim/bundle
git clone https://github.com/gmarik/Vundle.vim.git "$HOME/.vim/bundle/Vundle.vim"

# set up compatibility with neovim
if [ ! -d "$HOME/.config" ]; then
    mkdir -p "${XDG_CONFIG_HOME:=$HOME/.config}"
fi
if [ ! -e "$HOME/.config/nvim" ]; then
    ln -s ~/.vim "$HOME/.config/nvim"
    ln -s ~/.vimrc "$HOME/.config/nvim/init.vim"
fi

# install vundle packages in vim
vim +PluginInstall +qall
nvim +PluginInstall +qall

# install golang binaries
vim +GoInstallBinaries +qall

