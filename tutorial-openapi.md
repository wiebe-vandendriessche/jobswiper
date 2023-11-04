# Tutorial: Generate code from OpenAPI specification

To generate code from OpenAPI specifications, you can use tools like **openapi-generator**.
This tool supports multiple languages and can generate client and server code based on your OpenAPI specification.
In this example, we'll generate Python code from an [example](petstore.yaml).

1. Install OpenAPI Generator

   Install the OpenAPI Generator CLI. You can find the latest release [here](https://github.com/OpenAPITools/openapi-generator/releases).

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

## Extra 2: Generate OpenAPI spec from FastAPI code

You can also use OpenAPI to automatically generate documentation and specification for the API you created using FastAPI. Let's enhance the FastAPI microservice with OpenAPI.

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
