![Lint](https://github.com/software-students-spring2025/4-containers-super-container/actions/workflows/lint.yml/badge.svg)

# Environment Sensor Analysis System

A containerized application that collects environmental sensor data, performs machine learning analysis, and displays the results through a web interface. The system consists of three interconnected Docker containers:

1. **MongoDB Database** - Stores sensor readings and analysis results
2. **Machine Learning Client** - Simulates sensor data collection and performs ML-based analysis
3. **Web Application** - Displays the data and analysis results in a user-friendly dashboard

## Team Members

- [Xingjian Zhang](https://github.com/ScottZXJ123)
- [Yukun Dong](https://github.com/abccdyk)
- [Team Member 3](https://github.com/TeamMember3)
- [Jiangbo Shen](https://github.com/js-montgomery)

## System Architecture

The system uses a microservices architecture with three containers:

- **MongoDB**: Stores all sensor data and analysis results
- **ML Client**: Python application that:
  - Collects sensor data (temperature, humidity, light levels)
  - Analyzes the data using machine learning (Random Forest classifier)
  - Stores results in MongoDB
- **Web App**: Flask-based web application that:
  - Retrieves data from MongoDB
  - Displays sensor readings and analysis in a dashboard
  - Provides API endpoints for data access

## Setup and Installation

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the System

1. Clone this repository:
   ```bash
   git clone https://github.com/Your-Username/4-containers-super-container.git
   cd 4-containers-super-container
   ```

2. Start all containers with Docker Compose:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

3. Access the web dashboard:
   - Open your browser and go to [http://localhost:8080](http://localhost:8080)

### Container Details

- **MongoDB**: Runs on port 27017 (accessible within the container network)
- **ML Client**: Automatically collects and analyzes data every 10 seconds
- **Web App**: Accessible at http://localhost:8080

## Development

### Environment Variables

The system uses the following environment variables (already configured in docker-compose.yml):

- `MONGO_URI`: MongoDB connection string (default: `mongodb://mongodb:27017`)

### Project Structure

```
.
├── docker-compose.yml          # Docker Compose configuration
├── machine-learning-client/    # ML client code
│   ├── Dockerfile
│   ├── main.py                 # Main ML client application
│   ├── requirements.txt        # Python dependencies
│   └── test_ml_client.py       # Unit tests
└── web-app/                    # Flask web application
    ├── Dockerfile
    ├── app.py                  # Main Flask application
    ├── requirements.txt        # Python dependencies
    ├── templates/              # HTML templates
    │   ├── error.html
    │   └── index.html
    └── test_app.py             # Unit tests
```

### Running Tests Locally

#### Machine Learning Client

```bash
cd machine-learning-client
pip install -r requirements.txt
pytest --cov=.
```

#### Web App

```bash
cd web-app
pip install -r requirements.txt
pytest --cov=.
```

## APIs

The web app provides the following API endpoints:

- `GET /api/readings`: Returns the latest 50 sensor readings as JSON
- `GET /api/stats`: Returns statistics about the collected data

## Extending the System

To extend the system with additional sensors or analysis:

1. Modify the `generate_sensor_data()` function in `machine-learning-client/main.py` to include new sensor types
2. Update the `analyze_data()` function to perform additional analysis
3. Update the web app templates to display the new data
