# Use the official Python image as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libproj-dev \
    libgeos-dev \
    libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN pip uninstall --yes shapely
RUN pip install --no-binary :all: shapely

COPY download-osm.py .
RUN python download-osm.py

# Copy the source code into the container
COPY . .

# Run the command line program
# CMD ["python", "make_map.py"]
ENTRYPOINT [ "bash" ]