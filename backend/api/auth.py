from __future__ import annotations

import time
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from backend.db.db import get_session
from backend.db.models import Tenant

_bearer = HTTPBearer(auto_error=False)

# Phase 2: replace with real JWT validation
_DEV_TOKENS: dict[str, int] = {}


def create_dev_access_token(tenant_id: int = 1) -> str:
    token = f"dev-tenant-{tenant_id}-{int(time.time())}"
    _DEV_TOKENS[token] = tenant_id
    return token


def get_current_tenant_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
    session: Session = Depends(get_session),
) -> int:
    """Phase 2 JWT tenant resolver. MVP falls back to default tenant."""
    if credentials and credentials.credentials in _DEV_TOKENS:
        return _DEV_TOKENS[credentials.credentials]

    if credentials and credentials.credentials.startswith("dev-tenant-"):
        tenant = session.exec(select(Tenant).where(Tenant.id == 1)).first()
        if tenant:
            return tenant.id

    # MVP: allow unauthenticated access scoped to default tenant
    return 1


def require_tenant_admin(tenant_id: int = Depends(get_current_tenant_id)) -> int:
    if tenant_id < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return tenant_id
