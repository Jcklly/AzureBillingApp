import msal
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from config import CLIENT_ID, CLIENT_SECRET, TENANT_ID

router = APIRouter()

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/auth/callback"
REDIRECT_URI = f"https://ancerobilling.azurewebsites.net{REDIRECT_PATH}"

@router.get("/login")
def login():
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    auth_url = msal_app.get_authorization_request_url(
        scopes=["openid", "profile", "email"],
        redirect_uri=REDIRECT_URI
    )
    return RedirectResponse(url=auth_url)

@router.get(REDIRECT_PATH)
def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No authorization code provided."}

    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    result = msal_app.acquire_token_by_authorization_code(
        code, scopes=["openid", "profile", "email"], redirect_uri=REDIRECT_URI
    )

    if "access_token" in result:
        request.session["user"] = result
        return RedirectResponse(url="/dashboard")
    return {"error": "Authentication failed."}
