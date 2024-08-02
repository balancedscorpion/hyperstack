# Declare build-time argument for Python version
ARG PYTHON_VERSION=3.12

# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

ARG USER_NAME=dockeruser
ARG USER_PASSWORD=dockerpassword

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV USER_PASSWORD=${USER_PASSWORD}
ENV PATH="/usr/local/bin:${PATH}"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Re-declare ARG after FROM to make it available in later build stages
ARG PYTHON_VERSION

# Install necessary packages, build tools, and the specified Python version
RUN apt-get update && apt-get install -y \
    software-properties-common \
    pkg-config \
    build-essential \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-venv \
        python${PYTHON_VERSION}-dev \
        python${PYTHON_VERSION}-distutils \
        git \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the specified Python version as the default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION} 1

# Install pip for the specific Python version
RUN python3 -m ensurepip --upgrade \
    && python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Set up a non-root user with the name dockeruser
RUN useradd -m ${USER_NAME} && \
    echo "${USER_NAME}:${USER_PASSWORD}" | chpasswd && \
    adduser ${USER_NAME} sudo


# Update shared library cache
RUN ldconfig

# Switch to dockeruser for package installation
USER ${USER_NAME}
WORKDIR /home/${USER_NAME}

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Update PATH for user to include Rust binaries
ENV PATH="/home/${USER_NAME}/.cargo/bin:${PATH}"

RUN rustup default stable

# Install Python packages for dockeruser
RUN pip3 install --user --no-cache-dir \
    torch==2.4.0 \
    torchvision==0.19.0 \
    torchaudio==2.4.0 \
    notebook==7.2.1

RUN newgrp docker

# Set the default command to keep the container running
CMD ["/bin/bash"]