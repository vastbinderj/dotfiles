#
#

# OS specific stuff
if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
elif type lsb_release >/dev/null 2>&1; then
    # linuxbase.org
    OS=$(lsb_release -si)
    VER=$(lsb_release -sr)
elif [ -f /etc/lsb-release ]; then
    # For some versions of Debian/Ubuntu without lsb_release command
    . /etc/lsb-release
    OS=$DISTRIB_ID
    VER=$DISTRIB_RELEASE
elif [ -f /etc/debian_version ]; then
    # Older Debian/Ubuntu/etc.
    OS=Debian
    VER=$(cat /etc/debian_version)
else
    # Fall back to uname, e.g. "Linux <version>", also works for BSD, etc.
    OS=$(uname -s)
    VER=$(uname -r)
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
    # Add bash completion
    if [ -f `brew --prefix`/etc/bash_completion ]; then
        . `brew --prefix`/etc/bash_completion
    fi

    # Set architecture flags
    export ARCHFLAGS="-arch x86_64"

    # Golang
    export GOPATH=$HOME/code/go

    # Update the Path
    export PATH=$GOPATH/bin:$HOME/bin:$HOME/.node/bin:/usr/local/bin:/usr/local/sbin:$PATH

elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    # add bash completion
    if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
    fi

    # fix our modifiers in gentoo and arch
    setxkbmap -option 'caps:ctrl_modifier'
    xcape -e 'Caps_Lock=Escape;Control_L=Escape'

    # set an alias for skype to use apulse
    alias  skype='apulse skype'
    # make less more friendly for non-text input files, see lesspipe(1)
    [ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"


    # Golang
    export GOROOT=$HOME/go
    export GOPATH=$HOME/code/go

    # JavaEnv
    export JENVROOT=$HOME/.jenv

    # IDEA
    export IDEAROOT=/opt/idea-IU-173.4548.28

    # Update the Path
    export PATH=$GOROOT/bin:$GOPATH/bin:$HOME/bin:$HOME/.node/bin:$JENVROOT/bin:$IDEAROOT/bin:/usr/local/bin:/usr/local/sbin:$PATH

fi


# bindkey to vim
set -o vi


# add ssh agent on login
if [ ! -S ~/.ssh/ssh_auth_sock  ]; then
    eval `ssh-agent`
    ln -sf "$SSH_AUTH_SOCK" ~/.ssh/ssh_auth_sock
fi
export SSH_AUTH_SOCK=~/.ssh/ssh_auth_sock
#ssh-add -l | grep "The agent has no identities" && ssh-add
ssh-add -l >/dev/null 2>&1


# add z
. $HOME/code/z/z.sh

# Initialize rbenv
if [ -x /usr/local/bin/rbenv ]; then
    eval "$(rbenv init -)"
fi

# Initialize jenv
if [ -x $HOME/.jenv/bin/jenv ]; then
    eval "$(jenv init -)"
fi


# Set my preferred editor
export EDITOR='vim'

# fix for tmux 2.2
export EVENT_NOKQUEUE=1

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

# Base16 Shell
BASE16_SHELL="$HOME/code/vim-hybrid-material/base16-material/base16-material.dark.sh"
[[ -s $BASE16_SHELL  ]] && source $BASE16_SHELL

# source dotfiles
for file in ~/.{bash_prompt,aliases,functions}; do
    [ -r "$file" ] && source "$file"
done
unset file

# add github token to env
export GITHUB_TOKEN=$(git config --get github.token)

# The next line updates PATH for the Google Cloud SDK.
if [ -f "$HOME/code/google-cloud-sdk/path.bash.inc" ]
    then source "$HOME/code/google-cloud-sdk/path.bash.inc"
fi

# Enables shell command completion for gcloud if it exists
if [ -f "$HOME/code/google-cloud-sdk/completion.bash.inc" ]
   then source "$HOME/code/google-cloud-sdk/completion.bash.inc"
fi

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
