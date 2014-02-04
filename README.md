This is my personal collection of dotfiles for rails/node dev.  I use Supertab for code completion 
and my mapleader is a ','.  Be sure to read through the .vimrc file for key mappings, as they are set to 
ones which suite me best. I use vim installed with hombrew on my personal hardware, but these work well with vim 7.2+ on Cent OS and Ubuntu.

## dotfiles included

        - bash_profile (for mac)
        - bashrc       (for linux)
        - vimrc
        - gemrc
        - jshintrc
        - npmrc        (modify the path for your home dir)
        
All the dotfiles are in the dotfiles folder and must be symlinked into your home directory like:
        
        > ln -s ~/.vim/dotfiles/jshintrc ~/.jshintrc
        > ln -s ~/.vim/dotfiles/bash_profile ~/.bash_profile

* To get the git prompt to work and to enable bash completion install bash-completion through homebrew on a mac

        > brew install bash-completion

* To enable mouse scrolling on a mac in terminal, install [easySIMBL](https://github.com/norio-nomura/EasySIMBL) and [mouseterm](https://bitheap.org/mouseterm/) or use iTerm.

## Installed Vim modules of note
        
        - Surround
        - Fugitive
        - Ctrl-P
        - NERDTree 
        - NERDCommenter
        - SuperTab
        - Airline
        - JSHint
        - Repeat.vim
        - SnipMate
        - headlights
        - Vim Indent Guides
        - ZenCoding (Emmet)


## Installation:

        > git clone https://github.com/vastbinderj/dotfiles.git

### Create symlinks:

        > ln -s ~/.vim/dotfiles/vimrc ~/.vimrc
        > ln -s ~/.vim/dotfiles/gvimrc ~/.gvimrc

### Add Sub-modules for bundles:
Switch to the `~/.vim` directory, and fetch submodules:

        > cd ~/.vim
        > git submodule update --init
        > mkdir autoload
        > ln -s ~/.vim/bundle/pathogen/autoload/pathogen.vim ~/.vim/autoload/pathogen.vim

### To upgrade all bundled plugins at any time:

        > git submodule foreach git pull origin master
        > git add -A
        > git commit -m 'random message'
        > git submodule update --init
    
Remember to download and install Exuberant Ctags, Ack and Pep8 if you want to use those features for your 
OS and vim configuration.

### For Django code completion on a project by project basis

        > export DJANGO_SETTINGS_MODULE=project.settings

## On Mac:
    
###    Install Ctags and Ack

        > brew install ctags
        
###     For NerdTree-Ack

        > brew install ack
    
###    For Ruby Debugging in VIM:

        > gem install ruby-debug-ide


###    For Python folks:
        
Install virtualenv and pep8

## On Linux: 

        > sudo apt-get install ctags
        OR
        > sudo yum install ctags
    
###    For Ruby Debugging in VIM:

        > gem install ruby-debug-ide

###    For Python folks:

Install virtualenv and pep8 for your OS
