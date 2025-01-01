# Base stage
FROM python:3.10-buster AS base
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential ...

# Dependencies stage
FROM base AS deps
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy

# Testing stage
FROM deps AS test
RUN pip install pytest
COPY . .
CMD ["pytest", "test_phase_2.py"]

# Production stage
FROM deps AS prod
COPY . .
EXPOSE 80
CMD ["./start.sh"]
