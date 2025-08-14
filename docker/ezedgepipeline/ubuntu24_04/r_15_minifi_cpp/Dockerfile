# Stage 1: System setup (root)
FROM r_apt

USER root

SHELL ["/bin/bash", "-c"]

# Create log directory as root
# RUN mkdir -p /opt/visagir/log && \
#     chown -R dockeruser:dockeruser /opt/visagir/log && \
#     chmod -R 775 /opt/visagir/log

RUN mkdir -p /opt/visagir/log && \
    chown -R ubuntu:ubuntu /opt/visagir/log && \
    chmod -R 775 /opt/visagir/log

# Install MiNiFi C++ Apt Dependency Packages
COPY minifi_dep_package_list.txt /opt/visagir/r_apt

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends $(perl -lpe 's/^\s+|\s+$//g'  /opt/visagir/r_apt/minifi_dep_package_list.txt) && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Stage 2: User-space setup (dockeruser)
# FROM base as user-setup
# USER dockeruser
# WORKDIR /home/dockeruser

USER ubuntu
WORKDIR /home/ubuntu

RUN mkdir -p /opt/visagir/ext-minifi-cpp/comp

# Python tools in venv (inherited from r_apt)
ENV PATH="/opt/venv/bin:$PATH"

# ROS 2 environment setup (dockeruser)
# COPY --chown=dockeruser:dockeruser runcomp /opt/visagir/ext-minifi-cpp
# COPY --chown=dockeruser:dockeruser comp/10-minifi-cpp.bash /opt/visagir/ext-minifi-cpp/comp

COPY --chown=ubuntu:ubuntu runcomp /opt/visagir/ext-minifi-cpp
COPY --chown=ubuntu:ubuntu comp/10-minifi-cpp.bash /opt/visagir/ext-minifi-cpp/comp


RUN chmod +x /opt/visagir/ext-minifi-cpp/runcomp
RUN chmod +x /opt/visagir/ext-minifi-cpp/comp/10-minifi-cpp.bash
# RUN time /opt/visagir/ext-minifi-cpp/runcomp 10-minifi-cpp.bash
