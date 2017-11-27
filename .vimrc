" set
set nocompatible

" Vundle Setup
filetype off
set runtimepath+=~/.vim/bundle/Vundle.vim
call vundle#begin('~/.vim/bundle')

Plugin 'gmarik/Vundle.vim'

" L9
Plugin 'vim-scripts/L9'

" Color Schemes
Plugin 'flazz/vim-colorschemes'

" CTRL P
Plugin 'ctrlpvim/ctrlp.vim'

" Ag
Plugin 'rking/ag.vim'

" Gsearch
Plugin 'skwp/greplace.vim'

" Bracketed Paste
Plugin 'ConradIrwin/vim-bracketed-paste'

" AutoPairs
Plugin 'jiangmiao/auto-pairs'

" base16-vim colorschemes
Plugin 'chriskempson/base16-vim'

" Emmet
Plugin 'mattn/emmet-vim'

" Fugitive
Plugin 'tpope/vim-fugitive'

" Git
Plugin 'tpope/vim-git'

" Gundo
Plugin 'sjl/gundo.vim'

" Java Completion
Plugin 'artur-shaik/vim-javacomplete2'

" JSHint
Plugin 'wookiehangover/jshint.vim'

" List Toggle
Plugin 'Valloric/ListToggle'

" Markdown from PlasticBoy
Plugin 'plasticboy/vim-markdown'

" Mustache
Plugin 'juvenn/mustache.vim'

" Nerdtree
Plugin 'vim-scripts/The-NERD-tree'

" Repeat
Plugin 'tpope/vim-repeat'

" Surround
Plugin 'tpope/vim-surround'

" Ale
Plugin 'w0rp/ale'

" Tabular
Plugin 'godlygeek/tabular'

" Tagbar
Plugin 'majutsushi/tagbar'

" Tasklist
Plugin 'vim-scripts/TaskList.vim'

" TmuxLine
Plugin 'edkolev/tmuxline.vim'

" Vim-Airline
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'

" Coffescript
Plugin 'kchmck/vim-coffee-script'

" EasyMotion
Plugin 'Lokaltog/vim-easymotion'

" GitGutter
Plugin 'airblade/vim-gitgutter'

" Vim-Go
Plugin 'fatih/vim-go'

" HTML5 Support
Plugin 'othree/html5.vim'

" Indent Guides
Plugin 'nathanaelkane/vim-indent-guides'

" Syntax for JavaScript
Plugin 'othree/javascript-libraries-syntax.vim'

" JSON
Plugin 'elzr/vim-json'

" NerdTree Tabs
Plugin 'jistr/vim-nerdtree-tabs'

" NerdTree Commenter
Plugin 'scrooloose/nerdcommenter'

" Node
Plugin 'guileen/vim-node'

" Node Completion
Plugin 'myhere/vim-nodejs-complete'

" Snippets
Plugin 'honza/vim-snippets'

" Unviversal Text Linking
Plugin 'vim-scripts/utl.vim'

" SyntaxRange
Plugin 'vim-scripts/SyntaxRange'

" SpeedDating
Plugin 'tpope/vim-speeddating'

" TMUX Navigator
Plugin 'christoomey/vim-tmux-navigator'

" Unimpaired
Plugin 'tpope/vim-unimpaired'

" NeoComplete
if has("nvim")
    Plugin 'Shougo/deoplete.nvim'
else
    Plugin 'Shougo/neocomplete.vim'
endif

" NeoSnippet
Plugin 'Shougo/neosnippet.vim'
Plugin 'Shougo/neosnippet-snippets'

" End Vundle Installed Plugins
call vundle#end()

" set mouse if possible
if has('mouse')
    set mouse+=a
endif
"tmux knows extended mouse mode
if &term =~ '^screen'
  set ttymouse=xterm2
endif

" turn filetype and syntax back on
filetype plugin indent on
syntax on

" when vimrc is edited, reload it
autocmd! BufWritePost vimrc source ~/.vimrc

set encoding=utf-8

set clipboard^=unnamed
set clipboard^=unnamedplus
set tabstop=4
set shiftwidth=4
set expandtab
set softtabstop=4
set smarttab
set hlsearch
set incsearch
set showmatch
set matchtime=5
set number
set title
set nobackup
set noswapfile
set history=1000
set undolevels=1000
set wildignore=*.swp,*.bak,*.pyc,*.class
set cursorline
set ruler
set wildmenu
set showcmd
set showfulltag
set cmdheight=2
set encoding=utf8
set scrolloff=5
set mat=2
set splitright
set foldmethod=indent           " Enable Code Folding
set foldlevel=99
set wrap
set textwidth=120

set laststatus=2
set t_Co=256


" airline settings
let g:airline_powerline_fonts = 1
let g:airline#extensions#whitespace#enabled = 0
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#left_sep = ' '
let g:airline#extensions#tabline#left_alt_sep = '|'
let g:airline_left_sep = ' '
let g:airline_right_sep = ' '
let g:airline_theme = "base16_ocean"
"nmap <Plug>AirlineTablineRefresh :set mod!<CR>

"======================================
" Function Key Maps
"======================================

" <F1>: Help
nmap <F1> [unite]h

" <F2>: Gundo
nnoremap <F2> :<C-u>GundoToggle<cr>

" <F3>: Save Session
nnoremap <F3> :<C-u>UniteSessionSave

" <F5>: Toggle Indent Guides
nnoremap <F5> :<C-u>IndentGuidesToggle<cr>

" <F6>: Generate CTAGS
nnoremap <F6> :!ctags -R --exclude=.git --exclude=log *<CR>

"======================================
" Leader Key Maps
"======================================


" Set the Map Leader
let mapleader =","
let g:mapleader =","
let maplocalleader=","
let g:maplocalleader=","

" Toggle Paste mode
nnoremap <silent> <Leader>1 :set paste!<cr>

" Toggle Tagbar
nnoremap <silent> <Leader>2  :TagbarToggle<CR>

" Quit all
nnoremap <Leader>q :qa<cr>

" Close Current Buffer
nnoremap <Leader>wc :NERDTreeClose<cr>:bdelete<cr>

"NerdTreeToggle
map <leader>nt <plug>NERDTreeTabsToggle<CR>


"==================================
" Fugitive Maps
"==================================

nnoremap <space>ga :Git add %:p<cr><cr>
nnoremap <space>gs :Gstatus<cr>
nnoremap <space>gc :Gcommit -v -q<cr>
nnoremap <space>gt :Gcommit -v -q %:p<cr>
nnoremap <space>gd :Gdiff<cr>
nnoremap <space>ge :Gedit<cr>
nnoremap <space>gr :Gread<cr>
nnoremap <space>gw :Gwrite<cr><cr>
nnoremap <space>gl :silent! Glog<cr>:bot copen<cr>
nnoremap <space>gp :Ggrep<space>
nnoremap <space>gm :Gmove<space>
nnoremap <space>gb :Git branch<space>
nnoremap <space>go :Git checkout<space>
nnoremap <space>gps :Git push<cr>
nnoremap <space>gpl :Git pull<cr>

"===================================
" Neovim Maps
"==================================

" to move from neovim terminal window to another window
if has ('nvim')
    tnoremap <C-h> <C-\><C-n><C-w>h
    tnoremap <C-j> <C-\><C-n><C-w>j
    tnoremap <C-k> <C-\><C-n><C-w>k
    tnoremap <C-l> <C-\><C-n><C-w>l

    " mapping to enter command mode in terminal
    tnoremap <Leader>e <C-\><C-n>

    " open a terminal below the current buffer
    nnoremap <space>o :below 15sp term://$SHELL<cr>

    " enter insert mode when cycling back to a terminal window
    autocmd WinEnter term://* startinsert
endif

"===================================
" MacVim stuff
"===================================

if has("gui_macvim")
    set macmeta
    set guifont=Source\ Code\ Pro\ for\ Powerline:h13
    set clipboard+=unnamed
    set vb t_vb=

    " Open goto symbol on current buffer
    nmap <D-r> :MyCtrlPTag<cr>
    imap <D-r> <esc>:MyCtrlPTag<cr>

    " Open goto symbol on all buffers
    nmap <D-R> :CtrlPBufTagAll<cr>
    imap <D-R> <esc>:CtrlPBufTagAll<cr>
else
    " open goto symbols
    nmap <Leader>r :MyCtrlPTag<cr>
    imap <Leader>r <esc>:MyCtrlPTag<cr>

    " Open goto symbol on all buffers
    nmap <Leader>R :CtrlPBufTagAll<cr>
    imap <Leader>R <esc>:CtrlPBufTagAll<cr>

endif

"==================================
" Window Movement
"==================================

" move around windows with ctrl key
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-l> <C-w>l
map <C-h> <C-w>h

" Mappings for two-handed save
" insert to normal mode save
inoremap ;a <ESC>:w<CR>
inoremap ;d <ESC>:update<CR>
" insert to normal to insert
inoremap ;f <C-O>:w<CR>
" normal to nomal mode save
nnoremap ;f :w<CR>

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

nnoremap <silent> <Leader>wm :call MarkWindowSwap()<CR>
nnoremap <silent> <Leader>ws :call DoWindowSwap()<CR>

" map escape to jk
:imap jk <Esc>

" toggle the numbering in the gutter
function! NumberToggle()
  if(&relativenumber == 1)
    set norelativenumber
  else
    set relativenumber
  endif
endfunc

nnoremap <C-n> :call NumberToggle()<cr>

"============================
" Tagbar config
"============================

" open on the left
let g:tagbar_left = 1

" autoclose tagbar on selection
let g:tagbar_autoclose = 1

" give tagbar focus when opened
let g:tagbar_autofocus = 1

" Scala Tagbar configuration
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

" Go tagbar config
let g:tagbar_type_go = {
    \ 'ctagstype' : 'go',
    \ 'kinds'     : [
        \ 'p:package',
        \ 'i:imports:1',
        \ 'c:constants',
        \ 'v:variables',
        \ 't:types',
        \ 'n:interfaces',
        \ 'w:fields',
        \ 'e:embedded',
        \ 'm:methods',
        \ 'r:constructor',
        \ 'f:functions'
    \ ],
    \ 'sro' : '.',
    \ 'kind2scope' : {
        \ 't' : 'ctype',
        \ 'n' : 'ntype'
    \ },
    \ 'scope2kind' : {
        \ 'ctype' : 't',
        \ 'ntype' : 'n'
    \ },
    \ 'ctagsbin'  : 'gotags',
    \ 'ctagsargs' : '-sort -silent'
\ }

" Tag path
set tags=./tags,tags;$HOME

"=====================================
" Golang vim-go config
"=====================================

" Golang customizations
let g:go_fmt_command = "goimports"
let g:go_fmt_fail_silently = 1
let g:go_bin_path = expand("$HOME/code/go/bin")
let g:go_auto_type_info = 1

" Syntax Highlighting for Golang
let g:go_highlight_functions = 1
let g:go_highlight_methods = 1
let g:go_highlight_structs = 1
let g:go_highlight_interfaces = 1
let g:go_highlight_operators = 1
let g:go_highlight_build_constraints = 1

" generate go ctags upon save
au BufWritePost *.go,*.js,*.rb,*.py silent! !ctags -R --exclude=*.html 2> /dev/null &
let g:godef_same_file_in_same_window=1                              " when in go, just move the cursor if in same file
autocmd FileType go setlocal shiftwidth=8 tabstop=8 softtabstop=8   " set tabstop to 8 for go files
autocmd FileType go setlocal noexpandtab                            " don't expand tabs to spaces for go files
" Go keymaps
" Type Info
au FileType go nmap <Leader>i <Plug>(go-info)
" GoDoc
au FileType go nmap <Leader>gd <Plug>(go-doc)
au Filetype go nmap <Leader>gv <Plug>(go-doc-vertical)
" Build/Run/Test
au FileType go nmap <Leader>r <Plug>(go-run)
au FileType go nmap <Leader>b <Plug>(go-build)
au FileType go nmap <Leader>t <Plug>(go-test)
" GoDef
au FileType go nmap gd <Plug>(go-def)
au FileType go nmap <Leader>gs <Plug>(go-def-split)
au FileType go nmap <Leader>gv <Plug>(go-def-vertical)
au FileType go nmap <Leader>gt <Plug>(go-def-tab)

" mapping for tasks in current file
map <leader>Tt <Plug>TaskList
let g:tlWindowPosition = 1                                          " set the window postion below
" mapping for tasks in project
noremap <Leader>Tp :noautocmd vimgrep /TODO/j **/**<CR>:cw<CR>

"===========================================
" Easy Motion Maps
"===========================================

" easymotion leader binding
map <Leader><Leader> <Plug>(easymotion-prefix)

map <Leader><Leader>l <Plug>(easymotion-lineforward)
map <Leader><Leader>j <Plug>(easymotion-j)
map <Leader><Leader>k <Plug>(easymotion-k)
map <Leader><Leader>h <Plug>(easymotion-linebackward)

let g:EasyMotion_startofline = 0
let g:EasyMotion_smartcase = 1

" For local replace
nnoremap gr gd[{V%::s/<C-R>///gc<left><left><left>

" For global replace
nnoremap gR gD:%s/<C-R>///gc<left><left><left>

" List Toggle
let g:lt_height = 5

"Fuzzy Finder
nnoremap <C-f><C-f> :FufFile<CR>

" Diff Options
set diffopt=vertical

" Trigger configuration for snippets
let g:ycm_key_list_select_completion=[]
let g:ycm_key_list_previous_completion=[]

" Trigger configuration, do not use <tab>
let g:UltiSnipsExpandTrigger="<c-tab>"
let g:UltiSnipsJumpForwardTrigger="<c-b>"
let g:UltiSnipsJumpBackwardTrigger="<c-z>"
"
" " If you want :UltiSnipsEdit to split your window.
let g:UltiSnipsEditSplit="vertical"

"==========================
" The Silver Searcher
"==========================
" Ack
" bind \ (backward slash) to grep shortcut
command -nargs=+ -complete=file -bar Ag silent! grep! <args>|cwindow|redraw!
nnoremap \ :Ag<SPACE>

" Gsearch
set grepprg=ag\ --nogroup\ --nocolor
let g:grep_cmd_opts = '--line-numbers --noheading'

" bind K to grep word under cursor
nnoremap K :grep! "\b<C-R><C-W>\b"<CR>:cw<CR>k

"===============
" CTRL-P
"===============
set wildignore+=*/.git/*,*/.idea/*,*/.DS_Store,*/node_modules/*,*/bower_components/*.so,*.swp,*.zip
let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd = 'CtrlP'
let g:ctrlp_max_files = 0
let g:ctrlp_match_window = 'top,order:ttb,min:1,max:10,results:10'
let g:ctrlp_working_path_mode = '0'         " Current Working Directory
let g:ctrlp_user_command = 'ag %s -l --nocolor -g ""'
let g:ctrlp_use_caching = 0                 " ag is fast enough we don't need caching
let g:ctrlp_custom_ignore = {
            \ 'dir':  '\v[\/](\.(git|idea|sass-cache)|node_modules|bower_components|dist)$',
            \ 'file': '\v\.(exe|so|dll)$',
            \ 'link': 'some_bad_symbolic_links',
            \ }
let g:ctrlp_buftag_types={'go': '--language-force=go --golang-types=ftv', 'javascript': '--langauge-force=js'}
" Easy bindings for its various modes
nmap <leader>bb :CtrlPBuffer<cr>
nmap <leader>bm :CtrlPMixed<cr>
nmap <leader>bs :CtrlPMRU<cr>
nmap <leader>b. :CtrlPBufTag<cr>

func! MyCtrlPTag()
  let g:ctrlp_prompt_mappings = {
        \ 'AcceptSelection("e")': ['<cr>', '<2-LeftMouse>'],
        \ 'AcceptSelection("t")': ['<c-t>'],
        \ }
  CtrlPBufTag
endfunc
command! MyCtrlPTag call MyCtrlPTag()

" List Toggle Settings
let g:lt_location_list_toggle_map = '<leader>Tl'
let g:lt_quickfix_list_toggle_map = '<leader>Tq'

" Toggle auto-pairs
let g:AutoPairsShortcutToggle = '<leader>Ta'

" NodeJS Completion Settings
let g:nodejs_complete_config = {
            \ 'js_compl_fn': 'jscomplete#CompleteJS',
            \ 'max_node_compl_len': 15
            \ }

" Syntastic settings
"let g:syntastic_error_symbol = '✘'
"let g:syntastic_warning_symbol = '✘'
"let g:syntastic_style_error_symbol = '≋'
"let g:syntastic_style_warning_symbol = '≈'
"let g:syntastic_go_checkers = ['golint']                       " use golint for syntax checking in Go
"let g:syntastic_loc_list_height = 5                            " set error window height to 5
"let g:syntastic_always_populate_loc_list = 1                   " stick errors into a location-list
"let g:syntastic_html_tidy_exec = 'tidy5'
"let g:syntastic_html_tidy_ignore_errors=[" proprietary attribute " ,"trimming empty <", "unescaped &" , "lacks \"action", "is not recognized!", "discarding unexpected"]

"=======================
" Ale for linting
"======================
let g:ale_sign_column_always = 1                                " keep the sign gutter open
let g:ale_sign_error = '>>'
let g:ale_sign_warning = '--'
let g:ale_open_list = 1                                         " open loc list
nmap <silent> '<leader>k' <Plug>(ale_previous_wrap)             " navigate errors
nmap <silent> '<leader>j' <Plug>(ale_next_wrap)

" Do not lint or fix minified files.
let g:ale_pattern_options = {
\ '\.min\.js$': {'ale_linters': [], 'ale_fixers': []},
\ '\.min\.css$': {'ale_linters': [], 'ale_fixers': []},
\}

"====================================
" DeoComplete for Neovim and Settings
"====================================
" turn of omnifunc
let g:acp_enableAtStartup = 0
" neovim
if has('nvim')
    set omnifunc=syntaxcomplete#Complete
    let g:deoplete#enable_at_startup = 1
    let g:deoplete#ignore_sources = {}
    let g:deoplete#ignore_sources._ = ['buffer', 'member', 'tag', 'file', 'neosnippet']
    let g:deoplete#omni_patterns = {}
    let g:deoplete#omni_patterns.java = '[^. *\t]\.\w*'
    let g:deoplete#sources = {}
    let g:deoplete#sources._ = []
    let g:deoplete#file#enable_bugger_path = 1
    let g:deoplete#sources#go#sort_class = ['func', 'type', 'var', 'const']
    let g:deoplete#sources#go#align_class = 1

    " Use partial fuzzy matches like YouCompleteMe
    call deoplete#custom#set('_', 'matchers', ['matcher_fuzzy'])
    call deoplete#custom#set('_', 'converters', ['converter_remove_paren'])
    call deoplete#custom#set('_', 'disabled_syntaxes', ['Comment', 'String'])
else
    let g:neocomplete#enable_at_startup = 1
    let g:neocomplete#enable_smart_case = 1
    let g:neocomplete#sources#syntax#min_keyword_length = 3

    if !exists('g:neocomplete#sources')
        let g:neocomplete#sources = {}
    endif
    let g:neocomplete#sources._ = ['buffer', 'member', 'tag', 'file', 'dictionary']
    let g:neocomplete#sources.go = ['omni']

    " disable sorting
    call neocomplete#custom#source('_', 'sorters', [])
endif

" Enable Omni complete
if has("autocmd")
    set ofu=syntaxcomplete#Complete
    autocmd FileType c set omnifunc=ccomplete#Complete
    autocmd FileType css set omnifunc=csscomplete#CompleteCSS
    autocmd FileType html set omnifunc=htmlcomplete#CompleteTags
    autocmd FileType java set completefunc=javacomplete#CompleteParamsInfo
    autocmd FileType java set omnifunc=javascomplete#Complete
    autocmd FileType java set completefunc=javacomplete#CompleteParamsInfo
    autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS
    autocmd FileType php let php_sql_query=1
    autocmd FileType php let php_htmlInStrings=1
    autocmd FileType php set omnifunc=phpcomplete#CompletePHP
    autocmd FileType python set omnifunc=pythoncomplete#Complete
    autocmd FileType ruby,eruby set omnifunc=rubycomplete#Complete
    autocmd FileType ruby,eruby let g:rubycomplete_buffer_loading = 1
    autocmd FileType ruby,eruby let g:rubycomplete_classes_in_global = 1
    autocmd FileType ruby,eruby let g:rubycomplete_rails = 1
    autocmd FileType sql set omnifunc=sqlcomplete#Complete
    autocmd FileType xml set omnifunc=xmlcomlete#CompleteTags
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

"============================
" Java lang maps
"============================
" enable smart class imports
nmap <space><F4> <Plug>(JavaComplete-Imports-AddSmart)
imap <space><F4> <Plug>(JavaComplete-Imports-AddSmart)
" enable insertion of class imports
nmap <space><F5> <Plug>(JavaComplete-Imports-Add)
imap <space><F5> <Plug>(JavaComplete-Imports-Add)
" add all missing imports
nmap <space><F6> <Plug>(JavaComplete-Imports-AddMissing)
imap <space><F6> <Plug>(JavaComplete-Imports-AddMissing)
" remove all missing imports
nmap <space><F7> <Plug>(JavaComplete-Imports-RemoveUnused)
imap <space><F7> <Plug>(JavaComplete-Imports-RemoveUnused)


" Node.js dictionary
au FileType javascript set dictionary+=$HOME/.vim/bundle/vim-node/dict/node.dict

" Recompile a Coffee file when saved
au BufWritePost *.coffee silent CoffeeMake! -b | cwindow | redraw!

" jQuery Syntax
au BufRead,BufNewFile jquery.*.js set ft=javascript syntax=jquery

" Deal with whitespace
highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+$/
autocmd BufWinEnter * match ExtraWhitespace /\s\+$/
autocmd InsertEnter * match ExtraWhitespace /\s\+\%#\@<!$/
autocmd InsertLeave * match ExtraWhitespace /\s\+$/
autocmd BufWinLeave * call clearmatches()
" func to trim whitespace
function! TrimWhiteSpace()
    %s/\s\+$//e
endfunction
autocmd BufWritePre * :call TrimWhiteSpace()

" Solarized stuff
"let g:solarized_termtrans=1
"let g:solarized_contrast='high'
let g:enable_bold_font = 1
let g:enable_italic_font = 1
let g:hybrid_custom_term_colors = 1
let base16colorspace=256
set background=dark
colorscheme hybrid
highlight CursorLine cterm=BOLD ctermbg=235 ctermfg=NONE

