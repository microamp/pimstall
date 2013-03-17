" Colourscheme
color zenburn

" Basic settings
set number
set cul
set ruler
set nowrap
set textwidth=79
set colorcolumn=80
set autoindent
set backspace=indent,eol,start
set ls=2

" Searching preferences
set hlsearch
set incsearch
set ignorecase
set smartcase

" Four spaces per indentation
set shiftwidth=4
set softtabstop=4
set expandtab

" Block indentation
vnoremap > >gv
vnoremap < <gv

" Map Tab to Esc
nnoremap <Tab> <Esc>
vnoremap <Tab> <Esc>gV
onoremap <Tab> <Esc>
inoremap <Tab> <Esc>"^
inoremap <Leader><Tab> <Tab>

" Tab settings
set tabpagemax=10
map t :tabnew<CR>
map J :tabnext<CR>
map K :tabprevious<CR>

" Pathogen settings
call pathogen#infect()
syntax on
filetype plugin indent on

" NERDTree settings
let NERDTreeIgnore = ["\.pyc", "\.swp"]
map NT :NERDTreeToggle<CR>
let g:NERDTreeDirArrows=0

" ctrlp.vim settings
let g:ctrlp_map = "<c-p>"
let g:ctrlp_cmd = "CtrlP"
let g:ctrlp_working_path_mode = "ra"
let g:ctrlp_custom_ignore = {
  \ "dir":  "\v[\/]\.(git|hg|svn)$",
  \ "file": "\v\.(exe|so|dll)$",
  \ "link": "some_bad_symbolic_links",
  \ }

" Tagbar settings
nmap <F8> :TagbarToggle<CR>

" Gundo settings (requires Vim compiled with Python support)
nnoremap <F5> :GundoToggle<CR>
