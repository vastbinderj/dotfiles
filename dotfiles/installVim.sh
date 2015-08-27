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


# install vundle packages in vim
vim +PluginInstall +qall

# install golang binaries
vim +GoInstallBinaries +qall

# build YouCompleteMe
if [ -f $HOME/.vim/bundle/YouCompleteMe/install.sh  ]; then
    $HOME/.vim/bundle/YouCompleteMe/install.py --clang-completer
fi

