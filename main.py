#main.py
from fastapi import FastAPI
from routes.blog import router as blog_router 
from routes.gallery import router as gallery_router 
from routes.contact import router as contact_router 
from routes.user import router as user_router
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(blog_router, prefix="/blog", tags=["blog"]),
app.include_router(gallery_router, prefix="/gallery", tags=["gallery"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(contact_router, prefix="/contact", tags=["contact"])

# app.include_router(blog_router, prefix="/blog", tags=["blog"], dependencies=[Depends(oauth2_scheme)])
# app.include_router(gallery_router, prefix="/gallery", tags=["gallery"], dependencies=[Depends(oauth2_scheme)])
# app.include_router(user_router, prefix="/user", tags=["user"], dependencies=[Depends(oauth2_scheme)])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
