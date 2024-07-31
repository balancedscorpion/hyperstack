# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

ARG PYTHON_VERSION=3.12
ARG USER_PASSWORD

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV USER_PASSWORD=${USER_PASSWORD}

# Install necessary packages and the specified Python version
RUN apt-get update && apt-get install -y \
    software-properties-common \
    git \
    sudo \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-venv \
        python${PYTHON_VERSION}-dev \
        python${PYTHON_VERSION}-distutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y git

# Set the specified Python version as the default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1

# Install pip for the specific Python version
RUN python3 -m ensurepip --upgrade \
    && python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Set up dockeruser
RUN useradd -m dockeruser && \
    adduser dockeruser sudo

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to dockeruser for package installation
USER dockeruser
WORKDIR /home/dockeruser

# Install Python packages for dockeruser
RUN pip3 install --user --no-cache-dir \
    torch==2.4.0 \
    torchvision==0.19.0 \
    torchaudio==2.4.0 \
    notebook==7.2.1

ENTRYPOINT ["/entrypoint.sh"]

# Set the default command to start a Python shell
CMD ["/bin/sh" ]
