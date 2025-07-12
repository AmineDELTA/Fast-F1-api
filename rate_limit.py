from fastapi import FastAPI, Request, HTTPException
from datetime import datetime, timedelta
from collections import defaultdict

request_logs = defaultdict(list) #key:IP  value:timestamps

async def rate_limiter(request: Request, call_next):
    client_ip = request.client.host
    
    now = datetime.now()
    one_minute_ago = now - timedelta(minutes=1)
    request_logs[client_ip] = [
        timestamp for timestamp in request_logs[client_ip] 
        if timestamp > one_minute_ago
    ]
    if len(request_logs[client_ip]) >= 10:
        retry_after = 60 - (now - request_logs[client_ip][0]).seconds
        raise HTTPException(
        status_code=429,
        detail=f"Too many requests. Try again in {retry_after} seconds.",
        headers={"Retry-After": str(retry_after)}
    )
        
    request_logs[client_ip].append(now)
    response = await call_next(request)
    return response