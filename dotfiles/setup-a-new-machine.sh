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

            # Add PPAs
            sudo add-apt-repository ppa:neovim-ppa/unstable -y
            sudo apt-get update
            
            # Install stuff
            sudo apt-get update && sudo apt-get install \
                # packages to install 
                bash-completion \
                build-essential \
                bzr \
                ctags \
                cmake \
                golang \
                grc \
                neovim \
                python-dev \
                python-setuptools \
                python3-dev \
                python3-setuptools \
                rbenv \
                ruby-build \
                silversearcher-ag \
                # tags for apt-get install
                -y

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


# clone vundle in ~/.vim/bundle
git clone https://github.com/gmarik/Vundle.vim.git $HOME/.vim/bundle/Vundle.vim


# install vundle packages in vim
vim +PluginInstall +qall

# build YouCompleteMe
if [ -f $HOME/.vim/bundle/YouCompleteMe/install.sh  ]; then
    $HOME/.vim/bundle/YouCompleteMe/install.sh --clang-completer
fi


# symlinks!
#   put/move git credentials into ~/.gitconfig.local
#   http://stackoverflow.com/a/13615531/89484
./symlink-setup.sh

