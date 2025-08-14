# 3.68GB
# FROM nvidia/cuda:13.0.0-devel-ubuntu24.04

# 28.34 MB
FROM ubuntu:24.04

# Build arguments (defaults match typical Linux host IDs)
# ARG HOST_UID=1000
# ARG HOST_GID=1000

# System environment
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    PATH="/opt/venv/bin:$PATH"

RUN mkdir -p /opt/visagir/r_apt

ADD 95safe-update 94retry-get /etc/apt/apt.conf.d/

COPY apt_package_list.txt /opt/visagir/r_apt

# Base system configuration (root)
    # Fix apt cache permissions and install system dependencies as root
RUN mkdir -p /var/lib/apt/lists/partial && \
    chmod 0755 /var/lib/apt/lists && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends $(perl -lpe 's/^\s+|\s+$//g' /opt/visagir/r_apt/apt_package_list.txt) && \
    locale-gen en_US en_US.UTF-8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
# Repository setup (root)
    # Add repositories
RUN add-apt-repository -y universe && \
    add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get update -y && \
    apt-get install -y wget && \
    wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list && \
    apt-get update -y && \
    apt-get install -y code


# Create a non-root user with host-mapped UID/GID
# RUN if ! getent group ${HOST_GID}; then \
#         groupadd --gid ${HOST_GID} dockeruser; \
#     fi && \
#     useradd --uid ${HOST_UID} --gid ${HOST_GID} -m dockeruser && \
#     mkdir -p /opt/venv /opt/visagir && \
#     chown -R ${HOST_UID}:${HOST_GID} /opt/venv /opt/visagir

RUN mkdir -p /opt/venv /opt/visagir && \
    chown -R ubuntu:ubuntu /opt/venv /opt/visagir

# Stage 2: User environment (dockeruser)
    # Switch to the generic user
# FROM base as user-env
# USER dockeruser
# WORKDIR /home/dockeruser

USER ubuntu
WORKDIR /home/ubuntu

# Create venv (owned by dockeruser) for managing Python toolchain
    # "conan==2.14.0"
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install "conan==2.0.17" && \
    /opt/venv/bin/pip install numpy scipy pytest libtmux && \
    conan profile detect
