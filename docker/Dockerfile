FROM python:3.11-slim-bullseye

#
# OS extra packages
#
RUN <<EOR
	apt-get update
	# for video /image stuffs
	apt-get install -y ffmpeg python3-opencv v4l2loopback-dkms
	# system utilities
	apt-get install -y htop tree curl wget git neovim entr
	# clean up
	apt-get clean
EOR

#
# Install torch first because it's heavy
#
RUN pip install -U pip
RUN pip install torch torchvision torchaudio

#
# Create user 1000 because it's normally the default
# Root user get a password if installing extra package is needed
#
RUN useradd -u 1000 -m dev
RUN usermod -a dev -G video # Needed to access raw webcam
RUN echo "dev:1234" | chpasswd
RUN echo "root:1234" | chpasswd

#
# Install other packages
#
COPY requirements.txt /tmp/requirements.txt
RUN pip install -U -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

#
# Setup jupyter notebook
# Do not use hinterland because that shit is buggy
# Do not use code folding because it breaks the line number when using theme
#
RUN jupyter contrib nbextension install
RUN jupyter nbextensions_configurator enable
RUN jupyter nbextension enable toc2/main
RUN jupyter nbextension enable code_prettify/autopep8
RUN jupyter nbextension enable toggle_all_line_numbers/main
RUN jupyter nbextension enable init_cell/main
RUN jt -t onedork -fs 11 --cellw 90%  -lineh 130

#
# Setup shell stuffs
# use /etc/profile because user might not be 1000
# - local path
# - aliases
# - change bash ctrl-w mapping to rubout path
# - set term to xterm-256color for colors
# 
COPY extra.bashrc /tmp/extra.bashrc
RUN cat /tmp/extra.bashrc | tee -a /etc/bash.bashrc
RUN rm /tmp/extra.bashrc
ENV TERM=xterm-256color

#
# Clean up apt cache and pip cache
#
RUN pip cache purge
RUN apt-get clean
RUN rm /var/lib/apt/lists/ -rf

#
# Move to the normal user and a normal working directory
#
USER dev
RUN mkdir /home/dev/working
WORKDIR /home/dev/working

#
# Environment and entrypoint
#
ENTRYPOINT "/bin/bash"
