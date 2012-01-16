This is my personal collection of dotvim files for Rails/Python dev.  I use Supertab for code completion 
and my mapleader is a ','.  Be sure to read through the .vimrc file for key mappings, as they are set to 
ones which suite me best. I do use macvim on my personal hardware, but these work well with vim 7.2 and 7.3 on Cent OS and Ubuntu.


## Installation:

        > git clone git://github.com/vastbinderj/dotvim.git ~/.vim

### Create symlinks:

        > ln -s ~/.vim/vimrc ~/.vimrc
        > ln -s ~/.vim/gvimrc ~/.gvimrc

### Add Sub-modules for bundles:
Switch to the `~/.vim` directory, and fetch submodules:

        > cd ~/.vim
        > git submodule update --init
        > mkdir autoload
        > ln -s ~/.vim/bundle/pathogen/autoload/pathogen.vim ~/.vim/autoload/pathogen.vim

### To upgrade all bundled plugins at any time:

        > git submodule foreach git pull origin master
    
Remember to download and install Ctags and Pep8 if you want to use those features for your 
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
        
Install virtualenv and pep8

## On Linux: 

        > sudo apt-get install ctags

###    For Command-T :
(be sure you use the same version of ruby you compiled vim with)
    
        > cd ~/.vim/bundle/command-t
        > rake make
    
###    For Ruby Debugging in VIM:

        > gem install ruby-debug-ide

###    For Python folks:

Install virtualenv and pep8 for your OS
