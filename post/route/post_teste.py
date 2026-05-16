import json
from typing import List

from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, UploadFile
from pydantic import Json
from auth.auth import get_current_user
from database.database import get_db
from post.models.post import Post, PostSection
from post.schemas.post import SectionCreate
from post.utils.post import create_upload_img, generate_slug
from users.models.users import User

from sqlalchemy.orm import Session

router = APIRouter(prefix="/v2/posts", tags=["testeimg"])

@router.post("/")
async def create_post(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(None),
    sections: List[SectionCreate] = Body(...),
    files: List[UploadFile] = File([]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        slug = generate_slug(title)

        # validar sections primeiro
        try:
            sections_data = json.loads(sections)
            validated_sections = [SectionCreate(**sec) for sec in sections_data]
        except Exception:
            raise HTTPException(status_code=400, detail="Sections inválido")
        
        img_url = None
        if file:
            img_url = await create_upload_img(file)

        db_post = Post(
            title=title,
            img_url=img_url,
            description=description,
            slug=slug,
            user_id=current_user.id
        )
        db.add(db_post)
        db.flush()  
        
        
        post_img_url = await create_upload_img(files)
        db_post.img_url = post_img_url

        # sections
        for i, sec in enumerate(validated_sections):
            section_img_url = None

            if sec.image_index < len(files):
                section_img_url = await create_upload_img(files[sec.image_index])

            db_section = PostSection(
                post_id=db_post.id,
                title=sec.title,
                content=sec.content,
                order=sec.order,
                img_url=section_img_url
            )
            db.add(db_section)

        db.commit()

        return {
            "message": "Post criado com sections",
            "url": f"/post/{slug}"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@router.post("/upload")
async def upload_img(file_img: UploadFile = File(None)):
    slug = "teste-upload"
    img_url = await create_upload_img(slug=slug, file=file_img)
    print(f"{file_img.filename} uploaded successfully. Accessible at: {img_url}")
    print(f"Image URL: {img_url}")
    return {"img": img_url}


