FROM python:3.10-buster

WORKDIR /app

# Install system dependencies and SQLite in a single RUN command to reduce layers
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    wget \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    sqlite3 \
    xz-utils \
    tk-dev \
    liblzma-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libffi-dev \
    liblzma-dev \
    curl \
    git && \
    wget https://www.sqlite.org/2023/sqlite-autoconf-3410200.tar.gz -O sqlite.tar.gz && \
    tar -xvf sqlite.tar.gz && \
    cd sqlite-autoconf-3410200 && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    cd .. && \
    rm -rf sqlite-autoconf-3410200 sqlite.tar.gz && \
    ln -sf /usr/local/bin/sqlite3 /usr/bin/sqlite3 && \
    ln -sf /usr/local/lib/libsqlite3.so /usr/lib/x86_64-linux-gnu/libsqlite3.so && \
    ln -sf /usr/local/lib/libsqlite3.so /usr/lib/x86_64-linux-gnu/libsqlite3.so.0

# Install pipenv and dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# Install Django and other dependencies
RUN pip install --upgrade pip django djangorestframework
RUN pip install django-cors-headers

# Verify installations
RUN python -m django --version && sqlite3 --version

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]