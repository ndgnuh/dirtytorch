# FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime
FROM python:3.9-slim-bullseye

# ENV
ENV TERM=xterm-256color

# Install python
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y python-is-python3

# Heavy deps get installed first
RUN pip install -U pip
RUN pip install torch torchvision torchaudio

RUN pip cache purge

# Extra packages
RUN apt-get install -y sudo ffmpeg python3-opencv
RUN apt-get install -y thunar v4l2loopback-dkms vlc file
RUN apt-get install -y neovim tmux htop tree build-essential
RUN apt-get install -y git feh
RUN apt-get install -y curl wget aria2

# Create user
RUN useradd -u 1000 -m dev
RUN echo "dev:1234" | chpasswd
RUN usermod -a dev -G sudo
RUN usermod -a dev -G video # For camera
USER dev
WORKDIR /home/dev/

# Install deps
# Heavy deps get installed first
RUN pip install -U pip
COPY requirements.txt .
RUN pip install -r requirements.txt -U

# JUPYTER STUFFS!
env PATH=/home/dev/.local/bin:$PATH
RUN echo $PATH
RUN jupyter contrib nbextension install --user
RUN jupyter nbextensions_configurator enable --user
RUN jupyter nbextension enable toc2/main
RUN jupyter nbextension enable code_prettify/autopep8
RUN jupyter nbextension enable codefolding/main
RUN jupyter nbextension enable toggle_all_line_numbers/main
RUN jupyter nbextension enable hinterland/hinterland
RUN jupyter nbextension enable init_cell/main
COPY unsafe-jupyter-notebook /home/dev/.local/bin/

RUN pip cache purge

# SHELL STUFF
COPY .bashrc /home/dev/

RUN mkdir /home/dev/working
WORKDIR /home/dev/working

CMD ["bash"]
