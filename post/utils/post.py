import re
import os
import uuid

from dotenv import load_dotenv

from fastapi import HTTPException, UploadFile, File

from  post.models.post import Post


load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR")

os.makedirs(UPLOAD_DIR, exist_ok=True)

def unique_slug(db, slug: str, post_id: int = None):
    base_slug = slug
    count = 1

    while True:
        query = db.query(Post).filter(Post.slug == slug)

        if post_id:
            query = query.filter(Post.id != post_id)

        exists = query.first()

        if not exists:
            break

        slug = f"{base_slug}-{count}"
        count += 1

    return slug

def generate_slug(title: str):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    
    return slug.strip()


async def create_upload_img(slug: str = None, file: UploadFile | None = None):
        
    if file is None or slug is None:
        print("No file or slug provided for upload.")
        return None
    
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
    
    print(f"Received file: {file.filename}")
    
    ext = file.filename.split(".")[-1].lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido")
    
    post_slug = slug

    folder = os.path.join(UPLOAD_DIR, post_slug)
    
    os.makedirs(folder , exist_ok=True)
    
    file_name = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(folder, file_name)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return f"/uploads/{post_slug}/{file_name}"

