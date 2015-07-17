# Support for both Mac and Ubuntu Linux
# 
#

# OS specific stuff
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Add bash completion
    if [ -f `brew --prefix`/etc/bash_completion ]; then
        . `brew --prefix`/etc/bash_completion
    fi

    # Set architecture flags
    export ARCHFLAGS="-arch x86_64"

    # protect node install when upgrading nvm
    export NVM_DIR=~/.nvm

    # source nvm.sh
    source $(brew --prefix nvm)/nvm.sh

    # Golang 
    export GOROOT=/usr/local/go
    export GOPATH=$HOME/code/go
    
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    # add bash completion
    if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
    fi

    # protect node install when upgrading nvm
    export NVM_DIR=~/.nvm

    # Golang 
    export GOROOT=$HOME/go
    export GOPATH=$HOME/code/go
fi


# bindkey to vim
set -o vi


# Update the Path
export PATH=$GOPATH/bin:$GOROOT/bin:$HOME/bin:$HOME/.node/bin:/usr/local/bin:/usr/local/sbin:$PATH

# add z
. $HOME/code/z/z.sh

# Initialize rbenv
eval "$(rbenv init -)"


# Set my preferred editor
export VISUAL='mvim -v'
export EDITOR='vim'


# Python setup stuff
export PIP_REQUIRE_VIRTUALENV=false
export PIP_DOWNLOAD_CACHE=$HOME/.pip/cache
[ -d $HOME/.virtualenv ] || mkdir -p $HOME/.virtualenv
export WORKON_HOME=$HOME/.virtualenv

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize


# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# add colors to apps
GRC=`which grc`
if [ "$TERM" != dumb ] && [ -n "$GRC" ]
    then
        alias colourify="$GRC -es --colour=auto"
        alias configure='colourify ./configure'
        for app in {diff,make,gcc,g++,mtr,ping,traceroute}; do
            alias "$app"='colourify '$app
    done
fi

# LS_COLORS
if [[ "$OSTYPE" == "darwin"* ]]; then
    eval "$(gdircolors -b ~/.dircolors)"
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    eval "$(dircolors -b ~/.dircolors)"
fi    

# source dotfiles
for file in ~/.{bash_prompt,aliases,functions}; do
    [ -r "$file" ] && source "$file"
done
unset file

# Support the use of GVM for golang versions
[[ -s "$HOME/.gvm/scripts/gvm" ]] && source "$HOME/.gvm/scripts/gvm"
