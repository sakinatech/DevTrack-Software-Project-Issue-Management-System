from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class IssueCreate(BaseModel):
    title: str
    description: str | None = None
    issue_type: str
    priority: str
    project_id: int


class IssueResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    issue_type: str
    priority: str
    status: str
    project_id: int

    class Config:
        from_attributes = True
