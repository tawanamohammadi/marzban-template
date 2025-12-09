from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime, timedelta

app = FastAPI()

# Setup templates
templates = Jinja2Templates(directory="templates")

# Mock Database/Service
def get_user_data(username: str):
    # In a real app, this would query Marzban API or DB
    return {
        "username": username,
        "status": "active",
        "used_traffic": 1.57 * 1024 * 1024 * 1024, # 1.57 GB
        "data_limit": 50.0 * 1024 * 1024 * 1024,   # 50 GB
        "expire": (datetime.now() + timedelta(days=30)).timestamp(),
        "link": f"https://example.com/sub/{username}?token=xyz123"
    }

@app.get("/sub/{username}")
async def subscription_page(request: Request, username: str):
    user_data = get_user_data(username)
    
    return templates.TemplateResponse("subscription.html", {
        "request": request,
        "username": user_data["username"],
        "status": user_data["status"],
        "used_traffic": user_data["used_traffic"],
        "data_limit": user_data["data_limit"],
        "expire": user_data["expire"],
        "link": user_data["link"]
    })

@app.get("/manifest.json")
async def manifest():
    return templates.TemplateResponse("manifest.json", {"request": {}})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
