from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tasks import process_task 
from celery.result import AsyncResult

app = FastAPI(title="Fibbonaci Number calculator")

class JobRequest(BaseModel):
    target: int

@app.post("/jobs", status_code=201)
async def create_job(request: JobRequest):
    task = process_task.delay(request.dict())
    return {"job_id": task.id, "status": "queued"}

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    res = AsyncResult(job_id)
    
    if res.state == 'PENDING':
        return {"job_id": job_id, "state": res.state, "result": "Job is in queue"}
    elif res.state == 'SUCCESS':
        return {"job_id": job_id, "state": res.state, "result": res.result}
    elif res.state == 'ERROR':
        return {"job_id": job_id, "state": res.state, "error": str(res.info)}
    
    return {"job_id": job_id, "state": res.state}
