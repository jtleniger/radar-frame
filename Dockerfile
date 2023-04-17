FROM ubuntu:latest

WORKDIR /app

RUN apt-get update
RUN apt-get install -y \
    python3 \
    python3-pip \
    git \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    proj-bin \
    proj-data \
    libproj-dev

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --prefer-binary -r requirements.txt

COPY . .

COPY --from=golang:1.20.3 /usr/local/go /usr/local/go
ENV PATH=$PATH:/usr/local/go/bin

RUN git clone https://github.com/jtleniger/go-nexrad.git

WORKDIR /app/go-nexrad

RUN git checkout csv
RUN go build -o ../bin/nexrad-csv-amd64 cmd/nexrad-csv/*

WORKDIR /app

RUN apt-get install -y libcairo2

EXPOSE 8000

CMD gunicorn --timeout 90 --log-level=info -b 0.0.0.0:8000 "main:create_server()"