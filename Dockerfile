# Declare build-time argument for Python version
ARG PYTHON_VERSION=3.12

# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Re-declare ARG after FROM to make it available in later build stages
ARG PYTHON_VERSION

# Install necessary packages and the specified Python version
RUN apt-get update && apt-get install -y \
    software-properties-common \
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

# Set up a non-root user with the name dockeruser
RUN useradd -m dockeruser && echo "dockeruser:dockeruser" | chpasswd && adduser dockeruser sudo
USER dockeruser

# Create and switch to a new directory for the app
WORKDIR /app

# Create requirements.txt with necessary packages
RUN cat <<EOT > requirements.txt
torch==2.4.0
torchvision==0.19.0
torchaudio==2.4.0
notebook==7.2.1
EOT

# Install Python packages from requirements.txt
RUN pip3 install --user -r requirements.txt

# Set the default command to keep the container running
CMD ["/bin/bash"]