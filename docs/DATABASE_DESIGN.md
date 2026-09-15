# NEXORA AI — Diseño de Base de Datos (PostgreSQL)

Principio rector: **toda tabla de negocio tiene `organization_id`** (aislamiento multi-tenant). Ninguna query de negocio se hace sin filtrar por organización — esto se hace cumplir en `repository.py` de cada módulo, nunca a nivel de router.

Convenciones:
- PK: `id` (UUID, no autoincremental — evita que un tenant adivine IDs de otro)
- Timestamps: `created_at`, `updated_at` (timestamptz, default now())
- Soft delete donde aplique: `deleted_at` (nullable) en vez de borrar filas de negocio

---

## 1. Núcleo (Auth + Multi-tenancy)

### `organizations`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| name | varchar | |
| slug | varchar unique | para URLs amigables |
| plan | varchar | free / pro / business (para futuro billing) |
| created_at / updated_at | timestamptz | |

### `users`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| email | varchar unique | |
| hashed_password | varchar | |
| full_name | varchar | |
| is_active | boolean | default true |
| created_at / updated_at | timestamptz | |

> Nota: un `user` puede pertenecer a varias organizaciones (multi-tenant real) → tabla puente `memberships`.

### `memberships`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| user_id | uuid FK → users | |
| organization_id | uuid FK → organizations | |
| role | varchar (enum) | super_admin / org_admin / manager / employee / viewer |
| created_at | timestamptz | |

Constraint: `unique(user_id, organization_id)` — un usuario tiene un solo rol por organización.

### `refresh_tokens`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| user_id | uuid FK → users | |
| token_hash | varchar | nunca guardar el token en texto plano |
| expires_at | timestamptz | |
| revoked | boolean | default false |
| created_at | timestamptz | |

---

## 2. Datos de negocio

### `customers`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| organization_id | uuid FK | ← aislamiento tenant |
| name | varchar | |
| email | varchar nullable | |
| phone | varchar nullable | |
| company | varchar nullable | |
| notes | text nullable | |
| created_at / updated_at / deleted_at | timestamptz | |

Índice: `(organization_id, deleted_at)` para listados rápidos.

### `projects`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| organization_id | uuid FK | |
| customer_id | uuid FK nullable → customers | |
| name | varchar | |
| description | text nullable | |
| status | varchar (enum) | planning / active / on_hold / completed |
| start_date / end_date | date nullable | |
| created_at / updated_at / deleted_at | timestamptz | |

### `tasks`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| organization_id | uuid FK | |
| project_id | uuid FK nullable → projects | |
| customer_id | uuid FK nullable → customers | (una tarea puede no venir de un proyecto, sino directo de un cliente/automatización) |
| title | varchar | |
| description | text nullable | |
| status | varchar (enum) | todo / in_progress / done / cancelled |
| priority | varchar (enum) | low / medium / high / urgent |
| assignee_id | uuid FK nullable → users | |
| due_date | timestamptz nullable | |
| created_by | varchar (enum) | 'user' / 'ai' / 'automation' ← **clave para trazabilidad: saber qué tareas creó la IA vs una persona** |
| created_at / updated_at / deleted_at | timestamptz | |

Índices: `(organization_id, status)`, `(organization_id, assignee_id)`, `(organization_id, due_date)`.

### `comments`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| task_id | uuid FK → tasks | |
| user_id | uuid FK → users | |
| content | text | |
| created_at | timestamptz | |

### `attachments`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| organization_id | uuid FK | |
| task_id | uuid FK nullable → tasks | |
| project_id | uuid FK nullable → projects | |
| file_url | varchar | (Cloudinary u otro storage) |
| file_name | varchar | |
| uploaded_by | uuid FK → users | |
| created_at | timestamptz | |

---

## 3. AI Engine

### `ai_requests`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| organization_id | uuid FK | |
| user_id | uuid FK nullable | (puede ser nulo si lo dispara una automatización) |
| module | varchar | 'classification' / 'extraction' / 'summary' / 'nl_search' |
| provider | varchar | 'gemini' / 'openai' / 'ollama' |
| prompt | text | |
| response | jsonb | respuesta estructurada de la IA |
| tokens_used | integer nullable | |
| latency_ms | integer nullable | |
| created_at | timestamptz | |

> Esta tabla es la que alimenta la métrica "AI requests" y "tiempo ahorrado" del dashboard de analytics.

---

## 4. Automation Engine (el núcleo diferenciador)

### `automations`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| organization_id | uuid FK | |
| name | varchar | |
| description | text nullable | |
| is_active | boolean | default true |
| created_by | uuid FK → users | |
| created_at / updated_at | timestamptz | |

### `automation_triggers`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| automation_id | uuid FK → automations | |
| trigger_type | varchar | 'customer_inactive' / 'task_overdue' / 'task_created' / 'schedule' |
| config | jsonb | ej: `{"days_inactive": 7}` — flexible sin cambiar el esquema |

### `automation_conditions`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| automation_id | uuid FK → automations | |
| condition_type | varchar | 'ai_evaluation' / 'field_equals' / 'priority_is' |
| config | jsonb | |

### `automation_actions`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| automation_id | uuid FK → automations | |
| action_type | varchar | 'create_task' / 'send_notification' / 'send_email' |
| config | jsonb | |
| order | integer | orden de ejecución si hay varias acciones |

### `automation_executions`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| automation_id | uuid FK → automations | |
| organization_id | uuid FK | (denormalizado a propósito, para queries rápidas de analytics) |
| status | varchar (enum) | pending / running / success / failed |
| trigger_context | jsonb | qué disparó la ejecución |
| ai_analysis | jsonb nullable | qué decidió la IA, con "confidence" si aplica |
| result | jsonb nullable | qué se ejecutó al final |
| started_at / finished_at | timestamptz | |

> Esta tabla es la que le da a NEXORA la "trazabilidad completa" que planteamos: siempre se puede responder "¿por qué se ejecutó esto?".

---

## 5. Notificaciones y auditoría

### `notifications`
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| organization_id | uuid FK | |
| user_id | uuid FK → users | destinatario |
| type | varchar | 'task_assigned' / 'automation_triggered' / 'mention' |
| title | varchar | |
| message | text | |
| is_read | boolean | default false |
| metadata | jsonb nullable | ej: `{"task_id": "..."}` para poder navegar al hacer click |
| created_at | timestamptz | |

### `activity_logs` (auditoría)
| columna | tipo | notas |
|---|---|---|
| id | uuid PK | |
| organization_id | uuid FK | |
| user_id | uuid FK nullable | (nulo si la acción la hizo el sistema/automatización) |
| action | varchar | 'CREATE_TASK' / 'UPDATE_CUSTOMER' / 'LOGIN' etc. |
| resource_type | varchar | 'task' / 'customer' / 'automation' |
| resource_id | uuid nullable | |
| metadata | jsonb nullable | detalle adicional |
| ip_address | varchar nullable | |
| created_at | timestamptz | |

---

## Diagrama de relaciones (resumen)

```
organizations 1───* memberships *───1 users
organizations 1───* customers
organizations 1───* projects ───* tasks
customers     1───* projects (opcional)
customers     1───* tasks (opcional, directo)
projects      1───* tasks
tasks         1───* comments
tasks         1───* attachments
users         1───* refresh_tokens

organizations 1───* automations 1───* automation_triggers
                                 1───* automation_conditions
                                 1───* automation_actions
                                 1───* automation_executions

organizations 1───* ai_requests
organizations 1───* notifications
organizations 1───* activity_logs
```

## Decisión de aislamiento multi-tenant
**No** usamos schemas separados por organización (eso complica migraciones y conexiones). Usamos **row-level isolation**: cada tabla de negocio tiene `organization_id`, y **todo repository.py filtra siempre por la organización del usuario autenticado** — nunca se confía en que el frontend mande el `organization_id` correcto, siempre se toma del JWT/sesión del usuario en el backend.

## Próximo paso técnico
Con este esquema cerrado, el siguiente paso es: instalar SQLAlchemy + Alembic, crear los modelos reales en cada `models.py`, y generar la primera migración. Antes de eso, dejamos corriendo Docker Compose con PostgreSQL + Redis para tener dónde aplicar esa migración.
