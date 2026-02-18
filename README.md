Health Insurance Cost Prediction API

A production-ready Machine Learning API built with FastAPI, containerized using Docker, and automated with CI/CD via GitHub Actions.

This project predicts health insurance expenses based on user inputs such as age, BMI, smoking status, region, and number of children.

Overview

This application exposes a REST API that serves predictions from a trained scikit-learn model. The project follows production-oriented practices including:

Modular project structure

Automated testing with pytest

Continuous Integration

Continuous Deployment to Docker Hub

Lazy model loading for runtime stability

Dockerized deployment

Project Structure
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

API Endpoint
POST /predict
Request Body
{
  "age": 30,
  "sex": "male",
  "bmi": 25.5,
  "children": 1,
  "smoker": "no",
  "region": "southwest"
}

Response
{
  "predicted_expenses": 3456.78
}


Interactive API documentation is available at:

http://127.0.0.1:8000/docs

Running Locally
1. Create Virtual Environment
python -m venv venv


Activate:

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

2. Install Dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

3. Run the API
uvicorn src.api.main:app --reload

Running with Docker
Build Image
docker build -t health-insurance-api .

Run Container
docker run -p 8000:8000 health-insurance-api

Testing

Run tests locally:

pytest


The CI pipeline automatically runs tests on every push to the main branch.

CI/CD Pipeline
Continuous Integration

Installs dependencies

Runs unit tests

Builds Docker image

Continuous Deployment

Builds Docker image

Pushes image to Docker Hub

Secrets configured in GitHub:

DOCKERHUB_USERNAME

DOCKERHUB_TOKEN

Model Training

To retrain the model:

python -m src.models.train


The model is loaded lazily at runtime to prevent import-time failures during CI execution.

Production Considerations

Lazy model initialization

Dockerized environment

Isolated dependency management

Automated validation via tests

Secure secret handling in GitHub Actions

Docker Hub

Pull the production image:

docker pull <your-dockerhub-username>/health-insurance-api

Tech Stack

Python 3.11

FastAPI

scikit-learn

MLflow

Docker

GitHub Actions

pytest

If you want, next we can tighten this further with:

API versioning

Health check endpoint

Logging middleware

Production Docker optimizations

Now it looks clean and serious.