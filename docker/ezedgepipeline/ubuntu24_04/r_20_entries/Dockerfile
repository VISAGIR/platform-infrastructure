# Stage 1: Base setup (root)
FROM r_minifi_cpp

USER root

# System directories (root)
RUN mkdir -p /opt/visagir/r_entries/

# Configure sudo access for dockeruser
    # Allow for homedir mount to trigger non-root user and group creation
COPY --chown=root:root sudoers /etc/sudoers

# Stage 2: User environment
# FROM base as user-setup
# USER dockeruser
# WORKDIR /home/dockeruser

USER ubuntu
WORKDIR /home/ubuntu

# Copy entrypoint scripts (dockeruser-owned)
# COPY --chown=dockeruser:dockeruser pyentrypoint/ /opt/visagir/r_entries/pyentrypoint

COPY --chown=ubuntu:ubuntu pyentrypoint/ /opt/visagir/r_entries/pyentrypoint

# Final stage
# FROM user-setup as final

ENV SHELL=/usr/bin/bash \
    PYTHONUNBUFFERED=1

# ROS 2 environment activation via Python entrypoint
ENTRYPOINT ["python3", "-u", "/opt/visagir/r_entries/pyentrypoint/entrypoint.py"]

