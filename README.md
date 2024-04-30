
# Time Lock

Time Lock is a Python service built using FastAPI that securely handles RSA keys, designed for environments where key access is strictly controlled by time. This service allows RSA keys to be split and distributed, with recovery only possible after a specified date.

## Features

- **Key Generation**: Upon receiving a POST request with a specified date, generates an RSA key and splits it into two secrets.
- **Secure Storage**: Stores one part of the key secret in a database alongside the specified date and a unique identifier (UUID).
- **Conditional Key Recovery**: On a subsequent POST request with the stored UUID and one of the secrets, the service checks the current date. If it matches or exceeds the specified date, the RSA private key is reconstructed and returned to the client. If not, a 400 status code is returned, indicating that the date condition has not been met.

## Sample Project

For a practical implementation example of Time Lock, refer to the [sample project](https://github.com/luca-soda/time-vault).

## Use Cases
Use cases for Time Lock include:
- Auctions where the bid is only revealed after a specific time.
- Secure data storage where access is only granted after a certain date.
- Legal documents that can only be accessed after a specific date.
- Locked systems that can only be accessed after a certain time has passed (through an encrypted password)
- Secure data sharing where the data is only accessible after a certain date.
- Voting systems where the results are only revealed after a specific time.

But actually any information that needs to be kept secret and secure until a certain date.

## Getting Started

To get started with Time Lock, follow these steps:

### Prerequisites

- Python 3.12+
- FastAPI
- Uvicorn (for serving the application)
- A Postgres Database
###  or
- Docker

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/luca-soda/time-lock
   cd time-lock
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Service

#### Env variables
There should be a `.env` file in the root directory of the project. You can change the values of the variables in this file to suit your needs. There are not default values for the variables, so you need to set them up. 

You can find a .env.template file in the root directory of the project that you can use as a template.

```bash
cp .env.template .env
```
#### Docker compose
To run the service locally using docker-compose:

```bash
docker compose up
```
The docker compose includes a datatabase and an adminer to see what is stored in the database.
The docker compose project needs anyway the .env file to be set up.

#### Uvicorn
To run the service locally:

```bash
uvicorn main:app --reload
```

This will start the server on `http://127.0.0.1:8000`, where Time Lock is ready to accept requests.
This may be a solution if you want to run the service without docker and you have an external database.

## Documentation

You can check the automatically generated Swagger documentation by visiting `/docs` on your local server instance.

## Production
The project is not production ready. It is missing some features like:
- logging
- authentication
- brute force protection
- rate limiting

You can fork the project and add these features.

## Contact

You can contact me at luca.soda@gmail.com
