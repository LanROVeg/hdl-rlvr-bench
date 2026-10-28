FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    ngspice \
    python3 \
    python3-scipy \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY workspace/ /workspace/
COPY instruction.md /workspace/instruction.md
