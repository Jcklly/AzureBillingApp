from fastapi import APIRouter, HTTPException
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from database import init_cosmos_db
from config import CLIENT_ID, CLIENT_SECRET, TENANT_ID

router = APIRouter()

@router.get("/check-resources")
def check_resources():
    db = init_cosmos_db()
    user_sub_container = db["user_subscriptions_container"]

    admin_user_id = "admin@jcklly.onmicrosoft.com"
    query = f"SELECT TOP 1 c.subscriptionID FROM c WHERE c.userID = '{admin_user_id}'"

    try:
        results = list(user_sub_container.query_items(query=query, enable_cross_partition_query=True))
        if not results:
            raise HTTPException(status_code=404, detail="No subscription found.")
        subscription_id = results[0]["subscriptionID"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving subscription: {str(e)}")

    try:
        credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
        resource_client = ResourceManagementClient(credential, subscription_id)
        resources = [{"id": res.id, "name": res.name, "type": res.type, "location": res.location} for res in resource_client.resources.list()]
        return {"status": "success", "subscription_id": subscription_id, "resources": resources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Azure API error: {str(e)}")