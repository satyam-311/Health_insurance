# Health Insurance Cost Prediction API

A production-ready Machine Learning API built with FastAPI, containerized using Docker, and automated using CI/CD via GitHub Actions.

This service predicts health insurance expenses based on user inputs such as age, BMI, smoking status, region, and number of children.

---

## Overview

This application exposes a REST API that serves predictions from a trained scikit-learn model.  
The project follows production-oriented practices including:

- Modular architecture
- Automated testing with pytest
- Continuous Integration
- Continuous Deployment to Docker Hub
- Lazy model loading for runtime stability
- Dockerized deployment

---

## Project Structure

```
Health_insurance/
│
├── src/
│   ├── api/
│   │   ├── main.py
│   │   └── schema.py
│   ├── data/
│   ├── features/
│   ├── models/
│   └── utils/
│
├── tests/
│   ├── test_api.py
│   └── test_train.py
│
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .github/workflows/
│   ├── ci.yml
│   └── cd.yml
```

---

## API Endpoint

### POST `/predict`

### Request Body

```json
{
  "age": 30,
  "sex": "male",
  "bmi": 25.5,
  "children": 1,
  "smoker": "no",
  "region": "southwest"
}
```

### Response

```json
{
  "predicted_expenses": 3456.78
}
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

## Running Locally

### 1. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Run the API

```bash
uvicorn src.api.main:app --reload
```

---

## Running with Docker

### Build Image

```bash
docker build -t health-insurance-api .
```

### Run Container

```bash
docker run -p 8000:8000 health-insurance-api
```

---

## Running Tests

```bash
pytest
```

Tests are automatically executed in the CI pipeline on every push to the `main` branch.

---

## CI/CD Pipeline

### Continuous Integration

- Installs dependencies
- Runs unit tests
- Builds Docker image

### Continuous Deployment

- Builds Docker image
- Pushes image to Docker Hub

Configured GitHub Secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

---

## Model Training

To retrain the model:

```bash
python -m src.models.train
```

The model is loaded lazily at runtime to prevent import-time failures during CI execution.

---

## Production Considerations

- Lazy model initialization
- Docker-based isolation
- Automated validation through tests
- Secure secret management
- Ready for cloud deployment

---

## Docker Hub

Pull the production image:

```bash
docker pull <your-dockerhub-username>/health-insurance-api
```

---

## Tech Stack

- Python 3.11
- FastAPI
- scikit-learn
- MLflow
- Docker
- GitHub Actions
- pytest

---

## License

MIT License
