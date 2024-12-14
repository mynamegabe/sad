from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
    Form,
    File,
    UploadFile,
    Request,
    Response,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from typing import Annotated, Optional, List
from routers import users, auth, webhooks
from utils.common import hash_password, random_string
from utils.db import Session, get_session, User, create_db_and_tables
from utils.common import get_current_active_user
from modules.github import *
from config import *
from werkzeug.utils import secure_filename
import uvicorn
from schemas import Repo, Commit, GetCommits, GetCommit, CommitRef
import requests


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(webhooks.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/repos", response_model=List[Repo])
async def http_get_repos(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    r = get_repos(current_user.github_access_token)
    repos = r.json()
    repos = get_repos_branches(current_user.github_access_token, repos)
    return repos


@app.post("/commits", response_model=List[Commit])
async def http_get_commits(
    params: GetCommits, current_user: Annotated[User, Depends(get_current_active_user)]
) -> List[Commit]:
    r = get_commits(
        current_user.github_access_token,
        current_user.username,
        params.repo,
        params.branch,
    )
    commits = r.json()
    print(commits)
    return commits


@app.get("/commit", response_model=Commit)
async def http_get_commit(
    params: GetCommit, current_user: Annotated[User, Depends(get_current_active_user)]
) -> Commit:
    r = get_commit(
        current_user.github_access_token, current_user.username, params.repo, params.sha
    )
    commit = r.json()
    with open("commit.json", "w") as f:
        f.write(str(commit))
    return commit


@app.post("/scan", response_model=List[dict])
async def scan_commit(
    params: GetCommit, current_user: Annotated[User, Depends(get_current_active_user)]
):
    r = get_commit(
        current_user.github_access_token, current_user.username, params.repo, params.sha
    )
    commit_json = r.json()
    output_list = []
    if commit_json["files"]:
        files_changed = len(commit_json["files"])
        for i in range(files_changed):
            filename = commit_json["files"][i]["filename"]
            raw_url = commit_json["files"][i]["raw_url"]
            original_code = requests.get(raw_url).text
            code_patch = commit_json["files"][i]["patch"]

            prompt = f"""
            Given {original_code} as the context,
            is this patch malicious: {code_patch}
            
            at the end of your answer add a YES or NO to represent if the code given is malicious anot and surroud your answer with *
            """

            from config import MAKERSUITE_API_KEY

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={MAKERSUITE_API_KEY}"
            LLM_query = {"contents": [{"parts": [{"text": f"{prompt}"}]}]}
            LLM_request = requests.post(
                url, json=LLM_query, headers={"Content-Type": "application/json"}
            )
            LLM_response = LLM_request.json()
            LLM_response_text = LLM_response["candidates"][0]["content"]["parts"][0][
                "text"
            ]

            yes_no = LLM_response_text[-6:].upper()
            if "YES" in yes_no:
                output_list.append({f"{filename}": "YES"})

                prompt = f"why is this malicious ?\n{code_patch}"
                LLM_query = {"contents": [{"parts": [{"text": f"{prompt}"}]}]}
                LLM_request = requests.post(
                    url, json=LLM_query, headers={"Content-Type": "application/json"}
                )
                LLM_response = LLM_request.json()
                reason = LLM_response["candidates"][0]["content"]["parts"][0]["text"]
                output_list.append({"REASON": f"{reason}"})
            elif "NO" in yes_no:
                output_list.append({f"{filename}": "NO"})
            else:
                output_list.append({f"{filename}": "ERR"})

    return output_list


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
