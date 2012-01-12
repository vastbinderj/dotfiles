## Installation:

        > git clone git://github.com/vastbinderj/dotvim.git ~/.vim

## Create symlinks:

        > ln -s ~/.vim/vimrc ~/.vimrc
        > ln -s ~/.vim/gvimrc ~/.gvimrc

Switch to the `~/.vim` directory, and fetch submodules:

        > cd ~/.vim
        > git submodule update --init
        > mkdir autoload
        > ln -s ~/.vim/bundle/pathogen/autoload/pathogen.vim ~/.vim/autoload/pathogen.vim

## To upgrade all bundled plugins at any time:

        > git submodule foreach git pull origin master
    
Remember to download and install Ctags, Pep8 and L9 if you want to use those features for your 
OS and vim configuration.

## On mac:
    
###    Install Ctags

        > brew install ctags
    
###    For Command-T :
(be sure you use the same version of ruby you compiled VIM with)
    
        > cd ~/.vim/bundle/command-t
        > rake make
    
###    For Ruby Debugging in VIM:

        > gem install ruby-debug-ide


###    For Python folks:
        
Install virtualenv, L9 and pep8

## On Linux: 

        > sudo apt-get install ctags

###    For Command-T :
(be sure you use the same version of ruby you compiled vim with)
    
        > cd ~/.vim/bundle/command-t
        > rake make
    
###    For ruby debugging in vim:

        > gem install ruby-debug-ide


###    For python folks:
        
Install virtualenv, L9 and pep8
