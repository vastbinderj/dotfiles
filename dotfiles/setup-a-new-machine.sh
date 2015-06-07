##
## new machine setup.
##

if [[ "$OSTYPE" == "darwin"* ]]; then
    # Found Mac OSX

    #
    # homebrew!
    #
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

    # then install things
    ./brew.sh


    # github.com/thebitguru/play-button-itunes-patch
    # disable itunes opening on media keys
    git clone https://github.com/thebitguru/play-button-itunes-patch ~/code/play-button-itunes-patch


    # change to bash 4 (installed by homebrew)
    BASHPATH=$(brew --prefix)/bin/bash
    sudo echo $BASHPATH >> /etc/shells
    chsh -s $BASHPATH # will set for current user only.
    echo $BASH_VERSION # should be 4.x not the old 3.2.X
    # Later, confirm iterm settings aren't conflicting.

    # create GOPATH dirs
    mkdir -p $HOME/go
    mkdir -p $HOME/go/{src,pkg,bin}


elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    # Found Linux

    if [ -f /etc/lsb-release  ]; then
            # Found Ubuntu
            . /etc/lsb-release
            
            # Install stuff
            sudo apt-get update && sudo apt-get install bash-completion build-essential bzr ctags cmake golang grc python-dev rbenv ruby-build silversearcher-ag -y

            # create GOPATH dirs
            mkdir -p $HOME/go
            mkdir -p $HOME/go/{src,pkg,bin}
    fi
fi

# github.com/jamiew/git-friendly
# the `push` command which copies the github compare URL to my clipboard is heaven
bash < <( curl https://raw.github.com/jamiew/git-friendly/master/install.sh)


# github.com/rupa/z   - oh how i love you
git clone https://github.com/rupa/z.git ~/code/z
chmod +x ~/code/z/z.sh
# consider reusing your current .z file if possible. it's painful to rebuild :)
# z hooked up in .bash_profile


# for the c alias (syntax highlighted cat)
sudo easy_install Pygments


# symlinks!
#   put/move git credentials into ~/.gitconfig.local
#   http://stackoverflow.com/a/13615531/89484
./symlink-setup.sh

