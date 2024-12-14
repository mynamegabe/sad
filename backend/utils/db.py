from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USERNAME


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    # email: str = Field(index=True)
    # password: str = Field()
    avatar_url: str = Field()
    github_access_token: str = Field()


class Scan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    repo_name: str
    branch_name: str
    commit_sha: str
    scan_status: str
    scan_result: str
    last_scanned: str
    

class SuspiciousFiles(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    scan_id: int
    filename: str
    reason: str

# mysql
db_url = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# connect_args = {"check_same_thread": False}
engine = create_engine(db_url)  # , connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
