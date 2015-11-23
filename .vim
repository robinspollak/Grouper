set softtabstop=4 shiftwidth=4
set expandtab
set relativenumber
set autoindent


""""""""""""""""""""
" Nice visual stuff
""""""""""""""""""""
set list listchars=trail:-
syntax on

""""""""""""""""""""
" Status bar
""""""""""""""""""""
set laststatus=2
set statusline=%t[%{strlen(&fenc)?&fenc:'none'},%{&ff}]%h%m%r%y%=%c,%l/%L\ %P
set formatoptions+=r

set mouse=a
