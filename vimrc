set nocompatible

" Call Pathogen
filetype off 
call pathogen#incubate()
call pathogen#helptags()

filetype on
filetype plugin on
filetype plugin indent on

" Set the Map Leader
let mapleader=","

syntax enable
set background=dark
set encoding=utf-8
set guifont=Menlo\ For\ Powerline:14
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
set cursorline
set ruler
set showcmd
set cmdheight=2
set encoding=utf8
set mat=2
" Enable Code Folding
set foldmethod=indent
set foldlevel=99

set laststatus=2
set t_Co=256
let g:Powerline_symbols = 'fancy'

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

"Scala Tagbar configuration
let g:tagbar_type_scala = {
    \ 'ctagstype' : 'Scala',
    \ 'kinds'     : [
        \ 'p:packages:1',
        \ 'V:values',
        \ 'v:variables',
        \ 'T:types',
        \ 't:traits',
        \ 'o:objects',
        \ 'a:aclasses',
        \ 'c:classes',
        \ 'r:cclasses',
        \ 'm:methods'
    \ ]
\ }
 
" Mapping for Tasklist
map <leader>td <Plug>TaskList

"NerdTreeToggle
map <leader>nt <plug>NERDTreeTabsToggle<CR>

" Bind F4 to :TlistToggle
nnoremap <F4> :TlistToggle<CR>
let Tlist_Use_Right_Window = 1

" Bind F6 to CTAGS
nnoremap <F6> :!/usr/local/bin/ctags -R --exclude=.git --exclude=log *<CR>

" Bind F8 to Tagbar
nnoremap <F8> :TagbarToggle<CR>

" Rope Mappings
nnoremap <,g> :RopeGotoDefinition<CR>
nnoremap <,r> :RopeRename<CR>

"Fuzzy Finder
nnoremap <C-f><C-f> :FufFile<CR>

" Ack
nnoremap <,a> <Esc>:Ack!

" CTRL-P
let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd = 'CtrlP'
let g:ctrlp_working_path_mode = 'ra'         " Working Directory
set wildignore+=*/tmp/*,*.so,*.swp,*.zip     " MacOSX/Linux
let g:ctrlp_user_command = 'find %s -type f'
let g:ctrlp_custom_ignore = {
            \ 'dir':  '\v[\/]\.(git|hg|svn)$',
            \ 'file': '\v\.(exe|so|dll)$',
            \ 'link': 'some_bad_symbolic_links',
            \ }

" Pep8 Mapping
let g:pep8_map=',p8'

" Ultisnips
let g:UltiSnipsUsePythonVersion = 2

" NodeJS Completion Settings
let g:nodejs_complete_config = {
            \ 'js_compl_fn': 'jscomplete#CompleteJS',
            \ 'max_node_compl_len': 15 
            \ }

" Configure SuperTab
let g:SuperTabDefaultCompletionType = "context"
set completeopt=menuone,menu,longest

" Enable Omni complete
if has("autocmd")
    autocmd FileType ruby,eruby set omnifunc=rubycomplete#Complete
    autocmd FileType ruby,eruby let g:rubycomplete_buffer_loading = 1
    autocmd FileType ruby,eruby let g:rubycomplete_classes_in_global = 1
    autocmd FileType ruby,eruby let g:rubycomplete_rails = 1

    autocmd FileType python set omnifunc=pythoncomplete#Complete

    autocmd FileType php let php_sql_query=1
    autocmd FileType php let php_htmlInStrings=1
    autocmd FileType php set omnifunc=phpcomplete#CompletePHP
    autocmd FileType html set omnifunc=htmlcomplete#CompleteTags
    autocmd FileType css set omnifunc=csscomplete#CompleteCSS
    autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS

    autocmd FileType c set omnifunc=ccomplete#Complete
endif


"Improve autocomplete menu color
highlight   clear
highlight   Pmenu         ctermfg=0 ctermbg=2
highlight   PmenuSel      ctermfg=0 ctermbg=7
highlight   PmenuSbar     ctermfg=7 ctermbg=0
highlight   PmenuThumb    ctermfg=0 ctermbg=7

" JavaScript 
let g:html_indent_inctags = "html,body,head,tbody"
let g:html_indent_script1 = "inc"
let g:html_indent_style1 = "inc"

" Node.js dictionary 
au FileType javascript set dictionary+=$HOME/.vim/bundle/vim-node/dict/node.dict

" Recompile a Coffee file when saved
au BufWritePost *.coffee silent CoffeeMake! -b | cwindow | redraw!


" jQuery Syntax
au BufRead,BufNewFile jquery.*.js set ft=javascript syntax=jquery

" set the default color scheme
colors molokai
