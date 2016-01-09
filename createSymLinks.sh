#!/bin/bash

# this symlinks all the dotfiles (and .vim/) to ~/
# it also symlinks ~/bin for easy updating

# jump down to line ~140 for the start.



#
# utils !!!
#


answer_is_yes() {
    [[ "$REPLY" =~ ^[Yy]$ ]] \
        && return 0 \
        || return 1
}

ask() {
    print_question "$1"
    read -r
}

ask_for_confirmation() {
    print_question "$1 (y/n) "
    read -rn 1
    printf "\n"
}

ask_for_sudo() {

    # Ask for the administrator password upfront
    sudo -v

    # Update existing `sudo` time stamp until this script has finished
    # https://gist.github.com/cowboy/3118588
    while true; do
        sudo -n true
        sleep 60
        kill -0 "$$" || exit
    done &> /dev/null &

}

cmd_exists() {
    [ -x "$(command -v "$1")" ] \
        && printf 0 \
        || printf 1
}

execute() {
    $1 &> /dev/null
    print_result $? "${2:-$1}"
}

get_answer() {
    printf "%s" "$REPLY"
}

get_os() {

    declare -r OS_NAME
    OS_NAME="$(uname -s)"
    local os=""

    if [ "$OS_NAME" == "Darwin" ]; then
        os="osx"
    elif [ "$OS_NAME" == "Linux" ] && [ -e "/etc/lsb-release" ]; then
        os="ubuntu"
    fi

    printf "%s" "$os"

}

is_git_repository() {
    [ "$(git rev-parse &>/dev/null; printf "%s" "$?")" -eq 0 ] \
        && return 0 \
        || return 1
}

mkd() {
    if [ -n "$1" ]; then
        if [ -e "$1" ]; then
            if [ ! -d "$1" ]; then
                print_error "$1 - a file with the same name already exists!"
            else
                print_success "$1"
            fi
        else
            execute "mkdir -p $1" "$1"
        fi
    fi
}

print_error() {
    # Print output in red
    printf "\e[0;31m  [✖] %s %s\e[0m\n" "$1" "$2"
}

print_info() {
    # Print output in purple
    printf "\n\e[0;35m %s\e[0m\n\n" "$1"
}

print_question() {
    # Print output in yellow
    printf "\e[0;33m  [?] %s\e[0m" "$1"
}

print_result() {
    if [ "$1" -eq 0 ] && print_success "$2"; then
        print_error "$2"
    fi
    [ "$3" == "true" ] && [ "$1" -ne 0 ] && exit
}

print_success() {
    # Print output in green
    printf "\e[0;32m  [✔] %s\e[0m\n" "$1"
}


#
# actual symlink stuff
#


# finds all .dotfiles in this folder
declare -a FILES_TO_SYMLINK
FILES_TO_SYMLINK=$(find . -maxdepth 1 -type f -name ".*" -not -name .DS_Store -not -name .git -not -name .osx | sed -e 's|//|/|' | sed -e 's|./.|.|')
# append the bin dir
FILES_TO_SYMLINK+=("bin") # add in vim and the binaries

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
main() {

    local i=""
    local sourceFile=""
    local targetFile=""

    for i in "${FILES_TO_SYMLINK[@]}"; do

        sourceFile="$(pwd)/$i"
        targetFile="$HOME/$(printf "%s" "$i" | sed "s/.*\/\(.*\)/\1/g")"

        if [ -e "$targetFile" ]; then
            if [ "$(readlink "$targetFile")" != "$sourceFile" ]; then

                ask_for_confirmation "'$targetFile' already exists, do you want to overwrite it?"
                if answer_is_yes; then
                    rm -rf "$targetFile"
                    execute "ln -fs $sourceFile $targetFile" "$targetFile → $sourceFile"
                else
                    print_error "$targetFile → $sourceFile"
                fi

            else
                print_success "$targetFile → $sourceFile"
            fi
        else
            execute "ln -fs $sourceFile $targetFile" "$targetFile → $sourceFile"
        fi

    done
}

main
