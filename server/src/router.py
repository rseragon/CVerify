from typing import Union
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from src.db import get_candidate, insert_candidate
from src.pdfanal.parser import parser
from .models import ErrorResponse, UserAuth, AuthResponse, ParseRequest, ParseResponse, CandidateInfo
from .auth import check_login

router = APIRouter()


# Nothing here
@router.get("/")
async def index_redirect():
    # TODO: Redirect to index page
    return RedirectResponse("https://google.com")


# Login
@router.post("/auth", include_in_schema=False)
async def auth(info: UserAuth) -> AuthResponse:
    user = info.username
    password = info.password
    # Check login and give user a token, add that token to the db
    logged_in, id = await check_login(user, password)

    if logged_in:
        return AuthResponse(logged_in=True, message="Vaild credentials", sessionId=id)
    return AuthResponse(logged_in=False, message="Invalid credentials", sessionId="-1")


# Parser
parser_description = """
> Used for parsing Resume

## Required Parameters
- path: local path where the resume is stored
"""


@router.post("/parse", description=parser_description)
async def parse(req: ParseRequest) -> ParseResponse:
    """
    TODO: Handle validation errors
    TODO: Handle emptpy body: 422 Unprocessable Entity
    """
    path = req.path

    # TODO: Include path boundary checking
    id, msg = await parser(path)

    return ParseResponse(candidate_id=id, message=msg if msg else "")


# Get Candidate info
@router.post("/candidate/{candidate_id}")
async def get_details(candidate_id: int) -> Union[CandidateInfo, ErrorResponse]:
    # info = CandidateInfo(
    #     name="Asad",
    #     number="100",
    #     email="asad@azad.com",
    #     skills=[],
    #     education=[],
    #     github="asad",
    #     linkedin="https://google.com",
    # )
    # id = await insert_candidate(info)
    cand = await get_candidate(candidate_id)

    if not cand:
        return ErrorResponse(message="Candidate id not found")

    return cand


@router.post("/summary/{limit}")
async def candidate_range(limit: int) -> list[CandidateInfo]:
    """
    Returns first `limit` candidates from the DB
    """
    return []
