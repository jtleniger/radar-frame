# Use the official Python image as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    proj-bin \
    libproj-dev \
    libgeos-dev \
    libspatialindex-dev \
    libhdf5-serial-dev \
    netcdf-bin \
    libnetcdf-dev \
    cmake \
    ninja-build

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --prefer-binary --no-cache-dir pyproj==3.2.1
RUN pip install --no-cache-dir boto3
RUN pip install --prefer-binary --no-cache-dir matplotlib
RUN pip install --no-cache-dir cartopy
RUN pip install --prefer-binary --no-dependencies --no-cache-dir osmnx
RUN apt-get install -y --no-install-recommends gfortran libopenblas-dev pkg-config patchelf cython3 gfortran
RUN pip install --prefer-binary --no-cache-dir arm_pyart
RUN pip install --no-cache-dir gunicorn
RUN pip install --no-cache-dir Flask
RUN pip install --no-cache-dir cairosvg
RUN pip install boto3==1.26.100
RUN pip install botocore==1.29.100
RUN pip install networkx==3.0
RUN apt-get install -y --no-install-recommends gdal-bin libgdal-dev
RUN pip install geopandas==0.12.2

# Copy the source code into the container
COPY . .

RUN python main.py download-osm
RUN python main.py create-palette

CMD gunicorn --log-level=info --timeout 90 -b 0.0.0.0:8000 "main:create_server()"