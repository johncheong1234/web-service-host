# Web Service Host

This project sets up a simple web service using Flask and Docker. Follow the steps below to get the application running on your local machine.

## Prerequisites

- Python 3.x
- Docker

## Setup Instructions

1. Clone the repository:

    ```sh
    git clone https://github.com/johncheong1234/web-service-host.git
    cd web-service-host
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    On Windows:
    ```sh
    venv\Scripts\activate
    ```

    On macOS and Linux:
    ```sh
    source venv/bin/activate
    ```

4. Install the required dependencies:

    ```sh
    pip install Flask docker
    ```

5. Make sure Docker is installed and running on your machine.

6. Run the Flask application:

    ```sh
    python app.py
    ```

The server should now be running on [http://localhost:5000](http://localhost:5000).

## License

This project is licensed under the MIT License.
