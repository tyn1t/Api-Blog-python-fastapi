from fastapi import APIRouter, Depends, File, HTTPException
from fastapi.datastructures import UploadFile
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from database.database import get_db

from post.models.post import Post, PostSection
from post.schemas.post import PostCreate, PostCreateResponse, PostResponse, SectionResponse

from post.utils.post import create_upload_img, unique_slug, generate_slug
from users.models.users import User

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostCreateResponse)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    slug = generate_slug(post.title)

    existing = db.query(Post).filter(Post.slug == slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug já existe")

    try:
        db_post = Post(
            title=post.title,
            img_url=post.img_url,
            description=post.description,
            slug=slug,
            user_id=current_user.id
        )

        db.add(db_post)
        db.flush()

        for section in post.sections:
            db.add(PostSection(
                post_id=db_post.id,
                title=section.title,
                img_url=section.img_url,
                content=section.content,
                order=section.order
            ))

        db.commit()
        db.refresh(db_post)

        return {
            "message": "Post criado com sections",
            "url": f"post/{slug}"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
        
@router.get("/", response_model=list[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    
    
    return [{
        "id": post.id,
        "title": post.title,
        "img_url": post.img_url,
        "description": post.description,
        "url": f"post/{post.slug}",
        "slug": post.slug,
    } for post in posts]

@router.get("/{slug}", response_model=SectionResponse)
def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug == slug).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")

    sections = db.query(PostSection).filter(
        PostSection.post_id == post.id
    ).order_by(PostSection.order).all()

    return {
        "id": post.id,
        "title": post.title,
        "img_url": post.img_url,
        "slug": post.slug,
        "sections": [
            {   
                "title": section.title,
                "content": section.content,
                "img_url": section.img_url,
                "order": section.order
            } for section in sections
        ]
    }
    

@router.put("/{slug}")
def post_update(
        slug: str,
        post_data: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    
    post = db.query(Post).filter(Post.slug == slug).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    
    post.slug = unique_slug(db, generate_slug(post_data.title), post.id)

    post.title = post_data.title
    post.description = post_data.description

    db.query(PostSection).filter(
        PostSection.post_id == post.id
    ).delete(synchronize_session=False)
    
    for section in post_data.sections:
        db_section = PostSection(
            post_id=post.id,
            title=section.title,
            content=section.content,
            order=section.order
        )
        db.add(db_section)

    db.commit()
    db.refresh(post)
    
    return {"message": "Post atualizado com sucesso"}



@router.delete("/{slug}")
def delete_post(
        slug: str, 
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    
    post = db.query(Post).filter(Post.slug == slug).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    db.query(PostSection).filter(PostSection.post_id == post.id).delete()

    db.delete(post)    
    db.commit()
    
    return {"message": "Post deletado com sucesso"}
    
@router.post("/upload/{slug}")
async def upload_img(
    slug: str,
    file_img: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if not file_img.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Envie apenas imagens"
        )

    img_url = await create_upload_img(slug=slug, file=file_img)

    return {"img": img_url}