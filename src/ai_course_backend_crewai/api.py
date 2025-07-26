from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import os
import webbrowser
from .crew import AiCourseBackendCrewai

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Automatically open Swagger UI on server startup
    if os.environ.get("OPEN_SWAGGER", "1") == "1":
        try:
            webbrowser.open_new_tab("http://localhost:8000/docs")
        except Exception:
            pass
    yield

app = FastAPI(lifespan=lifespan)

class CourseOutlineRequest(BaseModel):
    topic: str
    complexity: Optional[str] = "medium"
    current_year: Optional[str] = str(datetime.now().year)

class GenerateCourseRequest(BaseModel):
    topic: str
    complexity: Optional[str] = "medium"
    format: str = "markdown"
    outline_edit: Optional[Dict[str, Any]] = None
    current_year: Optional[str] = str(datetime.now().year)

@app.get("/course-outline")
def get_course_outline(topic: str, complexity: Optional[str] = "medium", current_year: Optional[str] = str(datetime.now().year)):
    """
    Generate a course outline for a given topic and complexity.
    """
    try:
        crew = AiCourseBackendCrewai().crew()
        # Assuming the crew has a method to generate outline only
        outline = crew.generate_outline({
            "topic": topic,
            "complexity": complexity,
            "current_year": current_year
        })
        return {"outline": outline}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-course")
def generate_course(request: GenerateCourseRequest):
    """
    Generate a full course for a given topic, complexity, and (optionally) edited outline.
    """
    try:
        crew = AiCourseBackendCrewai().crew()
        # Assuming the crew.kickoff can take outline_edit as part of inputs
        inputs = {
            "topic": request.topic,
            "complexity_level": request.complexity,
            "format": request.format,
            "current_year": request.current_year
        }
        if request.outline_edit:
            inputs["outline_edit"] = request.outline_edit
        result = crew.kickoff(inputs=inputs)
        return {"course": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
