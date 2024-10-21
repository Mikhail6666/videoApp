import os
from fastapi import APIRouter, Response, Depends, HTTPException
from typing import Annotated
from fastapi.responses import StreamingResponse
from dependency import get_violation_repository
from dependency import get_complete_png_files_repository
from repository import ViolationRepository
from repository import CompletePngFileRepository


router = APIRouter(prefix="/download", tags=["download"])



