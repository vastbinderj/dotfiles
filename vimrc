" Call Pathogen
filetype off 
call pathogen#runtime_append_all_bundles()
call pathogen#helptags()

set nocompatible
set runtimepath+=~/.vim/UltiSnips-1.4

" Install the latest updates
let g:GetLatestVimScripts_allowautoinstall=1

filetype plugin indent on
"filetype off 
"call pathogen#runtime_append_all_bundles()
"call pathogen#helptags()

let mapleader=","

syntax on
colorscheme lucius
"colorscheme mustang
set background=dark
set gfn=Monaco:h10
set nowrap
set tabstop=4
set shiftwidth=4
set expandtab
set softtabstop=4
set smarttab
set smartindent
set autoindent
set hlsearch
set incsearch
set showmatch
set number
set title
set nobackup
set noswapfile
set history=1000
set undolevels=1000
set wildignore=*.swp,*.bak,*.pyc,*.class

" Enable Code Folding
set foldmethod=indent
set foldlevel=99

" Set the Window Size
if has("gui_running")
    set lines=50 columns=100
else
    if exists("+lines")
        set lines=50
    endif
    if exists("+columns")
        set columns=100
    endif
endif
 
" Bind F6 to CTAGS
nnoremap <F6> :!/opt/local/bin/ctags -R --python-kinds=-i *.py<CR>

" Bind F4 to :TlistToggle
nnoremap <F4> :TlistToggle<CR>
let Tlist_Use_Right_Window = 1

" Enable Omni complete
" autocmd FileType python set omnifunc=pythoncomplete#Complete
" inoremap <C-space> <C-x><C-o>
autocmd FileType ruby set omnifunc=ruby#Complete
autocmd FileType python set omnifunc=pythoncomplete#Complete
autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS
autocmd FileType html set omnifunc=htmlcomplete#CompleteTags
autocmd FileType css set omnifunc=csscomplete#CompleteCSS
let g:SuperTabDefaultCompletionType = "context"
set completeopt=menuone,longest,preview

" Rope Mappings
nnoremap <,g> :RopeGotoDefinition<CR>
nnoremap <,r> :RopeRename<CR>

"Fuzzy Finder
nnoremap <C-f><C-f> :FufFile<CR>

" Ack
nnoremap <,a> <Esc>:Ack!

"NerdTreeToggle
nnoremap <F3> :NERDTreeToggle<CR>

" Pep8 Mapping
let g:pep8_map=',p8'

" Add the virtualenv's site-packages to vim path
python << EOF
import os.path
import sys
import vim
if 'VIRTUAL_ENV' in os.environ:
    project_base_dir = os.environ['VIRTUAL_ENV']
    sys.path.insert(0, project_base_dir)
    activate_this = os.path.join(project_base_dir, 'bin/activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))
EOF

