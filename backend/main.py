from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(title="Landing Constructor API")
api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# In-memory storage
# -----------------------------


@dataclass
class Client:
    id: str
    company_type: str
    username: str
    email: str
    password_hash: str
    plan_id: Optional[str]


@dataclass
class Plan:
    id: str
    name: str
    features: List[str]
    limits: Optional[Dict[str, int]]


@dataclass
class Template:
    id: str
    name: str
    category: str
    is_premium: bool
    preview_image: str
    description: str


@dataclass
class Project:
    id: str
    client_id: str
    name: str
    template_id: str
    created_at: str
    updated_at: str
    status: str
    thumbnail_url: str
    data: Dict[str, object]


clients_by_id: Dict[str, Client] = {}
clients_by_email: Dict[str, Client] = {}
plans_by_id: Dict[str, Plan] = {}
tokens_to_client_id: Dict[str, str] = {}
templates_by_id: Dict[str, Template] = {}
projects_by_id: Dict[str, Project] = {}
exports_by_project_id: Dict[str, List[Dict[str, str]]] = {}
notifications_by_client_id: Dict[str, List[Dict[str, object]]] = {}


def seed_plans() -> None:
    starter = Plan(
        id=str(uuid4()),
        name="Starter",
        features=["Templates: 3", "Projects: 1", "Exports: HTML"],
        limits={"projects": 1, "templates": 3},
    )
    pro = Plan(
        id=str(uuid4()),
        name="Pro",
        features=["Templates: 12", "Projects: 10", "Exports: HTML/PDF/DOCX"],
        limits={"projects": 10, "templates": 12},
    )
    enterprise = Plan(
        id=str(uuid4()),
        name="Enterprise",
        features=["Unlimited templates", "Unlimited projects", "Priority support"],
        limits=None,
    )
    for plan in (starter, pro, enterprise):
        plans_by_id[plan.id] = plan


seed_plans()


def seed_templates() -> None:
    templates = [
        Template(
            id="modern-business",
            name="Современный Бизнес",
            category="Бизнес",
            is_premium=False,
            preview_image="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600",
            description="Минималистичный шаблон для B2B компаний",
        ),
        Template(
            id="creative-agency",
            name="Креативное Агентство",
            category="Дизайн",
            is_premium=True,
            preview_image="https://images.unsplash.com/photo-1561070791-2526d30994b5?w=600",
            description="Яркий шаблон для креативных студий",
        ),
        Template(
            id="tech-startup",
            name="Tech Стартап",
            category="IT",
            is_premium=False,
            preview_image="https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600",
            description="Современный шаблон для технологических компаний",
        ),
        Template(
            id="medical-clinic",
            name="Медицинская Клиника",
            category="Медицина",
            is_premium=True,
            preview_image="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=600",
            description="Профессиональный шаблон для медицинских учреждений",
        ),
        Template(
            id="real-estate",
            name="Недвижимость",
            category="Недвижимость",
            is_premium=False,
            preview_image="https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=600",
            description="Элегантный шаблон для агентств недвижимости",
        ),
        Template(
            id="education",
            name="Образовательный Центр",
            category="Образование",
            is_premium=True,
            preview_image="https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=600",
            description="Дружелюбный шаблон для образовательных проектов",
        ),
    ]
    for template in templates:
        templates_by_id[template.id] = template


seed_templates()


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


class ErrorResponse(BaseModel):
    message: str
    fieldErrors: Optional[Dict[str, str]] = None


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


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


def get_client_from_token(authorization: Optional[str] = Header(None)) -> Client:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized"},
        )
    token = authorization.replace("Bearer ", "").strip()
    client_id = tokens_to_client_id.get(token)
    if not client_id or client_id not in clients_by_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized"},
        )
    return clients_by_id[client_id]


def get_project_for_client(project_id: str, client: Client) -> Project:
    project = projects_by_id.get(project_id)
    if not project or project.client_id != client.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Project not found"},
        )
    return project


def get_project_limit(client: Client) -> Optional[int]:
    plan = plans_by_id.get(client.plan_id) if client.plan_id else None
    if plan and plan.limits and "projects" in plan.limits:
        return plan.limits["projects"]
    if client.plan_id is None:
        return 3
    return None


# -----------------------------
# Auth endpoints
# -----------------------------


@api_router.post("/auth/register", responses={422: {"model": ErrorResponse}})
def register(payload: RegisterRequest):
    validate_registration_payload(payload)

    if payload.email in clients_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "Email already registered"},
        )

    client = Client(
        id=str(uuid4()),
        company_type=payload.company_type,
        username=payload.username.strip(),
        email=payload.email.strip(),
        password_hash=hash_password(payload.password),
        plan_id=None,
    )
    clients_by_id[client.id] = client
    clients_by_email[client.email] = client

    return {
        "id": client.id,
        "company_type": client.company_type,
        "username": client.username,
        "email": client.email,
        "plan_id": client.plan_id,
    }


@api_router.post("/auth/login")
def login(payload: LoginRequest):
    client = clients_by_email.get(payload.email)
    if not client or client.password_hash != hash_password(payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid credentials"},
        )

    token = secrets.token_urlsafe(24)
    tokens_to_client_id[token] = client.id
    return {"token": token}


@api_router.post("/auth/logout")
def logout(client: Client = Depends(get_client_from_token), authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "").strip()
    tokens_to_client_id.pop(token, None)
    return {"message": "Logged out"}


# -----------------------------
# Client endpoints
# -----------------------------


@api_router.get("/clients/me")
def get_me(client: Client = Depends(get_client_from_token)):
    return {
        "id": client.id,
        "company_type": client.company_type,
        "username": client.username,
        "email": client.email,
        "plan_id": client.plan_id,
    }


@api_router.patch("/clients/me/plan")
def select_plan(payload: PlanSelectRequest, client: Client = Depends(get_client_from_token)):
    if payload.plan_id not in plans_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Plan not found"},
        )
    client.plan_id = payload.plan_id
    clients_by_id[client.id] = client
    clients_by_email[client.email] = client
    return {"message": "Plan updated", "plan_id": payload.plan_id}


# -----------------------------
# Plans endpoints
# -----------------------------


@api_router.get("/plans")
def list_plans():
    return [asdict(plan) for plan in plans_by_id.values()]


@api_router.get("/plans/{plan_id}")
def get_plan(plan_id: str):
    plan = plans_by_id.get(plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Plan not found"},
        )
    return asdict(plan)


@api_router.post("/plans")
def create_plan(payload: PlanCreateRequest):
    plan = Plan(
        id=str(uuid4()),
        name=payload.name.strip(),
        features=payload.features,
        limits=payload.limits,
    )
    plans_by_id[plan.id] = plan
    return asdict(plan)


@api_router.patch("/plans/{plan_id}")
def update_plan(plan_id: str, payload: PlanUpdateRequest):
    plan = plans_by_id.get(plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Plan not found"},
        )
    if payload.name is not None:
        plan.name = payload.name.strip()
    if payload.features is not None:
        plan.features = payload.features
    if payload.limits is not None:
        plan.limits = payload.limits
    plans_by_id[plan.id] = plan
    return asdict(plan)


@api_router.delete("/plans/{plan_id}")
def delete_plan(plan_id: str):
    if plan_id not in plans_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Plan not found"},
        )
    plans_by_id.pop(plan_id)
    return {"message": "Plan deleted"}


# -----------------------------
# Templates endpoints
# -----------------------------


@api_router.get("/templates")
def list_templates():
    return [asdict(template) for template in templates_by_id.values()]


@api_router.get("/templates/{template_id}")
def get_template(template_id: str):
    template = templates_by_id.get(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Template not found"},
        )
    return asdict(template)


# -----------------------------
# Projects endpoints
# -----------------------------


@api_router.get("/projects")
def list_projects(client: Client = Depends(get_client_from_token)):
    return [
        asdict(project)
        for project in projects_by_id.values()
        if project.client_id == client.id
    ]


@api_router.post("/projects")
def create_project(payload: ProjectCreateRequest, client: Client = Depends(get_client_from_token)):
    project_limit = get_project_limit(client)
    if project_limit is not None:
        current_count = sum(
            1 for project in projects_by_id.values() if project.client_id == client.id
        )
        if current_count >= project_limit:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": "Project limit reached for current plan"},
            )
    project_id = str(uuid4())
    timestamp = now_iso()
    project = Project(
        id=project_id,
        client_id=client.id,
        name=payload.name.strip(),
        template_id=payload.template_id,
        created_at=timestamp,
        updated_at=timestamp,
        status=payload.status,
        thumbnail_url=payload.thumbnail_url,
        data=payload.data,
    )
    projects_by_id[project_id] = project
    return asdict(project)


@api_router.get("/projects/{project_id}")
def get_project(project_id: str, client: Client = Depends(get_client_from_token)):
    project = get_project_for_client(project_id, client)
    return asdict(project)


@api_router.patch("/projects/{project_id}")
def update_project(project_id: str, payload: ProjectUpdateRequest, client: Client = Depends(get_client_from_token)):
    project = get_project_for_client(project_id, client)
    if payload.name is not None:
        project.name = payload.name.strip()
    if payload.status is not None:
        project.status = payload.status
    if payload.thumbnail_url is not None:
        project.thumbnail_url = payload.thumbnail_url
    if payload.data is not None:
        project.data = payload.data
    project.updated_at = now_iso()
    projects_by_id[project_id] = project
    return asdict(project)


@api_router.delete("/projects/{project_id}")
def delete_project(project_id: str, client: Client = Depends(get_client_from_token)):
    project = get_project_for_client(project_id, client)
    projects_by_id.pop(project.id)
    exports_by_project_id.pop(project_id, None)
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
def export_project(project_id: str, payload: ExportRequest, client: Client = Depends(get_client_from_token)):
    get_project_for_client(project_id, client)
    history = exports_by_project_id.setdefault(project_id, [])
    history.append(
        {
            "date": datetime.utcnow().strftime("%d %b %Y"),
            "format": payload.format.upper(),
            "size": "1.2 MB",
        }
    )
    return {"message": f"Export to {payload.format} queued"}


@api_router.get("/projects/{project_id}/exports")
def export_history(project_id: str, client: Client = Depends(get_client_from_token)):
    get_project_for_client(project_id, client)
    return exports_by_project_id.get(project_id, [])


# -----------------------------
# Client settings endpoints
# -----------------------------


@api_router.get("/clients/me/subscription")
def get_subscription(client: Client = Depends(get_client_from_token)):
    plan = plans_by_id.get(client.plan_id) if client.plan_id else None
    client_projects = [project.id for project in projects_by_id.values() if project.client_id == client.id]
    projects_count = len(client_projects)
    exports_count = sum(
        len(exports_by_project_id.get(project_id, [])) for project_id in client_projects
    )
    return {
        "plan_name": plan.name if plan else "Free",
        "limits": plan.limits if plan else {"projects": 3, "exports": 10},
        "usage": {"projects": projects_count, "exports": exports_count},
        "expires_at": None,
    }


@api_router.get("/clients/me/payments")
def get_payments(client: Client = Depends(get_client_from_token)):
    return []


@api_router.get("/clients/me/notifications")
def get_notifications(client: Client = Depends(get_client_from_token)):
    if client.id not in notifications_by_client_id:
        notifications_by_client_id[client.id] = [
            {"label": "Email уведомления о новых функциях", "checked": True},
            {"label": "Уведомления об экспорте проектов", "checked": True},
            {"label": "Маркетинговые рассылки", "checked": False},
            {"label": "Советы по использованию платформы", "checked": True},
        ]
    return notifications_by_client_id[client.id]


@api_router.patch("/clients/me/notifications")
def update_notifications(payload: NotificationsUpdateRequest, client: Client = Depends(get_client_from_token)):
    notifications_by_client_id[client.id] = payload.notifications
    return {"message": "Notifications updated"}


app.include_router(api_router)
