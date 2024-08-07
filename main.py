#main.py
from fastapi import FastAPI
from routes.blog import router as blog_router 
from routes.gallery import router as gallery_router 
from routes.contact import router as contact_router 
from routes.user import router as user_router
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(blog_router, prefix="/blog", tags=["blog"]),
app.include_router(gallery_router, prefix="/gallery", tags=["gallery"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(contact_router, prefix="/contact", tags=["contact"])

# app.include_router(blog_router, prefix="/blog", tags=["blog"], dependencies=[Depends(oauth2_scheme)])
# app.include_router(gallery_router, prefix="/gallery", tags=["gallery"], dependencies=[Depends(oauth2_scheme)])
# app.include_router(user_router, prefix="/user", tags=["user"], dependencies=[Depends(oauth2_scheme)])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://naadvenu.com","https://naadvenu.netlify.app", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cloudinary.config( 
    cloud_name = "dqnjhm36e", 
    api_key = "913536159649186", 
    api_secret = "<your_api_secret>",
    secure=True
)

import cloudinary


# Configuration       
cloudinary.config( 
    cloud_name = "dqnjhm36e", 
    api_key = "913536159649186", 
    api_secret = "GkCRtU8cQubOBSwnWBHXyLroetA", # Click 'View Credentials' below to copy your API secret
    secure=True
)
# Upload an image
# upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
#                                            public_id="shoes", fetch_format="auto")
# print(upload_result["secure_url"])

# # Optimize delivery by resizing and applying auto-format and auto-quality
# optimize_url, _ = cloudinary_url("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg", fetch_format="auto", quality="auto")
# print(optimize_url)

# # Transform the image: auto-crop to square aspect_ratio
# auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
# print(auto_crop_url)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
