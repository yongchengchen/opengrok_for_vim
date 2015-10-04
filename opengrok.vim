"=============================================================================
" check that everything is OK
"=============================================================================
if !has("python")
    finish
endif


if filereadable($VIMRUNTIME."/plugin/opengrok.py")
  pyfile $VIMRUNTIME/plugin/opengrok.py
elseif filereadable($HOME."/.vim/plugin/opengrok.py")
  pyfile $HOME/.vim/plugin/opengrok.py
elseif filereadable($VIM."/vimfiles/plugin/opengrok.py")
  pyfile $VIM/vimfiles/plugin/opengrok.py
else
  call confirm('opengrok.vim: Unable to find opengrok.py. Place it in either your home vim directory or in the Vim runtime directory.', 'OK')
endif


"=============================================================================
" map debugging function keys
"=============================================================================
map <S-F6> :python opengrok_search()<cr>
map <S-F7> :python opengrok_current_line_file()<cr>
map <S-F8> :python opengrok_find_in_the_file()<cr>
map <S-F12> :python opengrok_searchdefinition()<cr>

python init_opengrok()
