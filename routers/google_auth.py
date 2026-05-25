from datetime import timedelta
from typing import Annotated
from fastapi import Depends, Request, APIRouter
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
import os
from auth.auth import  create_access_token
from dotenv import load_dotenv
from config import Settings
from functools import lru_cache

load_dotenv()

router = APIRouter()


@lru_cache
def get_settings():
    return Settings()

# Configure OAuth
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.environ['GOOGLE_CLIENT_ID'],
    client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration"
)

# Redirect user to Google for authentication
@router.get("/auth/google")
async def auth_google(request: Request):
    redirect_uri = os.environ.get("REDIRECT_URI")


    return await oauth.google.authorize_redirect(
        request, redirect_uri=redirect_uri
    )


# Handle the OAuth callback from Google
@router.get("/auth/google/callback")
async def google_callback(request: Request,settings: Annotated[Settings, Depends(get_settings)]):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo") or {}

        # Extract user details
        username = user_info.get("email")  # Use email as username

        # Generate a JWT token with auth_method="google"
        access_token = create_access_token(
            settings, 
            data={"sub": username}, 
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            auth_method="google"
        )

        return {"access_token": access_token, "token": token}
    except Exception as e:
        import traceback
        print("Error:", traceback.format_exc())  # Debugging step
        return {"error": str(e)}