from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from .config import conf

employee_num_header = APIKeyHeader(name="employee-access-number", auto_error=False)

async def require_employee_code(code: str = Depends(employee_num_header)):
    if code is None or code != conf.employee_code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correct access code required. Message your manager if you need help.",
        )