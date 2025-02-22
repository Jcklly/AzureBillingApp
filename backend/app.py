import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

SESSION_SECRET = os.getenv("SESSION_SECRET", "super-secret-key")
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# Absolute path to the React production build
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_BUILD_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend/build"))

if not os.path.exists(FRONTEND_BUILD_DIR):
    raise RuntimeError(f"React build directory not found: {FRONTEND_BUILD_DIR}")

# Mount the production build directory at /static
app.mount("/static", StaticFiles(directory=FRONTEND_BUILD_DIR, html=True), name="static")

# Serve index.html for the root path so that / loads the React app
@app.get("/")
def serve_react():
    index_file = os.path.join(FRONTEND_BUILD_DIR, "index.html")
    return FileResponse(index_file)

# Include your other API routes, for example:
@app.get("/check-resources")
def check_resources():
    # Replace with your actual logic to query Cosmos DB
    return {
      "status": "success",
      "subscription_id": "dummy-subscription",
      "resources": [
        {"name": "MyVM", "type": "Microsoft.Compute/virtualMachines", "location": "eastus"},
        {"name": "MyStorage", "type": "Microsoft.Storage/storageAccounts", "location": "westus"}
      ]
    }