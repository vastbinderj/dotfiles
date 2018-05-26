#!/usr/bin/env bash
# Remove previous installations

sudo apt-get remove vim vim-runtime vim-tiny vim-common

# Install dependencies

sudo apt-get install libncurses5-dev python-dev liblua5.3-dev luajit libluajit-5.3 lua5.3 python3-dev

# Fix liblua paths

# You have to compile luajit for yourself.

sudo ln -s /usr/include/lua5.3 /usr/include/lua

sudo ln -s /usr/lib/x86_64-linux-gnu/liblua5.3.so /usr/local/lib/liblua.so



# Clone vim sources

cd ~/code

git clone https://github.com/vim/vim.git



cd vim



./configure \
    --enable-luainterp \
    --with-luajit \
    --enable-python3interp \
    --with-python3-config-dir=/usr/lib/python3.6/config-3.6m-x86_64-linux-gnu/ \
    --enable-cscope \
    --disable-netbeans \
    --enable-terminal \
    --disable-xsmp \
    --enable-fontset \
    --enable-multibyte \
    --enable-fail-if-missing \
    --with-compiledby=vastbinderj \
    --with-modified-by=vastbinderj
    # --enable-pythoninterp \
    # --with-python-config-dir=/usr/lib/python2.7/config-x86_64-linux-gnu/ \



    make VIMRUNTIMEDIR=/usr/local/share/vim/vim81



    sudo apt-get install checkinstall

    sudo checkinstall
