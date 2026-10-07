from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas

from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevTrack",
    description="Software Project and Issue Management System",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to DevTrack API"
    }


# ---------------- PROJECTS ----------------

@app.post("/projects", response_model=schemas.ProjectResponse)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):
    new_project = models.Project(
        name=project.name,
        description=project.description
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@app.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()


@app.get("/projects/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }


# ---------------- ISSUES ----------------

@app.post("/issues", response_model=schemas.IssueResponse)
def create_issue(
    issue: schemas.IssueCreate,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == issue.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_issue = models.Issue(
        title=issue.title,
        description=issue.description,
        issue_type=issue.issue_type,
        priority=issue.priority,
        project_id=issue.project_id
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return new_issue


@app.get("/issues")
def get_issues(db: Session = Depends(get_db)):
    return db.query(models.Issue).all()


@app.get("/issues/{issue_id}")
def get_issue(
    issue_id: int,
    db: Session = Depends(get_db)
):
    issue = db.query(models.Issue).filter(
        models.Issue.id == issue_id
    ).first()

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    return issue


@app.put("/issues/{issue_id}/status")
def update_issue_status(
    issue_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    issue = db.query(models.Issue).filter(
        models.Issue.id == issue_id
    ).first()

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    issue.status = status

    db.commit()
    db.refresh(issue)

    return {
        "message": "Issue status updated",
        "status": issue.status
    }
