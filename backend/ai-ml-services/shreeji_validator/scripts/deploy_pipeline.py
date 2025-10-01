"""
deploy_pipeline.py
Script to deploy the verification pipeline to server or cloud
"""

import subprocess
import os

def start_fastapi_server():
    print("Starting FastAPI server...")
    # Example: run via uvicorn
    subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])

def setup_docker_services():
    print("Setting up Docker services...")
    if os.path.exists("docker-compose.yml"):
        subprocess.run(["docker-compose", "up", "-d"])
    else:
        print("docker-compose.yml not found, skipping Docker setup.")

if __name__ == "__main__":
    setup_docker_services()
    start_fastapi_server()
