# syntax=docker/dockerfile:1
FROM python:3.10-buster
WORKDIR /app
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
    git

RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy
RUN pip install --upgrade pip
RUN pip uninstall -y django
RUN pip install django
RUN pip install djangorestframework
RUN python -m django --version
RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3410200.tar.gz -O sqlite.tar.gz && \
    tar -xvf sqlite.tar.gz && \
    cd sqlite-autoconf-3410200 && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    cd .. && \
    rm -rf sqlite-autoconf-3410200 sqlite.tar.gz

RUN ln -sf /usr/local/bin/sqlite3 /usr/bin/sqlite3 && \
    ln -sf /usr/local/lib/libsqlite3.so /usr/lib/x86_64-linux-gnu/libsqlite3.so && \
    ln -sf /usr/local/lib/libsqlite3.so /usr/lib/x86_64-linux-gnu/libsqlite3.so.0

RUN sqlite3 --version
COPY . .
EXPOSE 80
CMD ["./start.sh"]
