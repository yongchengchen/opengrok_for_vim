import os
import sys
import vim
import socket
import base64
import traceback
import xml.dom.minidom
import urllib
import os.path


def init_opengrok():
  global keywords
  keywords = ['this','true','false', 'integer','string', 'html','body','br','head','var_dump', '__halt_compiler', 'abstract', 'and', 'array', 'as', 'break', 'callable', 'case', 'catch', 'class', 'clone', 'const', 'continue', 'declare', 'default', 'die', 'do', 'echo', 'else', 'elseif', 'empty', 'enddeclare', 'endfor', 'endforeach', 'endif', 'endswitch', 'endwhile', 'eval', 'exit', 'extends', 'final', 'for', 'foreach', 'function', 'global', 'goto', 'if', 'implements', 'include', 'include_once', 'instanceof', 'insteadof', 'interface', 'isset', 'list', 'namespace', 'new', 'or', 'print', 'private', 'protected', 'public', 'require', 'require_once', 'return', 'static', 'switch', 'throw', 'trait', 'try', 'unset', 'use', 'var', 'while', 'xor', '__CLASS__', '__DIR__', '__FILE__', '__FUNCTION__', '__LINE__', '__METHOD__', '__NAMESPACE__', '__TRAIT__']

def is_php_keyword(name): 
  if name and not name.isspace() and len(name)>2:
    if any(name in s for s in keywords):
      return True
  return False

def open_file(filename, keyword='', line = '1'):
    vim.command("tabnew")
    vim.command('set nowrap fdm=marker fmr={{{,}}} ft=php fdl=1')
    vim.command('edit ' + filename)
    vim.command(':' + line)
    if keyword and not keyword.isspace() and len(keyword)>2:
      vim.command('/' + keyword)
    #vim.command('normal G')  #go to lastline

def open_file_in_result():
    file = vim.current.line.split(':')
    #vim.current.buffer.append(file)
    #vim.command('normal G')
    if os.path.exists(file[0]):
      open_file(file[0], '', file[1])

def search(type = 'f', name = ''):
    if not is_php_keyword(name):
        tmpfile = '/tmp/.'+ name +'.sch'
        os.system('echo "Find definination: '+name+'" > ' + tmpfile);
        cmd = 'java -cp /usr/local/opengrok/lib/opengrok.jar org.opensolaris.opengrok.search.Search -R /var/opengrok/etc/configuration.xml -' + type +' "'+name+'" >> '+ tmpfile
        os.system(cmd);
        os.system('echo "Find definination: '+name+' finished" >> ' + tmpfile);
        #cmd = "php -r '$str = html_entity_decode(file_get_contents(\"/tmp/.sch.ls\")); file_put_contents(\"/tmp/.sch.ls\", $str);'";
        cmd = "sed -i '/\[.*\*/d' " + tmpfile
        os.system(cmd);
        cmd = "sed -i 's/\[.*\]//g' " + tmpfile
        os.system(cmd);
        open_file(tmpfile, name)
        os.system('rm -rf '+tmpfile);


def opengrok_search():
    name = vim.eval('expand("<cword>")')
    search('f', name)

def opengrok_searchdefinition():
    name = vim.eval('expand("<cword>")')
    search('d', name)

def opengrok_current_line_file():
    open_file_in_result()

def opengrok_find_in_the_file():
    curfile = vim.eval('expand("%:p")')
    os.system('rm -rf /tmp/tags /tmp/tags.tmp')
    os.system('ctags -f /tmp/tags ' + curfile)
    cmd = "cat /tmp/tags | awk -F'\t' '" + '{ if ($4 =="f") {print "function " $1} else if ($4=="v"){ print "$" $1}}' + "' > /tmp/tags.tmp && sort /tmp/tags.tmp | uniq -u > /tmp/tags"
    os.system(cmd)
    vim.command("vsplit")
    vim.command('set nowrap fdm=marker fmr={{{,}}} ft=php fdl=1')
    vim.command('edit /tmp/tags')
    vim.command(':vertical resize 30')
    vim.command(':set splitright')


