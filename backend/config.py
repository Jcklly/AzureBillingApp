import os
from dotenv import load_dotenv

load_dotenv()

# Microsoft Auth
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

# Cosmos DB
COSMOS_DB_URL = os.getenv("COSMOS_DB_URL")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY")
COSMOS_DB_NAME = os.getenv("COSMOS_DB_NAME")
COSMOS_DB_CONTAINER_RESOURCES = os.getenv("COSMOS_DB_CONTAINER_RESOURCES")
COSMOS_DB_CONTAINER_USER_SUBSCRIPTIONS = os.getenv("COSMOS_DB_CONTAINER_USER_SUBSCRIPTIONS")