This is my personal collection of dotfiles for golang/rails/node development.  I use [YouCompleteMe](https://github.com/Valloric/YouCompleteMe) for code completion and my mapleader is a ','.  Be sure to read through the .vimrc file for key mappings, as they are set to ones which suite me best. I use vim 7.4 installed with hombrew on my macs, but these work well with vim 7.2+ on Cent OS and Ubuntu.

## dotfiles included

        - bash_profile (for mac)
        - bashrc       (for linux)
        - vimrc
        - gemrc
        - jshintrc
        - npmrc        (modify the path for your home dir)
        - tmux.conf    (prefix set to ctrl-a and vim key-mappings)
        
All the dotfiles are in the dotfiles folder and must be symlinked into your home directory like:
        
        > ln -s ~/.vim/dotfiles/jshintrc ~/.jshintrc
        > ln -s ~/.vim/dotfiles/bash_profile ~/.bash_profile

* To get the git prompt to work and to enable bash completion install bash-completion through homebrew on a mac

        > brew install bash-completion

* To enable mouse scrolling on a mac in terminal, install [easySIMBL](https://github.com/norio-nomura/EasySIMBL) and [mouseterm](https://bitheap.org/mouseterm/) or use iTerm.  I use iTerm and have installed [patched fonts](https://github.com/Lokaltog/powerline-fonts) for airline and my tmuxline.

* For golang development, I use [vim-go](https://github.com/fatih/vim-go) which does many things for me like auto-imports, gofmt upon save and provides easy jump mappings to quickly browse source code.  

* Mappings for Escape
  * j-k
  * ;-f to save and coninue in the current mode
  * ;-a to save and switch modes
* Mappings for pane movement vim and tmux
  * C-h - Left one pane
  * C-j - Down one pane
  * C-k - Up one pane
  * C-l - Right one pane
* Tmux mappings
  * C-a,- to split a pane horizontally
  * C-a,\ to split a pane vertically
  * Shift-leftarrow to move to the left window
  * Shift-rightarrow to move to the right window

## Installed Vim modules of note
        
        - Airline
        - Ctrl-P
        - DelimitMate
        - Fugitive
        - Gundo
        - vim-go
        - NERDTree 
        - headlights
        - tmuxline
        - JSHint
        - Repeat.vim
        - SnipMate
        - SuperTab
        - Surround
        - Syntastic
        - TComment
        - Vim Indent Guides
        - Emmet



## Installation:

        > git clone https://github.com/vastbinderj/dotfiles.git

### Create symlinks:

        > ln -s ~/.vim/dotfiles/vimrc ~/.vimrc
        > ln -s ~/.vim/dotfiles/gvimrc ~/.gvimrc

### Add Sub-modules for bundles:
Switch to the `~/.vim` directory, and fetch submodules:

        > cd ~/.vim
        > git submodule update --init --recursive
        > mkdir autoload
        > ln -s ~/.vim/bundle/pathogen/autoload/pathogen.vim ~/.vim/autoload/pathogen.vim

### To upgrade all bundled plugins at any time:

        > git submodule foreach git pull origin master
        > git add -A
        > git commit -m 'random message'
        > git submodule update --init
    
Remember to download and install Exuberant Ctags, Ack and Pep8 if you want to use those features for your 
OS and vim configuration.  


## On Mac:
    
###    Install Ctags and Ack

        > brew install ctags ack

###    Install gocode for golang syntax highlighting with syntastic

        > go get -u github.com/nsf/gocode
        
Additionally, for golang you must set $GOROOT for YCM to pick up the standard libary in completions.
        
###    Finish install of YouCompleteMe

        > cd ~/.vim/bundle/YouCompleteMe
        > ./install.sh --clang-completer

## On Linux: 

        > sudo apt-get install ctags
        > sudo apt-get install ack
        OR
        > sudo yum install ctags
        > sudo yum install ack
    
###    Install gocode for golang syntax highlighting with syntastic

        > go get -u github.com/nsf/gocode
        
Additionally, for golang you must set $GOROOT for YCM to pick up the standard libary in completions.

###    Finish install of YouCompleteMe

        > cd ~/.vim/bundle/YouCompleteMe
        > ./install.sh --clang-completer
