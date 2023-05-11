# Build stage
FROM python:3.9-slim-buster AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libopencv-dev \
    libgtk-3-dev \
    libboost-dev \
    libboost-system-dev \
    libboost-python-dev \
    libboost-filesystem-dev \
    libprotobuf-dev \
    protobuf-compiler \
    git

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Final stage
FROM python:3.9-slim-buster

COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

WORKDIR /app

COPY main.py export_csv.py image_representation.py match_template.py non_max_suppression.py proposal_box_improve.py rotate_template.py utils.py Output ./

CMD ["python", "main.py"]