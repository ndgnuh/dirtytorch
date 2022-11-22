FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime

RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y neovim tmux htop tree build-essential
RUN apt-get install -y python3 python3-opencv
RUN apt-get install -y python3-pip python-is-python3
RUN apt-get install -y sudo ffmpeg
RUN apt-get install -y thunar v4l2loopback-dkms vlc file

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
RUN pip install pyclean
RUN pip install torch torchvision torchaudio
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# PATH
COPY .bashrc /home/dev/

RUN mkdir /home/dev/working
WORKDIR /home/dev/working

# ENV
ENV TERM=xterm-256color

CMD ["bash"]
