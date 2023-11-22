# Base Image
FROM python:latest
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Prerequisites
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

# Set Working Directory
WORKDIR /usr/src

# Copy Application
COPY requirements.txt /usr/src
COPY . /usr/src

# Install Dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80 443
CMD ["python", "main.py"]
