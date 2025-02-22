from azure.cosmos import CosmosClient
from config import COSMOS_DB_URL, COSMOS_DB_KEY, COSMOS_DB_NAME, COSMOS_DB_CONTAINER_RESOURCES, COSMOS_DB_CONTAINER_USER_SUBSCRIPTIONS

def init_cosmos_db():
    if not all([COSMOS_DB_URL, COSMOS_DB_KEY, COSMOS_DB_NAME, COSMOS_DB_CONTAINER_RESOURCES, COSMOS_DB_CONTAINER_USER_SUBSCRIPTIONS]):
        raise RuntimeError("Missing required Cosmos DB configuration!")

    try:
        client = CosmosClient(COSMOS_DB_URL, COSMOS_DB_KEY)
        database = client.get_database_client(COSMOS_DB_NAME)
        resources_container = database.get_container_client(COSMOS_DB_CONTAINER_RESOURCES)
        user_subscriptions_container = database.get_container_client(COSMOS_DB_CONTAINER_USER_SUBSCRIPTIONS)

        return {
            "client": client,
            "resources_container": resources_container,
            "user_subscriptions_container": user_subscriptions_container
        }
    except Exception as e:
        raise RuntimeError(f"Failed to connect to Cosmos DB: {e}")