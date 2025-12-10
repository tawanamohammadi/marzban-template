from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import httpx
import uvicorn
import os
from datetime import datetime, timedelta

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Marzban Configuration
MARZBAN_URL = os.getenv("MARZBAN_URL", "http://localhost:8080")
MARZBAN_TOKEN = os.getenv("MARZBAN_TOKEN", "")

# Development Mode: Use mock data if no token provided
DEV_MODE = not MARZBAN_TOKEN

def get_mock_user_data(username: str):
    """
    Mock data for development/testing
    Simulates Marzban API response structure
    """
    now = datetime.now()
    created_at = now - timedelta(days=300)  # 10 months ago
    online_at = now - timedelta(minutes=2)   # 2 minutes ago
    expire = now + timedelta(days=30)        # 30 days from now
    
    return {
        "username": username,
        "status": "active",  # Will be converted to {"value": "active"}
        "used_traffic": int(1.57 * 1024 * 1024 * 1024),  # 1.57 GB
        "data_limit": int(50.0 * 1024 * 1024 * 1024),    # 50 GB
        "expire": int(expire.timestamp()),
        "online_at": int(online_at.timestamp()),
        "created_at": int(created_at.timestamp()),
        "links": [
            "vless://a1b2c3d4-e5f6-7890-abcd-ef1234567890@us1.example.com:443?encryption=none&security=tls&sni=us1.example.com&type=tcp&headerType=none#🇺🇸 US Server 1",
            "vless://b2c3d4e5-f6a7-8901-bcde-f12345678901@de1.example.com:443?encryption=none&security=reality&sni=google.com&type=tcp&headerType=none#🇩🇪 DE Server 1",
            "vmess://eyJ2IjoiMiIsInBzIjoi8J+HqPCfh6YgQ0EgU2VydmVyIDEiLCJhZGQiOiJjYTEuZXhhbXBsZS5jb20iLCJwb3J0Ijo0NDMsImlkIjoiYzNkNGU1ZjYtYTdiOC05MDEyLWNkZWYtMTIzNDU2Nzg5MDEyIiwiYWlkIjowLCJuZXQiOiJ3cyIsInR5cGUiOiJub25lIiwiaG9zdCI6ImNhMS5leGFtcGxlLmNvbSIsInBhdGgiOiIvd3MiLCJ0bHMiOiJ0bHMifQ==",
            "trojan://d4e5f6a7-b8c9-0123-def1-234567890123@nl1.example.com:443?security=tls&sni=nl1.example.com&type=tcp#🇳🇱 NL Server 1",
            "vless://e5f6a7b8-c9d0-1234-ef12-345678901234@fr1.example.com:443?encryption=none&security=tls&sni=fr1.example.com&type=tcp#🇫🇷 FR Server 1",
            "vless://f6a7b8c9-d0e1-2345-f123-456789012345@gb1.example.com:443?encryption=none&security=reality&sni=microsoft.com&type=tcp#🇬🇧 GB Server 1",
            "vless://a7b8c9d0-e1f2-3456-1234-567890123456@tr1.example.com:443?encryption=none&security=tls&sni=tr1.example.com&type=tcp#🇹🇷 TR Server 1",
            "vmess://eyJ2IjoiMiIsInBzIjoi8J+HrPCfh6cgSVIgU2VydmVyIDEiLCJhZGQiOiJpcjEuZXhhbXBsZS5jb20iLCJwb3J0Ijo0NDMsImlkIjoiYjhjOWQwZTEtZjJhMy00NTY3LTEyMzQtNjc4OTAxMjM0NTY3IiwiYWlkIjowLCJuZXQiOiJ3cyIsInR5cGUiOiJub25lIiwiaG9zdCI6ImlyMS5leGFtcGxlLmNvbSIsInBhdGgiOiIvd3MiLCJ0bHMiOiJ0bHMifQ==",
            "trojan://c9d0e1f2-a3b4-5678-2345-789012345678@fi1.example.com:443?security=tls&sni=fi1.example.com&type=tcp#🇫🇮 FI Server 1",
            "vless://d0e1f2a3-b4c5-6789-3456-890123456789@pl1.example.com:443?encryption=none&security=tls&sni=pl1.example.com&type=tcp#🇵🇱 PL Server 1",
            "vless://e1f2a3b4-c5d6-7890-4567-901234567890@se1.example.com:443?encryption=none&security=reality&sni=cloudflare.com&type=tcp#🇸🇪 SE Server 1",
            "vless://f2a3b4c5-d6e7-8901-5678-012345678901@jp1.example.com:443?encryption=none&security=tls&sni=jp1.example.com&type=tcp#🇯🇵 JP Server 1",
            "trojan://a3b4c5d6-e7f8-9012-6789-123456789012@sg1.example.com:443?security=tls&sni=sg1.example.com&type=tcp#🇸🇬 SG Server 1"
        ]
    }

async def get_user_from_marzban(username: str):
    """
    Fetch user data from Marzban API
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{MARZBAN_URL}/api/user/{username}",
                headers={"Authorization": f"Bearer {MARZBAN_TOKEN}"},
                timeout=10.0
            )
            
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="User not found")
            
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Marzban API Error: {str(e)}"
            )

def normalize_user_data(user_data: dict) -> dict:
    """
    Normalize user data to match V4 Dashboard expectations
    Ensures status is an object with 'value' key
    """
    # Convert status string to object if needed
    if isinstance(user_data.get("status"), str):
        user_data["status"] = {"value": user_data["status"]}
    
    return user_data

@app.get("/sub/{username}")
async def subscription_page(request: Request, username: str):
    """
    Main endpoint for displaying user dashboard
    Supports both development (mock) and production (Marzban API) modes
    """
    if DEV_MODE:
        print(f"[DEV MODE] Serving mock data for user: {username}")
        user_data = get_mock_user_data(username)
    else:
        print(f"[PRODUCTION] Fetching data from Marzban for user: {username}")
        user_data = await get_user_from_marzban(username)
    
    # Normalize data structure
    user_data = normalize_user_data(user_data)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user_data
    })

@app.get("/manifest.json")
async def manifest():
    """Serve PWA manifest"""
    return FileResponse("manifest.json")

@app.get("/sw.js")
async def service_worker():
    """Serve service worker"""
    return FileResponse("sw.js", media_type="application/javascript")

@app.get("/")
async def root():
    """Root endpoint - redirect or show info"""
    return {
        "app": "Marzban V4 Dashboard",
        "version": "4.0",
        "mode": "development" if DEV_MODE else "production",
        "endpoints": {
            "dashboard": "/sub/{username}",
            "manifest": "/manifest.json",
            "service_worker": "/sw.js"
        }
    }

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Marzban V4 Dashboard Server")
    print("=" * 60)
    print(f"Mode: {'🔧 DEVELOPMENT (Mock Data)' if DEV_MODE else '🌐 PRODUCTION (Marzban API)'}")
    if not DEV_MODE:
        print(f"Marzban URL: {MARZBAN_URL}")
    print(f"Server: http://localhost:8000")
    print(f"Dashboard: http://localhost:8000/sub/testuser")
    print("=" * 60)
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

