# Stage 1: BUILDER
FROM ubuntu:24.04 AS builder

# Update, upgrade and install necessary packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    python3.12 \
    python3.12-dev \
    python3.12-venv \
    python3-pip \
    build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV HOME=/home/nobody
WORKDIR $HOME
ENV PYTHONUNBUFFERED=1
ENV PATH="$HOME/venv/bin:$PATH"

# Create a virtual environment and upgrade pip, setuptools, wheel
RUN python3.12 -m venv $HOME/venv && \
    pip3 install --upgrade pip setuptools wheel --no-warn-script-location

# Copy requirements.txt from the host to the current location in the image (.)
COPY requirements.txt .

# Install Python dependencies
RUN pip3 wheel --wheel-dir=/wheels -r requirements.txt

# Stage 2: FINAL
FROM ubuntu:24.04 AS final

# Update, upgrade and install necessary packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    python3.12 \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV HOME=/home/nobody
WORKDIR $HOME
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=$HOME/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create a virtual environment and upgrade pip, setuptools, wheel
COPY --from=builder /wheels /wheels
COPY --from=builder $HOME/venv $HOME/venv
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-index --find-links=/wheels --no-warn-script-location -r requirements.txt

# Copy the application code to the image
COPY --chown=nobody:nogroup guardian_tales/ guardian_tales/
COPY --chown=nobody:nogroup entrypoint.sh .

# Run the application as a non-root user for added security
USER nobody

ENTRYPOINT ["./entrypoint.sh"]