FROM python:3.8.10-alpine

WORKDIR /app

RUN apk add build-base \
    libffi-dev \
    cairo \
    libc6-compat \
    freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    libimagequant-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --prefer-binary -r requirements.txt

COPY . .

RUN python main.py create-palette

EXPOSE 8000

CMD gunicorn --timeout 90 --log-level=info -b 0.0.0.0:8000 "main:create_server()"