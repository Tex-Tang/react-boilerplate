import os
from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

# Get the static files directory from environment variable
static_dir = os.environ.get("EXAMPLE_STATIC_DIR")
if static_dir:
    static_path = Path(static_dir)
    app.mount("/assets", StaticFiles(directory=static_path / "assets"), name="assets")

class RunPythonSchema(BaseModel):
    code: str = Field(
        ..., min_length=1, max_length=10000, description="Python code to execute"
    )
    timeout: Optional[int] = Field(
        default=30, ge=1, le=300, description="Execution timeout in seconds"
    )

@app.post("/api/run-python")
async def run_python(body: RunPythonSchema):
    try:
        code = body.code
        if not code:
            raise HTTPException(status_code=400, detail="No code provided")

        exec_globals = {"pd": pd}
        exec_locals = {}
        exec(code, exec_globals, exec_locals)

        result = exec_locals.get("result", None)

        if isinstance(result, pd.DataFrame):
            result = result.to_dict(orient="records")
        elif isinstance(result, pd.Series):
            result = result.to_dict()
        else:
            result = str(result)

        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

@app.get("/{path:path}")
async def serve_frontend(path: str):
    """Serve the frontend static files."""
    if not static_dir:
        raise HTTPException(status_code=500, detail="Static files directory not configured")
    
    static_path = Path(static_dir)
    file_path = static_path / path
    
    # Default to index.html for root or if file doesn't exist (for SPA routing)
    if path == "" or not file_path.exists():
        file_path = static_path / "index.html"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
        
    return FileResponse(file_path) 