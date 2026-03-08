from __future__ import annotations

import hashlib
import json
import secrets
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db import get_connection, init_db
from seed_db import seed


app = FastAPI(title="Landing Constructor API")
api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
seed()


@app.get("/", include_in_schema=False)
def root():
    return {"message": "API работает. Откройте /docs для документации."}

# -----------------------------
# Helpers
# -----------------------------


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def parse_json(value: Optional[str], default):
    if value is None:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return default


def plan_from_row(row) -> Dict[str, object]:
    return {
        "id": row["id"],
        "name": row["name"],
        "features": parse_json(row["features"], []),
        "limits": parse_json(row["limits"], None),
    }


def template_from_row(row) -> Dict[str, object]:
    return {
        "id": row["id"],
        "name": row["name"],
        "category": row["category"],
        "is_premium": bool(row["is_premium"]),
        "preview_image": row["preview_image"],
        "description": row["description"],
    }


def project_from_row(row) -> Dict[str, object]:
    return {
        "id": row["id"],
        "client_id": row["client_id"],
        "name": row["name"],
        "template_id": row["template_id"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "status": row["status"],
        "thumbnail_url": row["thumbnail_url"],
        "data": parse_json(row["data"], {}),
    }


# -----------------------------
# Schemas
# -----------------------------


class RegisterRequest(BaseModel):
    company_type: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class PlanCreateRequest(BaseModel):
    name: str
    features: List[str]
    limits: Optional[Dict[str, int]] = None


class PlanUpdateRequest(BaseModel):
    name: Optional[str] = None
    features: Optional[List[str]] = None
    limits: Optional[Dict[str, int]] = None


class PlanSelectRequest(BaseModel):
    plan_id: str


class ProjectCreateRequest(BaseModel):
    name: str
    template_id: str
    status: str = "draft"
    thumbnail_url: str
    data: Dict[str, object]


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    thumbnail_url: Optional[str] = None
    data: Optional[Dict[str, object]] = None


class AiGenerateRequest(BaseModel):
    companyName: str
    industry: str
    products: str
    targetAudience: str
    usp: Optional[str] = ""


class ExportRequest(BaseModel):
    format: str


class NotificationsUpdateRequest(BaseModel):
    notifications: List[Dict[str, object]]


class PasswordUpdateRequest(BaseModel):
    password: str


class ErrorResponse(BaseModel):
    message: str
    fieldErrors: Optional[Dict[str, str]] = None


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def validate_registration_payload(payload: RegisterRequest) -> None:
    field_errors: Dict[str, str] = {}
    fields = {
        "username": payload.username,
        "email": payload.email,
        "password": payload.password,
        "confirm_password": payload.confirm_password,
    }

    for field_name, value in fields.items():
        if value is None or value.strip() == "":
            field_errors[field_name] = "Field is required"
        elif len(value) > 30:
            field_errors[field_name] = "Must be 30 characters or less"

    if "email" not in field_errors and payload.email and "@" not in payload.email:
        field_errors["email"] = 'Email must contain "@"'

    if (
        "password" not in field_errors
        and "confirm_password" not in field_errors
        and payload.password != payload.confirm_password
    ):
        field_errors["confirm_password"] = "Passwords do not match"

    if payload.company_type not in ("small", "large"):
        field_errors["company_type"] = "Company type must be small or large"

    if field_errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Validation error", "fieldErrors": field_errors},
        )


def validate_password(password: str) -> None:
    if password.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Validation error", "fieldErrors": {"password": "Field is required"}},
        )
    if len(password) > 30:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Validation error", "fieldErrors": {"password": "Must be 30 characters or less"}},
        )


def get_client_from_token(authorization: Optional[str] = Header(None)) -> Dict[str, object]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized"},
        )
    token = authorization.replace("Bearer ", "").strip()
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT c.id, c.company_type, c.username, c.email, c.plan_id
            FROM auth_tokens t
            JOIN clients c ON c.id = t.client_id
            WHERE t.token = ?
            """,
            (token,),
        ).fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized"},
        )
    return dict(row)


def get_project_for_client(project_id: str, client_id: str) -> Dict[str, object]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM projects
            WHERE id = ? AND client_id = ?
            """,
            (project_id, client_id),
        ).fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Project not found"},
        )
    return project_from_row(row)


def get_project_limit(plan_id: Optional[str]) -> Optional[int]:
    if not plan_id:
        return 3
    with get_connection() as conn:
        row = conn.execute(
            "SELECT limits FROM plans WHERE id = ?",
            (plan_id,),
        ).fetchone()
    if not row:
        return 3
    limits = parse_json(row["limits"], None)
    if isinstance(limits, dict) and "projects" in limits:
        return limits["projects"]
    return None


# -----------------------------
# Auth endpoints
# -----------------------------


@api_router.post("/auth/register", responses={422: {"model": ErrorResponse}})
def register(payload: RegisterRequest):
    validate_registration_payload(payload)

    with get_connection() as conn:
        existing = conn.execute(
            "SELECT 1 FROM clients WHERE email = ?",
            (payload.email.strip(),),
        ).fetchone()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": "Email already registered"},
            )

        client_id = str(uuid4())
        conn.execute(
            """
            INSERT INTO clients (id, company_type, username, email, password_hash, plan_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                client_id,
                payload.company_type,
                payload.username.strip(),
                payload.email.strip(),
                hash_password(payload.password),
                None,
                now_iso(),
            ),
        )

    return {
        "id": client_id,
        "company_type": payload.company_type,
        "username": payload.username.strip(),
        "email": payload.email.strip(),
        "plan_id": None,
    }


@api_router.post("/auth/login")
def login(payload: LoginRequest):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, password_hash
            FROM clients
            WHERE email = ?
            """,
            (payload.email.strip(),),
        ).fetchone()

        if not row or row["password_hash"] != hash_password(payload.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Invalid credentials"},
            )

        token = secrets.token_urlsafe(24)
        conn.execute(
            """
            INSERT INTO auth_tokens (token, client_id, created_at)
            VALUES (?, ?, ?)
            """,
            (token, row["id"], now_iso()),
        )

    return {"token": token}


@api_router.post("/auth/logout")
def logout(client: Dict[str, object] = Depends(get_client_from_token), authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "").strip()
    with get_connection() as conn:
        conn.execute("DELETE FROM auth_tokens WHERE token = ?", (token,))
    return {"message": "Logged out"}


# -----------------------------
# Client endpoints
# -----------------------------


@api_router.get("/clients/me")
def get_me(client: Dict[str, object] = Depends(get_client_from_token)):
    return {
        "id": client["id"],
        "company_type": client["company_type"],
        "username": client["username"],
        "email": client["email"],
        "plan_id": client["plan_id"],
    }


@api_router.patch("/clients/me/plan")
def select_plan(payload: PlanSelectRequest, client: Dict[str, object] = Depends(get_client_from_token)):
    with get_connection() as conn:
        plan = conn.execute(
            "SELECT 1 FROM plans WHERE id = ?",
            (payload.plan_id,),
        ).fetchone()
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "Plan not found"},
            )
        conn.execute(
            "UPDATE clients SET plan_id = ? WHERE id = ?",
            (payload.plan_id, client["id"]),
        )
    return {"message": "Plan updated", "plan_id": payload.plan_id}


@api_router.patch("/clients/me/password", responses={422: {"model": ErrorResponse}})
def update_password(payload: PasswordUpdateRequest, client: Dict[str, object] = Depends(get_client_from_token)):
    validate_password(payload.password)
    with get_connection() as conn:
        conn.execute(
            "UPDATE clients SET password_hash = ? WHERE id = ?",
            (hash_password(payload.password), client["id"]),
        )
    return {"message": "Password updated"}


# -----------------------------
# Plans endpoints
# -----------------------------


@api_router.get("/plans")
def list_plans():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM plans").fetchall()
    return [plan_from_row(row) for row in rows]


@api_router.get("/plans/{plan_id}")
def get_plan(plan_id: str):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Plan not found"},
        )
    return plan_from_row(row)


@api_router.post("/plans")
def create_plan(payload: PlanCreateRequest):
    plan_id = str(uuid4())
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO plans (id, name, features, limits)
            VALUES (?, ?, ?, ?)
            """,
            (
                plan_id,
                payload.name.strip(),
                json.dumps(payload.features, ensure_ascii=False),
                json.dumps(payload.limits, ensure_ascii=False) if payload.limits is not None else None,
            ),
        )
        row = conn.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
    return plan_from_row(row)


@api_router.patch("/plans/{plan_id}")
def update_plan(plan_id: str, payload: PlanUpdateRequest):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "Plan not found"},
            )
        name = payload.name.strip() if payload.name is not None else row["name"]
        features = (
            json.dumps(payload.features, ensure_ascii=False)
            if payload.features is not None
            else row["features"]
        )
        limits = (
            json.dumps(payload.limits, ensure_ascii=False)
            if payload.limits is not None
            else row["limits"]
        )
        conn.execute(
            """
            UPDATE plans
            SET name = ?, features = ?, limits = ?
            WHERE id = ?
            """,
            (name, features, limits, plan_id),
        )
        updated = conn.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
    return plan_from_row(updated)


@api_router.delete("/plans/{plan_id}")
def delete_plan(plan_id: str):
    with get_connection() as conn:
        row = conn.execute("SELECT 1 FROM plans WHERE id = ?", (plan_id,)).fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "Plan not found"},
            )
        conn.execute("DELETE FROM plans WHERE id = ?", (plan_id,))
    return {"message": "Plan deleted"}


# -----------------------------
# Templates endpoints
# -----------------------------


@api_router.get("/templates")
def list_templates():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM templates").fetchall()
    return [template_from_row(row) for row in rows]


@api_router.get("/templates/{template_id}")
def get_template(template_id: str):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM templates WHERE id = ?", (template_id,)).fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Template not found"},
        )
    return template_from_row(row)


# -----------------------------
# Projects endpoints
# -----------------------------


@api_router.get("/projects")
def list_projects(client: Dict[str, object] = Depends(get_client_from_token)):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM projects WHERE client_id = ?",
            (client["id"],),
        ).fetchall()
    return [project_from_row(row) for row in rows]


@api_router.post("/projects")
def create_project(payload: ProjectCreateRequest, client: Dict[str, object] = Depends(get_client_from_token)):
    project_limit = get_project_limit(client.get("plan_id"))
    with get_connection() as conn:
        if project_limit is not None:
            current_count = conn.execute(
                "SELECT COUNT(1) AS cnt FROM projects WHERE client_id = ?",
                (client["id"],),
            ).fetchone()["cnt"]
            if current_count >= project_limit:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={"message": "Project limit reached for current plan"},
                )

        project_id = str(uuid4())
        timestamp = now_iso()
        conn.execute(
            """
            INSERT INTO projects (
                id, client_id, name, template_id, created_at, updated_at, status, thumbnail_url, data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                project_id,
                client["id"],
                payload.name.strip(),
                payload.template_id,
                timestamp,
                timestamp,
                payload.status,
                payload.thumbnail_url,
                json.dumps(payload.data, ensure_ascii=False),
            ),
        )
        row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    return project_from_row(row)


@api_router.get("/projects/{project_id}")
def get_project(project_id: str, client: Dict[str, object] = Depends(get_client_from_token)):
    project = get_project_for_client(project_id, client["id"])
    return project


@api_router.patch("/projects/{project_id}")
def update_project(project_id: str, payload: ProjectUpdateRequest, client: Dict[str, object] = Depends(get_client_from_token)):
    existing = get_project_for_client(project_id, client["id"])
    updated_name = payload.name.strip() if payload.name is not None else existing["name"]
    updated_status = payload.status if payload.status is not None else existing["status"]
    updated_thumbnail = (
        payload.thumbnail_url if payload.thumbnail_url is not None else existing["thumbnail_url"]
    )
    updated_data = payload.data if payload.data is not None else existing["data"]
    updated_at = now_iso()
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE projects
            SET name = ?, status = ?, thumbnail_url = ?, data = ?, updated_at = ?
            WHERE id = ? AND client_id = ?
            """,
            (
                updated_name,
                updated_status,
                updated_thumbnail,
                json.dumps(updated_data, ensure_ascii=False),
                updated_at,
                project_id,
                client["id"],
            ),
        )
        row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    return project_from_row(row)


@api_router.delete("/projects/{project_id}")
def delete_project(project_id: str, client: Dict[str, object] = Depends(get_client_from_token)):
    get_project_for_client(project_id, client["id"])
    with get_connection() as conn:
        conn.execute("DELETE FROM exports WHERE project_id = ?", (project_id,))
        conn.execute(
            "DELETE FROM projects WHERE id = ? AND client_id = ?",
            (project_id, client["id"]),
        )
    return {"message": "Project deleted"}


# -----------------------------
# AI generation endpoint
# -----------------------------


@api_router.post("/ai/generate")
def ai_generate(payload: AiGenerateRequest):
    products = [p.strip() for p in payload.products.split(",") if p.strip()]
    generated = {
        "company": {
            "name": payload.companyName,
            "logo": "",
            "description": f"{payload.companyName} - ведущая компания в сфере {payload.industry}. Мы предлагаем инновационные решения для наших клиентов, помогая им достигать бизнес-целей и оптимизировать процессы.",
            "mission": f"Делать {payload.industry} доступным и эффективным для каждого бизнеса",
            "values": ["Инновации", "Качество", "Клиентоориентированность", "Прозрачность"],
        },
        "products": [
            {
                "id": f"prod-{idx}",
                "name": name,
                "description": f"Профессиональное решение для {name.lower()}",
                "price": "От 10 000 ₽",
                "image": f"https://images.unsplash.com/photo-{1460925895917 + idx}?w=400",
            }
            for idx, name in enumerate(products)
        ],
        "benefits": [
            {
                "id": "b1",
                "icon": "⚡",
                "title": "Быстрое внедрение",
                "description": "Запуск решения за 2-3 недели",
            },
            {
                "id": "b2",
                "icon": "🎯",
                "title": "Индивидуальный подход",
                "description": "Решения под ваши задачи",
            },
            {
                "id": "b3",
                "icon": "💼",
                "title": "Опытная команда",
                "description": "Более 10 лет на рынке",
            },
        ],
    }
    return generated


# -----------------------------
# Export endpoints
# -----------------------------


@api_router.post("/projects/{project_id}/export")
def export_project(project_id: str, payload: ExportRequest, client: Dict[str, object] = Depends(get_client_from_token)):
    get_project_for_client(project_id, client["id"])
    export_id = str(uuid4())
    created_at = now_iso()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO exports (id, project_id, format, size, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (export_id, project_id, payload.format.upper(), "1.2 MB", created_at),
        )
    return {"message": f"Export to {payload.format} queued"}


@api_router.get("/projects/{project_id}/exports")
def export_history(project_id: str, client: Dict[str, object] = Depends(get_client_from_token)):
    get_project_for_client(project_id, client["id"])
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT format, size, created_at FROM exports WHERE project_id = ? ORDER BY created_at DESC",
            (project_id,),
        ).fetchall()
    return [
        {
            "date": datetime.fromisoformat(row["created_at"].replace("Z", "")).strftime("%d %b %Y"),
            "format": row["format"],
            "size": row["size"],
        }
        for row in rows
    ]


# -----------------------------
# Client settings endpoints
# -----------------------------


@api_router.get("/clients/me/subscription")
def get_subscription(client: Dict[str, object] = Depends(get_client_from_token)):
    with get_connection() as conn:
        plan_row = None
        if client["plan_id"]:
            plan_row = conn.execute(
                "SELECT * FROM plans WHERE id = ?",
                (client["plan_id"],),
            ).fetchone()

        projects_count = conn.execute(
            "SELECT COUNT(1) AS cnt FROM projects WHERE client_id = ?",
            (client["id"],),
        ).fetchone()["cnt"]

        exports_count = conn.execute(
            """
            SELECT COUNT(1) AS cnt
            FROM exports e
            JOIN projects p ON p.id = e.project_id
            WHERE p.client_id = ?
            """,
            (client["id"],),
        ).fetchone()["cnt"]

    plan_name = plan_row["name"] if plan_row else "Free"
    limits = parse_json(plan_row["limits"], None) if plan_row else {"projects": 3, "exports": 10}
    return {
        "plan_name": plan_name,
        "limits": limits,
        "usage": {"projects": projects_count, "exports": exports_count},
        "expires_at": None,
    }


@api_router.get("/clients/me/payments")
def get_payments(client: Dict[str, object] = Depends(get_client_from_token)):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT paid_at, amount, status
            FROM payments
            WHERE client_id = ?
            ORDER BY paid_at DESC
            """,
            (client["id"],),
        ).fetchall()
    return [{"date": row["paid_at"], "amount": row["amount"], "status": row["status"]} for row in rows]


@api_router.get("/clients/me/notifications")
def get_notifications(client: Dict[str, object] = Depends(get_client_from_token)):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, label, checked FROM notifications WHERE client_id = ?",
            (client["id"],),
        ).fetchall()
        if not rows:
            defaults = [
                ("Email уведомления о новых функциях", True),
                ("Уведомления об экспорте проектов", True),
                ("Маркетинговые рассылки", False),
                ("Советы по использованию платформы", True),
            ]
            for label, checked in defaults:
                conn.execute(
                    """
                    INSERT INTO notifications (id, client_id, label, checked)
                    VALUES (?, ?, ?, ?)
                    """,
                    (str(uuid4()), client["id"], label, int(checked)),
                )
            rows = conn.execute(
                "SELECT id, label, checked FROM notifications WHERE client_id = ?",
                (client["id"],),
            ).fetchall()

    return [{"label": row["label"], "checked": bool(row["checked"])} for row in rows]


@api_router.patch("/clients/me/notifications")
def update_notifications(payload: NotificationsUpdateRequest, client: Dict[str, object] = Depends(get_client_from_token)):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM notifications WHERE client_id = ?",
            (client["id"],),
        )
        for item in payload.notifications:
            conn.execute(
                """
                INSERT INTO notifications (id, client_id, label, checked)
                VALUES (?, ?, ?, ?)
                """,
                (
                    str(uuid4()),
                    client["id"],
                    str(item.get("label", "")),
                    int(bool(item.get("checked", False))),
                ),
            )
    return {"message": "Notifications updated"}


app.include_router(api_router)
