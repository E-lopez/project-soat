import time
from sqlalchemy import text
from typing import List
from fastapi import APIRouter, HTTPException


router = APIRouter(prefix="/query", tags=["AI Queries"], responses={
    404: {"description": "Not found"}
})


@router.post("/trigger-sales", responses={500: {"description": "Database commit failed"}})
async def trigger_sales():
    """
    Endpoint to trigger sales processes.
    This function simulates the process of triggering sales.
    """
    try:
        # Simulate sales triggering process
        time.sleep(2)  # Simulating a delay for sales triggering
        return {"message": "Sales triggered successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

