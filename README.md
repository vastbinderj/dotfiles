This is my personal collection of dotfiles for golang/rails/node development.  I use Vundle for plugin management and I use [YouCompleteMe](https://github.com/Valloric/YouCompleteMe) for code completion and my mapleader is a ','.  Be sure to read through the .vimrc file for key mappings, as they are set to ones which suite me best. This configuration works well vim 7.4 or neovim installed with hombrew on my macs, but these work well with vim 7.2+ on Cent OS and Ubuntu, which are my primary development environments at work.

## Installation for a Mac and Ubuntu Linux 
(redhat/centos coming soon)

        > mkdir -p $HOME/code
        > git clone https://github.com/vastbinderj/dotfiles.git ~/code/dotfiles
        > cd $HOME/dotfiles
        > ./setupNewRig.sh                  # this sets up a mac or x64 linux server
        > exec -l $SHELL                    # checkout the shiny new prompt
        > ./installGolang.sh                # build golang from source
        > ./setupVim.sh                     # configure vim and install plugins

## Manual steps for just setting up vim

### Clone Vundle into bundle/ and install all Plugins

        > ln -s $HOME/code/dotfiles/.vimrc $HOME/.vimrc
        > cd ~/.vim
        > git clone https://github.com/gmarik/Vundle.vim.git bundle/Vundle.vim
        > vim +PluginInstall +qall

###    Finish install of YouCompleteMe

        > cd ~/.vim/bundle/YouCompleteMe
        > ./install.py --clang-completer 

### To upgrade all bundled plugins at any time:

Open vim and run `:PluginUpdate` or `:PluginInstall!` 

## dotfiles included

        - bash_profile (for mac)
        - bashrc       (for linux & mac)
        - vimrc
        - gemrc
        - jshintrc
        - npmrc 
        - tmux.conf    (prefix set to ctrl-a and vim key-mappings)
        

* To enable mouse scrolling on a mac in terminal, install [easySIMBL](https://github.com/norio-nomura/EasySIMBL) and [mouseterm](https://bitheap.org/mouseterm/) or use iTerm.  I use iTerm and have installed [patched fonts](https://github.com/Lokaltog/powerline-fonts) for airline and my tmuxline.

* For golang development, I use [vim-go](https://github.com/fatih/vim-go) which does many things for me like auto-imports, gofmt upon save and provides easy jump mappings to quickly browse source code.  


* Mappings for Escape in Vim
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
  * C-a,| to split a pane vertically
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
