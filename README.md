# Time Lock

Time Lock is a Python service built with FastAPI that securely handles RSA keys by splitting and distributing them after a specific date. It is designed to be used in a secure environment where the key should only be accessible after a certain date.

## Features

- **Key Generation**: Generates a RSA key and splits it into two secrets upon receiving a POST request with a specified date.
- **Secure Storage**: Saves one part of the key secret in a database with the specified date and a unique identifier (UUID).
- **Conditional Key Recovery**: On a subsequent POST request with the stored UUID and one of the secrets, if the current date matches or exceeds the specified date, the service reconstructs the RSA private key and returns it to the client. Otherwise, it returns a 400 status code indicating the date condition has not been met.