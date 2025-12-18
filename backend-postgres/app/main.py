from __future__ import annotations

import uuid
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.routes.tasks import router as tasks_router
from app.core.config import settings
from app.db.session import Base, engine
from app.services.task_service import NotFoundError


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        docs_url="/docs",
        redoc_url=None,
    )

    # ---- CORS (Fix for frontend on Vite port 5173) ----
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---- Request trace id ----
    @app.middleware("http")
    async def add_trace_id(request: Request, call_next):
        trace_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.trace_id = trace_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = trace_id
        return response

    # ---- DB init (create tables) ----
    @app.on_event("startup")
    async def on_startup():
        Base.metadata.create_all(bind=engine)

    # ---- Exception handlers (uniform error model) ----
    def problem(
        status: int,
        title: str,
        detail: str,
        trace_id: str | None,
        errors: list[dict] | None = None,
    ):
        payload: Dict[str, Any] = {
            "type": "about:blank",
            "title": title,
            "status": status,
            "detail": detail,
            "trace_id": trace_id,
        }
        if errors is not None:
            payload["errors"] = errors
        return payload

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        trace_id = getattr(request.state, "trace_id", None)
        errors = []
        for e in exc.errors():
            loc = e.get("loc", [])
            field = ".".join([str(x) for x in loc if x not in ("body", "query", "path")]) or str(loc[-1]) if loc else ""
            errors.append({"field": field, "message": e.get("msg", "invalid")})
        return JSONResponse(
            status_code=422,
            content=problem(
                422,
                "Validation Error",
                "One or more fields are invalid.",
                trace_id,
                errors=errors,
            ),
        )

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        trace_id = getattr(request.state, "trace_id", None)
        return JSONResponse(
            status_code=404,
            content=problem(
                404,
                "Not Found",
                str(exc),
                trace_id,
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        trace_id = getattr(request.state, "trace_id", None)
        return JSONResponse(
            status_code=exc.status_code,
            content=problem(
                exc.status_code,
                "HTTP Error",
                exc.detail if isinstance(exc.detail, str) else "HTTP error",
                trace_id,
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        trace_id = getattr(request.state, "trace_id", None)
        return JSONResponse(
            status_code=500,
            content=problem(
                500,
                "Internal Server Error",
                "Unexpected error occurred.",
                trace_id,
            ),
        )

    # ---- Routers ----
    app.include_router(tasks_router, prefix=settings.api_v1_prefix, tags=["tasks"])

    return app


app = create_app()
