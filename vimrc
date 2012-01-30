set nocompatible

" Call Pathogen
filetype off 
call pathogen#runtime_append_all_bundles()
call pathogen#helptags()

filetype on
filetype plugin on
filetype plugin indent on

" Set the Map Leader
let mapleader=","

syntax on
set background=dark
set gfn=Monaco:h10
colors xoria256
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
set relativenumber
set title
set nobackup
set noswapfile
set history=1000
set undolevels=1000
set wildignore=*.swp,*.bak,*.pyc,*.class

" Add a git statusline 
set statusline=%<\ %f\ %{fugitive#statusline()}

" Enable Code Folding
set foldmethod=indent
set foldlevel=99

" Window Movement with split windows
map <c-j> <c-w>j
map <c-k> <c-w>k
map <c-l> <c-w>l
map <c-h> <c-w>h

" Set the Window Size
if has("gui_running")
    set lines=50 columns=132
else
    if exists("+lines")
        set lines=50
    endif
    if exists("+columns")
        set columns=132
    endif
endif

" Functions to easily mark and swap windows
function! MarkWindowSwap()
    let g:markedWinNum = winnr()
endfunction

function! DoWindowSwap()
    "Mark destination
    let curNum = winnr()
    let curBuf = bufnr( "%" )
    exe g:markedWinNum . "wincmd w"
    "Switch to source and shuffle dest->source
    let markedBuf = bufnr( "%" )
    "Hide and open so that we aren't prompted and keep history
    exe 'hide buf' curBuf
    "Switch to dest and shuffle source->dest
    exe curNum . "wincmd w"
    "Hide and open so that we aren't prompted and keep history
    exe 'hide buf' markedBuf 
endfunction

nnoremap <silent> <Leader>mw :call MarkWindowSwap()<CR>
nnoremap <silent> <Leader>pw :call DoWindowSwap()<CR>
 
" Bind F6 to CTAGS
nnoremap <F6> :!/opt/local/bin/ctags -R --python-kinds=-i *.py<CR>

" CommandT stuff
nnoremap <silent> <Leader>ct :CommandT<CR>
nnoremap <silent> <Leader>cb :CommandTBuffer<CR>

" Mapping for Tasklist
map <leader>td <Plug>TaskList

" Bind F4 to :TlistToggle
nnoremap <F4> :TlistToggle<CR>
let Tlist_Use_Right_Window = 1


" Enable Omni complete
if has("autocmd")
    autocmd FileType ruby,eruby set omnifunc=rubycomplete#Complete
    autocmd FileType ruby,eruby let g:rubycomplete_buffer_loading = 1
    autocmd FileType ruby,eruby let g:rubycomplete_classes_in_global = 1
    autocmd FileType ruby,eruby let g:rubycomplete_rails = 1

    autocmd FileType python set omnifunc=pythoncomplete#Complete
    autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS
    autocmd FileType html set omnifunc=htmlcomplete#CompleteTags
    autocmd FileType css set omnifunc=csscomplete#CompleteCSS
endif
let g:SuperTabDefaultCompletionType = "context"
set completeopt=menuone,longest,preview

"improve autocomplete menu color
highlight PMenu gui=bold guibg=#CECECE guifg=#444444

" jQuery Syntax
au BufRead,BufNewFile jquery.*.js set ft=javascript syntax=jquery

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
