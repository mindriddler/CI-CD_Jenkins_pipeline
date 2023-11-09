# PingURL v0.6 - URL Monitoring Service

PingURL is a RESTful service designed to monitor and perform periodic checks on specified URLs.

## Backend

### Requirements

- Python 3.10 or greater is required.

### Getting Started

#### VS Code Setup

To set up your environment with Visual Studio Code, follow these instructions:

1. Open the repository in VS Code which utilizes the `.vscode` directory at the root.
2. Install the recommended extensions that pop up upon opening.
3. Use "Python: Create Environment..." to set up a `.venv` at the root for local development, despite the backend directory being preferable for isolated Docker use.

#### Setting up the virtual environment

Before running the application, you need to set up a virtual environment and install the necessary dependencies. Follow these steps:

1. Navigate to the project's root directory.

```bash
cd path/to/pingurl/backend
```

2. Create a virtual environment in the `backend` directory.

```bash
# On macOS and Linux:
python3 -m venv venv

# On Windows:
python -m venv venv
```

3. Activate the virtual environment.

```bash
# On macOS and Linux:
source venv/bin/activate

# On Windows:
.\venv\Scripts\activate
```

#### Installing Dependencies

Install all dependencies required for the project to run:

```bash
pip install -r requirements.txt
```

#### Running the Application

Once the virtual environment is activated and dependencies are installed, you can start the Flask application using:

```bash
# Make sure your current working directory is the backend directory if you're not already there
cd backend

# Run the application
flask run
```

The application should now be running and accessible at `http://127.0.0.1:5000/`.

## API Endpoints

The following endpoints are available for interacting with the PingURL service:

#### Add a Watched URL

- `POST /watched-urls`: Add a new URL to be watched.
  - Payload: JSON object containing `activateAt` (ISO 8601 date-time string), `force` (boolean), `periodSec` (integer, minimum 10), and `url` (valid URL string).
  - Returns: JSON object with `message` indicating success and `urlId` of the added URL.
  - Status codes: 201 (Created), 400 (Bad Request).

Example request body:
```json
{
  "activateAt": "2023-11-06T01:36:28.610Z",
  "force": true,
  "periodSec": 30,
  "url": "http://example.com"
}
```

#### Delete a Watched URL

- `DELETE /watched-urls/{urlId}`: Remove a watched URL by its ID.
  - Returns: JSON object with a `message` indicating the URL has been removed.
  - Status codes: 200 (OK), 404 (Not Found).

#### Get Watched URL Data

- `GET /watched-urls/{urlId}`: Retrieve data for a specific watched URL by its ID.
  - Status codes: 
    - `200 (OK)`: The data for the watched URL was successfully retrieved.
    - `404 (Not Found)`: No data could be found for the provided URL ID.
  - Returns: A JSON object with the following structure:
    - `activateAt`: A timestamp in ISO 8601 format indicating when monitoring of the URL is scheduled to start.
    - `force`: A boolean indicating whether the monitoring process was initiated even when the creation request failed.
    - `periodSec`: The interval in seconds at which the URL is checked.
    - `pings`: An array of ping objects, each containing:
      - `pingedAt`: The timestamp of when the ping was executed.
      - `responseTimeSec`: The response time for the ping, in seconds.
      - `statusCode`: The HTTP status code received in response to the ping.
    - `url`: The URL that is being monitored.
    - `urlId`: The unique identifier for the watched URL.

Example request response:
```json
{
    "activateAt": "2023-11-06T02:35:05.923000+00:00",
    "force": false,
    "periodSec": 10,
    "pings": [
        {
            "pingedAt": "2023-11-09T03:57:13+00:00",
            "responseTimeSec": 0.052734,
            "statusCode": 200
        },
        {
            "pingedAt": "2023-11-09T03:57:23+00:00",
            "responseTimeSec": 0.052734,
            "statusCode": 200
        },
    ],
    "url": "http://google.com",
    "urlId": 1
}
```

#### Get All Watched URL IDs

- `GET /watched-urls`: Retrieves a list of IDs for all URLs currently under monitoring.
  - Status codes:
    - `200 (OK)`: The list of watched URL IDs was successfully retrieved.
  - Returns: A JSON object with the following structure:
    - `urlIds`: An array consisting of integer IDs, each uniquely identifying a watched URL.

Example request response:
```json
{
    "urlIds": [1, 2]
}
```

This example shows that there are two URLs being monitored, with the IDs 1 and 2.

#### Get Statistics

- `GET /stats`: Retrieve aggregate statistics about the watched URLs.
  - Status codes:
    - `200 (OK)`: Successfully retrieved statistics about the watched URLs.
  - Returns: A JSON object with the following data:
    - `pings`: The total count of pings that have been sent to monitored URLs.
    - `watchedUrls`: The number of unique URLs that are currently being monitored.

Example request response:
```json
{
    "pings": 12,
    "watchedUrls": 2
}
```

In this example, the response indicates that a total of 12 pings have been executed across 2 monitored URLs.

## Database

Further into the course...

## Frontend

Further into the course...
