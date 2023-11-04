# Tutorial: Building Microservices in Python with Docker Compose

## Introduction

Microservices architecture is a design pattern that structures an application as a collection of loosely coupled, independently deployable services. Each service is focused on a specific business capability and can be developed, deployed, and scaled independently. In this tutorial, we'll guide you through building microservices using Python and popular frameworks, and then demonstrate how to orchestrate them using Docker Compose.

## Prerequisites

* Basic understanding of Python programming language
* Familiarity with RESTful APIs and web services
* Docker and Docker Compose installed on your machine

## Fameworks and Tools

### Flask

Flask is a lightweight Python web framework that's great for building microservices due to its simplicity and extensibility.

### FastAPI

FastAPI is a modern, fast web framework for building APIs with Python. It's known for its high performance and type checking capabilities.

### Docker and Docker Compose

Docker allows you to containerize your applications, while Docker Compose is used to define and manage multi-container Docker applications.

## Template microservices with Flask and FastAPI

We've created two template microservices. One microservice uses Flask, the other one uses FastAPI. In order to start these microservices, follow these steps:

1. Navigate to the directory containing the `docker-compose.yml` file.
2. Run the following command to build and start the microservices:

   ```bash
   docker-compose up --build
   ```

3. Access the Flask microservice at `http://localhost:5000`, the FastAPI microservice at `http://localhost:8000` and make a request to the Flask microservice by visiting http://localhost:8000/call_flask.

Congratulations! You've successfully built and orchestrated two microservices using Python, Flask, FastAPI, and Docker Compose.
Also, the FastAPI microservice communicates with the Flask microservice to retrieve data, demonstrating inter-microservice communication within a Docker Compose setup.  

Feel free to extend and modify these microservices to suit your specific use case and requirements. Happy coding!

## Extra: Generate code from OpenAPI specification

To generate code from OpenAPI specifications, you can use tools like **openapi-generator**.
This tool supports multiple languages and can generate client and server code based on your OpenAPI specification.
In this example, we'll generate Python code from an [example](template/petstore.yaml).

1. Install OpenAPI Generator

   Install the OpenAPI Generator CLI.
   You can find the latest release [here](https://github.com/OpenAPITools/openapi-generator/releases).

2. Generate FastAPI Code

   Run the following command to generate FastAPI code:

   ```bash
   openapi-generator generate -i petstore.yaml -g python-fastapi -o fastapi_petstore_code
   ```

3. Generate Flask Code

   Similarly, you can generate code using the Python Flask generator:

   ```bash
   openapi-generator generate -i petstore.yaml -g python-flask -o flask_petstore_code
   ```

4. Modify Generated Code

   The generated code may still need some adjustments based on your specific needs. Please find the generated API endpoints and models in the respective directories (**fastapi_petstore_code** and **flask_petstore_code**). Customize these files as needed for your application, using your provided OpenAPI specification.

## Extra: Generate OpenAPI spec from FastAPI code

FastAPI supports automatic generation of OpenAPI documentation. Let's enhance the FastAPI microservice with OpenAPI.

1. Install the necessary dependencies:

   ```bash
   pip install fastapi uvicorn[standard]
   ```

2. Update the **main.py** file to include an OpenAPI specification:

   ```python
   from fastapi import FastAPI
   import requests

   app = FastAPI()

   FLASK_SERVICE_URL = "http://flask_microservice:5000"  # Docker network alias

   @app.get('/')
   async def read_root():
       return {"message": "Hello from FastAPI microservice!"}

   @app.get('/call_flask', response_model=dict)
   async def call_flask_microservice():
       response = await get_flask_response()
       return {"message": f"Response from Flask microservice: {response['message']}"}

   async def get_flask_response():
       response = requests.get(f"{FLASK_SERVICE_URL}/")
       return response.json()
   ```

   **async** support is added for handling asynchronous requests and included a **response_model** for the **/call_flask** route to specify the expected response structure.

3. Start FastAPI using Uvicorn with automatic OpenAPI documentation generation:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload --workers 2
   ```

   Access the FastAPI documentation at http://localhost:8000/docs to see the automatically generated OpenAPI documentation.

## Copyright

You can use and modify this lab as part of your education, but you are not allowed to share this lab, your modifications, and your solutions. Please contact the teaching staff if you want to use (part of) this lab for teaching other courses.

Copyright © teaching staff of the course "Systeemontwerp" at the Faculty of Engineering and Architecture - Ghent University.
