[![ML Client CI](https://github.com/software-students-spring2025/4-containers-super-container/actions/workflows/ml-client.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-super-container/actions/workflows/ml-client.yml)
[![Web App CI](https://github.com/software-students-spring2025/4-containers-super-container/actions/workflows/web-app.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-super-container/actions/workflows/web-app.yml)

## Overview

**EmotionSense** is a modular, containerized system that combines real-time data capture, machine learning-based emotion analysis, and interactive data visualization. Designed for portability and scalability, the system leverages Docker to manage three interoperable services:

- 🧠 **Machine Learning Client**: A Python-based backend service that uses a webcam to capture images, analyze facial expressions using [DeepFace](https://github.com/serengil/deepface), and persist results (dominant emotion + emotion scores) to a MongoDB database. It runs fully independently and can be triggered periodically or on demand.

- 🌐 **Web App**: A Flask-powered frontend dashboard that connects to the same MongoDB instance. It displays visualizations and analytics of the emotion data collected by the ML client. Users can view emotion trends, individual capture events, and metadata in an accessible and responsive UI.

- 🗄️ **MongoDB Database**: A persistent NoSQL data store running in a Docker container, shared by both the ML client and the web app. It stores the timestamped emotion analyses, image file paths, and emotion score vectors.

This system is especially useful for applications such as:
- Emotion-aware smart interfaces
- Human-computer interaction research
- Mental health and mood tracking
- Interactive art and installations

The full stack runs in isolated containers orchestrated via `docker-compose`, making it easy to deploy, scale, and test across platforms.



## Team Members

- [Xingjian Zhang](https://github.com/ScottZXJ123)
- [Hao Yang](https://github.com/Hao-Yang-Hao)
- [Yukun Dong](https://github.com/abccdyk)
- [Teammate 4](https://github.com/danielk98)


## 🛠 How to Configure and Run the Full Project (Cross-Platform Guide)

These instructions ensure that **any developer on any platform** (Windows, macOS, Linux) can configure and run all parts of the EmotionSense system successfully.

---

### 1️⃣ Prerequisites

Before starting, ensure the following tools are installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/)
- Webcam access (required for ML client to capture real-time images)

To verify installations:

```bash
python --version
docker --version
git --version
```

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/software-students-spring2025/4-containers-super-container.git
cd 4-containers-super-container
```
### 3️⃣ Create a Virtual Environment

Windows：

python -m venv venv
venv\\Scripts\\activate 

macOS / Linux：

python3 -m venv venv
source venv/bin/activate

### 4️⃣ Install Python Dependencies

```bash
pip install -r machine-learning-client/requirements.txt
pip install -r web-app/requirements.txt
```

### 5️⃣ Create and Configure the Environment File

Create a file named .env in the root directory with the following content:

```env
MONGO_URI=mongodb://localhost:27017/emotion_db
SECRET_KEY=changeme123
```

### 6️⃣ Run MongoDB Container

```bash
docker run --name mongodb -d -p 27017:27017 mongo
```

You can confirm MongoDB is running using:

```bash
docker ps
```

### 7️⃣ Run Machine Learning Client (Local Debug)

```bash
cd machine-learning-client
python main.py
```
This will:

Activate webcam

Capture an image

Analyze emotional expression via DeepFace

Save metadata and results to MongoDB

Save image locally in the images/ folder

### 8️⃣ Run Web App (Local Debug)

```bash
cd ../web-app
flask run
```
Visit http://localhost:5000 to view the web dashboard.

### 9️⃣ Run Everything Using Docker Compose (Deployment Mode)
Once each component works independently, you can launch the full system using:

```bash
docker-compose up --build
```

This will:

Spin up the MongoDB, ML Client, and Web App in separate containers

Set up internal networking between services

Automatically expose required ports (e.g., 5000 for the web)

To stop:
```bash
docker-compose down
```

## To run unit tests:

```bash
pytest  # from root or within client/web-app folders
```
