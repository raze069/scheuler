from datetime import datetime
import json
import logging
import random
import shutil
import string
from fastapi import Cookie, Depends, FastAPI, Form, HTTPException, Request, Response, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.core.database import engine, Base, SessionLocal
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.pages import router as pages_router
from app.routers.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import quote, urlencode
import os
import requests
from dotenv import load_dotenv
from app.utils.jwt import get_email_from_token, verify_access_token
from fastapi.responses import RedirectResponse, HTMLResponse
from google_auth_oauthlib.flow import Flow
import os
from dotenv import load_dotenv
import requests
from fastapi.templating import Jinja2Templates
from urllib.parse import quote
from oauthlib.oauth2 import WebApplicationClient

# Initialize database models
Base.metadata.create_all(bind=engine)

# Load environment variables
load_dotenv()

TIKTOK_CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")
TIKTOK_REDIRECT_URI = os.getenv("TIKTOK_REDIRECT_URI")
GOOGLE_CLIENT_ID= os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI=os.getenv("GOOGLE_REDIRECT_URI")
SCOPES = ["openid", "email", "profile"]
TIKTOK_SCOPE = "user.info.basic"  # Adjust the scope based on what you need
# Initialize FastAPI app
app = FastAPI()

client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Dependency to manage the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Encoding the redirect URI

# Middleware setup for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://127.0.0.1:8000",  # Local development
        "http://localhost:8000",  # Local development
        "https://scheduler-9v36.onrender.com",
        "https://scheduler-9v36.onrender.com/terms-and-conditions",
        "https://scheduler-9v36.onrender.com/privacy-policy"
        # Production domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")
PROFILE_PHOTO_DIR = "static/profile_photos"
# Include routers
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(pages_router, prefix="/pages", tags=["pages"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
os.makedirs("uploads", exist_ok=True)

@app.on_event("startup")
async def startup_event():
    print(f"CLIENT_KEY: {TIKTOK_CLIENT_KEY}")
    print(f"REDIRECT_URI: {TIKTOK_REDIRECT_URI}")

    

    
# Serve the HTML verification file for domain/app verification
@app.get("/googleb524bf271b1d073d.html")  # Change the filename to your actual file
async def serve_verification_file():
    file_path = "static/googleb524bf271b1d073d.html"  # Ensure this file is placed in the `static` folder
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}




@app.get("/tiktokBqCp0CjXfV1QtT9rl09qvRrnXgzDlmgK.txt")
async def serve_root_verification_file():
    # Specify the TikTok verification file path
    file_path = "static/tiktokBqCp0CjXfV1QtT9rl09qvRrnXgzDlmgK.txt"
    if os.path.exists(file_path):
        return FileResponse(file_path)  # Serve the file if it exists
    return {"error": "File not found"}

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request, token: str = Cookie(None)):
    # Log the cookie value to check if the token is being sent
    print(f"Cookie Token: {token}")  # This will appear in your server logs

    if token:
        try:
            # Verify the token (you can implement your token verification function here)
            verify_access_token(token)  # This function verifies the token
            # If the token is valid, redirect to the dashboard with token in URL
            print(f"Redirecting to dashboard with token: {token}")  # Debug log
            return RedirectResponse(url=f"/dashboard?token={token}", status_code=302)
        except HTTPException:
            # If the token is invalid or expired, redirect to login page
            print("Token is invalid or expired.")
            return RedirectResponse(url="/register?form=signin", status_code=302)
    else:
        # If there's no token, render the landing page
        print("No token found in cookie.")  # Debug log
        return templates.TemplateResponse("landingpage.html", {"request": request})



@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, form: str = "signup"):
    return templates.TemplateResponse("registerr.html", {"request": request, "form_type": form})

@app.get("/forgot-password", response_class=HTMLResponse)
async def terms_page(request: Request):
    return templates.TemplateResponse("forgot-password.html", {"request": request})


@app.get("/reset-password")
async def get_reset_password_page(request: Request, token: str):
    try:
        email = get_email_from_token(token)  # Extract the email from the token
    except HTTPException as e:
        logging.error(f"Invalid or expired token: {e}")
        return templates.TemplateResponse(
            "landingpage.html", {"request": request, "error_message": "Invalid or expired reset token."}
        )

    return templates.TemplateResponse("reset-password.html", {"request": request, "token": token})


@app.get("/authenticate", response_class=HTMLResponse)
async def authenticate(request: Request, email: str, token: str):
    return templates.TemplateResponse("authenticate.html", {"request": request, "email": email, "token": token})


@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy_page(request: Request):
    return templates.TemplateResponse("privacy-policy.html", {"request": request})

@app.get("/terms-and-conditions", response_class=HTMLResponse)
async def terms_page(request: Request):
    return templates.TemplateResponse("terms-and-conditions.html", {"request": request})





@app.get("/privacy-policy/tiktokCvwcy7TmgBroNQ5qZERcmWUXGj0jXbWl.txt")
async def serve_tiktok_verification_file():
    file_path = "static/tiktokCvwcy7TmgBroNQ5qZERcmWUXGj0jXbWl.txt"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}

# Serve TikTok verification file at the terms-and-conditions path
@app.get("/terms-and-conditions/tiktokxArJ8T0W2vPBu9uZTkrMHh0Ikd7Tgsyy.txt")
async def serve_tiktok_verification_file_terms():
    file_path = "static/tiktokxArJ8T0W2vPBu9uZTkrMHh0Ikd7Tgsyy.txt"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}


# Route to serve TikTok verification file
@app.get("/auth/tiktok/callback/{filename}")
async def serve_verification_file(filename: str):
    file_path = f"static/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}







import secrets  # ✅ Import the module

@app.get("/login/tiktok/")
async def auth_tiktok(response: Response, request: Request):
    csrf_state = secrets.token_urlsafe(16)  # ✅ Generate a secure random state
    
    response.set_cookie(
        key="csrfState", 
        value=csrf_state, 
        max_age=600, 
        httponly=False,  # ✅ Allow debugging (set back to True in production)
        secure=False,  # ✅ Debugging (change to True in production)
        samesite="Lax"  # ✅ Ensures cookies are sent in cross-site requests
    )

    print(f"✅ Cookie Set: csrfState = {csrf_state}")
    print(f"✅ All Cookies Before Redirect: {request.cookies}")

    auth_url = (
        f"https://www.tiktok.com/v2/auth/authorize/?"
        f"client_key={TIKTOK_CLIENT_KEY}&response_type=code&scope=user.info.basic&"
        f"redirect_uri={TIKTOK_REDIRECT_URI}&state={csrf_state}"
    )

    return RedirectResponse(url=auth_url)


@app.get("/auth/tiktok/callback/")
async def tiktok_callback(request: Request):
    """Handles TikTok's OAuth callback and exchanges the authorization code for an access token."""
    
    # Retrieve the authorization code and state from the callback query parameters
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    
    # Retrieve the CSRF state stored in cookies
    csrf_state = request.cookies.get("csrfState")

    # Debugging logs
    print(f"🔄 Callback Received!")
    print(f"🔹 Received State: {state}")
    print(f"🔹 Expected State (csrfState from Cookie): {csrf_state}")
    print(f"🔹 Authorization Code: {code}")
    print(f"🔹 All Received Cookies: {request.cookies}")  # ✅ Print all cookies

    # Validate the state parameter
    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing 'code' or 'state' parameters")

    if state != csrf_state:
        raise HTTPException(status_code=400, detail="State parameter mismatch")

    # Exchange the authorization code for an access token
    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    token_data = {
        "client_key": TIKTOK_CLIENT_KEY,
        "client_secret": TIKTOK_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": TIKTOK_REDIRECT_URI,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=token_data, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        error_message = response.json().get("message", "Unknown error")
        raise HTTPException(status_code=400, detail=f"Failed to get access token: {error_message}")
    
    # Extract the access token from the response
    access_token = response.json().get("data", {}).get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Access token not found")
    
    return {"access_token": access_token}

    
@app.get("/sitemap.xml")
async def get_sitemap():
    file_path = "static/sitemap.xml"  # Path to your sitemap in the static folder
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "Sitemap not found"}


@app.get("/robots.txt")
async def get_robots_txt():
    file_path = "static/robots.txt"  # Ensure the path matches your project structure
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "robots.txt not found"}

@app.get("/auth/google")
async def google_login(response: Response):
    """Generate Google OAuth URL and redirect user to Google for authentication."""
    
    # Generate the Google OAuth2 URL
    authorization_url = client.prepare_request_uri(
        "https://accounts.google.com/o/oauth2/auth",
        redirect_uri=GOOGLE_REDIRECT_URI,
        scope=" ".join(SCOPES),
        access_type="offline",
        prompt="consent"
    )

    # Store the state parameter in the cookies
    state = os.urandom(24).hex()  # Generate a random state string
    response.set_cookie("oauth_state", state)

    return RedirectResponse(authorization_url)


@app.get("/auth/callback")
async def oauth2_callback(request: Request, oauth_state: str = Cookie(None)):
    """Handle the OAuth2 callback and fetch the user's profile."""
    
    # Extract the code and state from the callback URL
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    # Validate the state parameter to prevent CSRF attacks
    if state != oauth_state:
        return {"error": "State parameter mismatch"}

    if code:
        # Exchange the authorization code for an access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        token_response = requests.post(token_url, data=token_data)
        
        if token_response.status_code != 200:
            return {"error": "Failed to get tokens"}

        # Extract the access token
        token_info = token_response.json()
        access_token = token_info.get("access_token")

        # Fetch the user's profile using the access token
        profile_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        profile_response = requests.get(profile_url, headers={"Authorization": f"Bearer {access_token}"})
        
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            return {"profile": profile_data}
        else:
            return {"error": "Failed to fetch profile"}
    
    return {"error": "No code found in request"}
