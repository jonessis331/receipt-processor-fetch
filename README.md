# Jonathan Essis Receipt Processor

Since this is a python built web service, a dockerized seup is included.

# Requirements

Docker and/or Docker Compose

# How to Run This Application (No Docker Compose)

1. Make sure your in project folder

   cd receipt-processor

2. Build Docker image:

   docker build -t receipt-processor-python .

3. Run container:

   docker run -p 8080:8080 receipt-processor-python

4. The app should then be available at http://localhost:8080

## OR

# How to Run This Application (With Docker Compose)

1. Make sure your in project folder

   cd receipt-processor

2. Build and start the service

   docker-compose up --build

3. The app should then be available at http://localhost:8080
