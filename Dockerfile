FROM python:3.7

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libffi-dev \
    libgmp-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone --single-branch --depth=1 --branch coordination_improvements https://github.com/SEArch-Service-Execution-Architecture/cfsm-bisimulation.git

WORKDIR /app/cfsm-bisimulation

RUN git pull

RUN ls -la && pip install --no-cache-dir -r requirements.txt

CMD ["python", "run_coordination_2025.py"]
