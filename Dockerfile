
FROM python:3.9

# Set root as current working directory
WORKDIR /

# Copy over everything except the things defined in the .dockerignore file
COPY . .

# Switch to backend directory

WORKDIR /backend

# Install required python packages and run fast api
RUN pip install -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
