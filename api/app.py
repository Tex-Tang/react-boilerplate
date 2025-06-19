from typing import Optional

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


@app.get("/")
async def root():
    return "Hello, world!"


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


class RunPythonSchema(BaseModel):
    code: str = Field(
        ..., min_length=1, max_length=10000, description="Python code to execute"
    )
    timeout: Optional[int] = Field(
        default=30, ge=1, le=300, description="Execution timeout in seconds"
    )


@app.post("/run-python")
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
