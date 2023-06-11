#
# Extra path
#
export PATH=$HOME/.local/bin:$PATH

#
# Aliases and custom command
#
alias l='ls -lha --color auto'
jnote () {
  jupyter-notebook --ip="0.0.0.0" --NotebookApp.token="" --NotebookApp.password="" --no-browser
}
alias unsafe-jupyter-notebook='jnote'

#
# Custom binding
#
stty werase undef
bind "\C-w:unix-filename-rubout"
