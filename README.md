# Emotion Detection System

![Lint](https://github.com/software-students-spring2025/4-containers-super-container/actions/workflows/lint.yml/badge.svg)
![ml-client-ci](https://github.com/software-students-spring2025/4-containers-super-container/actions/workflows/ml-client-ci.yml/badge.svg)
![web-app-ci](https://github.com/software-students-spring2025/4-containers-super-container/actions/workflows/web-app-ci.yml/badge.svg)

A containerized application that analyzes facial emotions using deep learning and displays results through a web interface. The system consists of two Docker containers working together:

1. **Machine Learning Client** - Performs facial emotion analysis using DeepFace
2. **Web Application** - Provides a user interface for capturing and analyzing images
3. **Database** - Stores pictures users take by MongoDB

## Team Members

- [Xingjian Zhang](https://github.com/ScottZXJ123)
- [Yukun Dong](https://github.com/abccdyk)
- [Hao Yang](https://github.com/Hao-Yang-Hao)
- [Jiangbo Shen](https://github.com/js-montgomery)

## System Architecture

The system uses a microservices architecture with two main containers:

- **ML Client**: Python application that:
  - Receives images via camera
  - Analyzes facial emotions using DeepFace
  - Returns emotion classification results
- **Web App**: Flask-based web application that:
  - Provides a user interface for camera access
  - Forwards captured images to the ML client
  - Displays emotion analysis results
- **MongoDB database**:
  - Use MongoDB to store the pictures.
  
## Setup and Installation

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the System

1. Clone this repository:
   ```bash
   git clone https://github.com/software-students-spring2025/4-containers-super-container.git
   cd 4-containers-super-container
   ```

2. Start all containers with Docker Compose:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

3. Access the web application:
   - Open your browser and go to [http://localhost:8081](http://localhost:8081)
   - Grant camera access permissions when prompted
   - Click "Capture and Analyze" to detect emotions in the captured image

### Container Details

- **ML Client**: Runs on port 5002 and provides the `/analyze` endpoint
- **Web App**: Accessible at http://localhost:8081

## Project Structure

```
.
├── docker-compose.yml           # Docker Compose configuration
├── machine-learning-client/     # ML client code
│   ├── Dockerfile
│   ├── app/
│   │   └── main.py              # Main ML client application
│   ├── tests/                   # Unit tests
│   ├── uploads/                 # Temporary image storage
│   └── requirements.txt         # Python dependencies
└── web-app/                     # Flask web application
    ├── Dockerfile
    ├── app/
    │   ├── main.py              # Main Flask application
    │   └── templates/           # HTML templates
    │       ├── error.html
    │       └── index.html       # Main UI
    ├── tests/                   # Unit tests
    └── requirements.txt         # Python dependencies
```

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Machine Learning**: DeepFace, TensorFlow, OpenCV
- **Database**: MongoDB
- **Infrastructure**: Docker, Docker Compose

## API Endpoints

### Web App 
- `GET /`: Main web interface for the application
- `POST /analyze`: Accepts image data and forwards to ML client

### ML Client (port 5002)
- `POST /analyze`: Accepts image data and returns emotion analysis results

## Development

### Running Tests

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

## Features

- Real-time camera capture
- Facial emotion detection (happiness, sadness, anger, fear, surprise, disgust, neutral)
- Display of emotion confidence scores
- Modern, responsive UI

## Projects Sprint

- [Sprint1](https://github.com/orgs/software-students-spring2025/projects/159/views/1)
- [Sprint2](https://github.com/orgs/software-students-spring2025/projects/209)
