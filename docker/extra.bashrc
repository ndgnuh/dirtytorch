#
# Extra path
#
export PATH=$HOME/.local/bin:$PATH

#
# Aliases and custom command
#
alias l='ls -lha --color auto'
jnote () {
  jupyter nbextensions_configurator enable
  jupyter nbextension enable toc2/main
  jupyter nbextension enable code_prettify/autopep8
  jupyter nbextension enable toggle_all_line_numbers/main
  jupyter nbextension enable init_cell/main
  jt -t onedork -fs 11 --cellw 90%  -lineh 130
  jupyter notebook --ip="0.0.0.0" --NotebookApp.token="" --NotebookApp.password="" --no-browser
}
alias unsafe-jupyter-notebook='jnote'

#
# Custom binding
#
stty werase undef
bind "\C-w:unix-filename-rubout"

