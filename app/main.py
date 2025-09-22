from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .database import get_db, Base, engine
from . import models, schemas
from fastapi.responses import JSONResponse
from typing import List
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

# CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, limit this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory (e.g., for index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Serve index.html at root
@app.get("/")
async def serve_index():
    index_path = os.path.join("static", "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path, media_type="text/html")

# Submit email (Form submission compatible)
@app.post("/add-email")
async def add_email(
    name: str = Form(...),
    email: str = Form(...),
    msg: str = Form(None),
    db: AsyncSession = Depends(get_db)
):
    email_obj = models.Email(name=name, email=email, msg=msg)
    db.add(email_obj)
    await db.commit()
    await db.refresh(email_obj)
    return {"message": "Email submitted successfully!"}

# Get all emails
@app.get("/get-emails", response_model=List[schemas.EmailResponse])
async def get_emails(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Email))
    emails = result.scalars().all()
    return emails  # FastAPI + Pydantic will serialize automatically

# Delete an email by ID
@app.delete("/delete-email/{email_id}")
async def delete_email(email_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Email).where(models.Email.id == email_id))
    email = result.scalar_one_or_none()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    await db.delete(email)
    await db.commit()
    return JSONResponse(content={"message": "Email deleted successfully"})
