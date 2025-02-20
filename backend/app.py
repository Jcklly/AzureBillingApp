import os
from dotenv import load_dotenv

# Load local environment variables if present
load_dotenv()


import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates

# MSAL for Microsoft authentication
import msal

# Azure management libraries
from azure.cosmos import CosmosClient
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.mgmt.recoveryservices import RecoveryServicesClient
from azure.mgmt.automation import AutomationClient
from azure.mgmt.logic import LogicManagementClient


# Load required environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
SESSION_SECRET = os.getenv("SESSION_SECRET", "super-secret-key")  # change in production!

COSMOS_DB_URL = os.getenv("COSMOS_DB_URL")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY")
COSMOS_DB_NAME = os.getenv("COSMOS_DB_NAME")
COSMOS_DB_CONTAINER_RESOURCES = os.getenv("COSMOS_DB_CONTAINER_RESOURCES")
COSMOS_DB_CONTAINER_USER_SUBSCRIPTIONS = os.getenv("COSMOS_DB_CONTAINER_USER_SUBSCRIPTIONS")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/auth/callback"
REDIRECT_URI = f"https://ancerobilling.azurewebsites.net{REDIRECT_PATH}"

app = FastAPI()

# Session middleware
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# Ensure static files exist
if not os.path.isdir("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Cosmos DB connection on startup
@app.on_event("startup")
def startup_event():
    time.sleep(5)  # Delay for external services if needed
    if not all([COSMOS_DB_URL, COSMOS_DB_KEY, COSMOS_DB_NAME,
                COSMOS_DB_CONTAINER_RESOURCES, COSMOS_DB_CONTAINER_USER_SUBSCRIPTIONS]):
        raise RuntimeError("Missing one or more Cosmos DB environment variables!")
    try:
        client = CosmosClient(COSMOS_DB_URL, COSMOS_DB_KEY)
        database = client.get_database_client(COSMOS_DB_NAME)
        resources_container = database.get_container_client(COSMOS_DB_CONTAINER_RESOURCES)
        user_subscriptions_container = database.get_container_client(COSMOS_DB_CONTAINER_USER_SUBSCRIPTIONS)
        app.state.cosmos_client = client
        app.state.resources_container = resources_container
        app.state.user_subscriptions_container = user_subscriptions_container
    except Exception as e:
        raise RuntimeError("Failed to connect to Cosmos DB: " + str(e))


# Root endpoint: show the login page if not logged in
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    if "user" in request.session:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("index.html", {"request": request})


# Dashboard: displays after a successful login
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if "user" not in request.session:
        return RedirectResponse(url="/")
    user = request.session["user"]
    # For now, simply display the dashboard template
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})


# Route to start the login process (Microsoft Sign In)
@app.get("/login")
def login(request: Request):
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    auth_url = msal_app.get_authorization_request_url(
        scopes=["openid", "profile", "email"],
        redirect_uri=REDIRECT_URI
    )
    return RedirectResponse(url=auth_url)


# Callback endpoint for Microsoft Sign In
@app.get(REDIRECT_PATH, response_class=HTMLResponse)
def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return templates.TemplateResponse("error.html", {"request": request, "error": "No authorization code returned."})
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=["openid", "profile", "email"],
        redirect_uri=REDIRECT_URI
    )
    if "access_token" in result:
        request.session["user"] = result  # Save user token info in session
        return RedirectResponse(url="/dashboard")
    else:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Authentication failed.", "details": result})


# Test endpoint for the AzureResources container in Cosmos DB
@app.get("/test-db")
def test_db_resources():
    container = app.state.resources_container
    test_item = {
        "id": "test-connection-resources",
        "name": "Test Resource Item",
        "description": "This is a test item for the AzureResources container.",
        "timestamp": "2025-02-17T00:00:00Z",
        "subscriptionID": "dummy-subscription"
    }
    try:
        container.upsert_item(test_item)
        query = "SELECT * FROM c WHERE c.id='test-connection-resources'"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        if items:
            return {"status": "success", "data": items}
        else:
            return {"status": "failure", "message": "Test resource item not found after upsert."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Test endpoint for the UserSubscriptions container in Cosmos DB
@app.get("/test-db-user-subscriptions")
def test_db_user_subscriptions():
    container = app.state.user_subscriptions_container
    test_item = {
        "id": "test-connection-user",
        "userID": "admin@jcklly.onmicrosoft.com",
        "subscriptionID": "609e6c4a-2934-4cfe-b73a-53840369dd73",
        "role": "Admin",
        "timestamp": "2025-02-17T00:00:00Z"
    }
    try:
        container.upsert_item(test_item)
        query = "SELECT * FROM c WHERE c.id='test-connection-user'"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        if items:
            return {"status": "success", "data": items}
        else:
            return {"status": "failure", "message": "Test user subscription item not found after upsert."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to check Azure resources (billing-impacting details)
@app.get("/check-resources")
def check_resources():
    admin_user_id = "admin@jcklly.onmicrosoft.com"
    query = f"SELECT TOP 1 c.subscriptionID FROM c WHERE c.userID = '{admin_user_id}'"
    try:
        user_sub_container = app.state.user_subscriptions_container
        results = list(user_sub_container.query_items(query=query, enable_cross_partition_query=True))
        if not results:
            raise HTTPException(status_code=404, detail="No subscription found for admin user.")
        subscription_id = results[0]["subscriptionID"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving subscription for admin user: {str(e)}")

    try:
        credential = ClientSecretCredential(
            tenant_id=TENANT_ID,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
        resource_client = ResourceManagementClient(credential, subscription_id)
        compute_client = ComputeManagementClient(credential, subscription_id)
        storage_client = StorageManagementClient(credential, subscription_id)
        network_client = NetworkManagementClient(credential, subscription_id)
        monitor_client = MonitorManagementClient(credential, subscription_id)
        loganalytics_client = LogAnalyticsManagementClient(credential, subscription_id)
        recovery_client = RecoveryServicesClient(credential, subscription_id)
        automation_client = AutomationClient(credential, subscription_id)
        logic_client = LogicManagementClient(credential, subscription_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication or client instantiation error: {str(e)}")

    resources = []
    try:
        for res in resource_client.resources.list():
            resource_data = {
                "id": res.id,
                "name": res.name,
                "type": res.type,
                "location": res.location
            }
            parts = res.id.split("/")
            resource_group = parts[parts.index("resourceGroups") + 1] if "resourceGroups" in parts else None

            try:
                rtype = res.type.lower()
                if rtype == "microsoft.compute/virtualmachines" and resource_group:
                    vm = compute_client.virtual_machines.get(resource_group, res.name)
                    os_disk = vm.storage_profile.os_disk
                    data_disks = vm.storage_profile.data_disks
                    resource_data["vm_details"] = {
                        "vm_size": vm.hardware_profile.vm_size,
                        "os_disk_size_gb": os_disk.disk_size_gb,
                        "os_disk_type": os_disk.managed_disk.storage_account_type if os_disk.managed_disk else "Unknown",
                        "data_disks": [
                            {
                                "name": d.name,
                                "size_gb": d.disk_size_gb,
                                "disk_type": d.managed_disk.storage_account_type if d.managed_disk else "Unknown"
                            } for d in data_disks
                        ]
                    }
                # (Additional resource type handling omitted for brevity)
            except Exception as inner_e:
                resource_data["error"] = f"Failed to fetch additional details: {str(inner_e)}"
            resources.append(resource_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list resources: {str(e)}")
    return {"status": "success", "subscription_id": subscription_id, "resources": resources}