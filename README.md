# Jonathan Essis Receipt Processor

Since this is a python built webservice, a dockerized setup is included.

# Requirements

Docker and/or Docker Compose

# Run This Application (No Docker Compose)

1. Make sure your in project folder

   `cd receipt-processor`

2. Build Docker image:

   `docker build -t receipt-processor-python .`

3. Run container:

   `docker run -p 8080:8080 receipt-processor-python`

4. The app should then be available at http://localhost:8080

## OR 

# Run This Application (With Docker Compose)

1. Make sure your in project folder

   `cd receipt-processor`

2. Build and start the service

   `docker-compose up --build`

3. The app should then be available at http://localhost:8080

# Note on Testing

`myTest.py` is a personal development test file used to verify functionality during the coding process. It is not intended for third-party testing and should not interfere with external test suites. By default, it cannot be executed unless `pytest` is explicitly included in `requirements.txt` before building the Docker image.




