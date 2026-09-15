# NEXORA AI — Arquitectura Técnica (Backend)

## Tipo de arquitectura
**Monolito modular.** No microservicios. Un solo proceso FastAPI, dividido internamente en módulos independientes por dominio de negocio. Si en el futuro algún módulo necesita escalar por separado (ej: `ai` o `automations`), se puede extraer sin rediseñar todo el sistema, porque ya está desacoplado internamente.

## Estructura de carpetas
```
backend/
├── core/                  ← código compartido por todos los módulos
│   ├── config.py          ← variables de entorno (Settings con Pydantic)
│   ├── database.py        ← engine y sesión de SQLAlchemy
│   ├── security.py        ← hashing de contraseñas, creación/validación de JWT
│   └── dependencies.py    ← get_current_user, get_current_organization, get_db
│
├── auth/
├── organizations/
├── users/
├── customers/
├── projects/
├── tasks/
├── ai/
├── automations/
├── notifications/
├── analytics/
│   (cada uno con la misma estructura interna, ver abajo)
│
└── main.py                ← crea la app FastAPI, incluye todos los routers
```

## Patrón interno de cada módulo (capas)
Cada módulo de negocio sigue siempre el mismo patrón de 5 archivos:

| Archivo | Responsabilidad | Regla |
|---|---|---|
| `models.py` | Tablas de SQLAlchemy | Solo define estructura de datos, sin lógica |
| `schemas.py` | Modelos de Pydantic (request/response) | Define qué entra y sale por la API, valida formato |
| `repository.py` | Acceso a datos (queries) | Único lugar que escribe SQL/ORM directo. **Siempre filtra por `organization_id`** |
| `service.py` | Lógica de negocio | Reglas, validaciones complejas, orquesta llamadas a otros módulos |
| `router.py` | Endpoints FastAPI | Solo recibe el request, valida con `schemas`, llama a `service`. Nunca contiene lógica de negocio ni queries |

### Flujo de una petición (siempre igual, sin excepciones)
```
Cliente HTTP
    ↓
router.py           (valida entrada con schemas.py)
    ↓
service.py          (aplica reglas de negocio)
    ↓
repository.py       (consulta/escribe en la base de datos)
    ↓
models.py / PostgreSQL
    ↓
service.py          (transforma resultado si es necesario)
    ↓
router.py           (responde con schemas.py de salida)
```

## Comunicación entre módulos
Un módulo **nunca** accede directo al `repository.py` de otro módulo. Si `automations` necesita crear una tarea, llama a `tasks.service.create_task(...)`, nunca escribe directo en la tabla `tasks`. Esto mantiene las reglas de negocio de cada módulo centralizadas en un solo lugar.

```
automations/service.py
        ↓ (llama función pública)
tasks/service.py
        ↓
tasks/repository.py
        ↓
PostgreSQL
```

## Multi-tenancy (aplicación práctica)
- El JWT del usuario incluye `user_id` y, tras seleccionar organización, `organization_id`.
- `core/dependencies.py` expone `get_current_organization()`, que se inyecta en **todos** los endpoints protegidos.
- Cada función de `repository.py` que consulta datos de negocio recibe `organization_id` como parámetro obligatorio y lo usa en el `WHERE` de la query. No existe una función de repositorio que liste datos "de todas las organizaciones" salvo las usadas explícitamente por el rol Super Admin.

## Autenticación
- Login devuelve `access_token` (corta duración, ~15-30 min) + `refresh_token` (larga duración, almacenado hasheado en la tabla `refresh_tokens`).
- Cada request protegido pasa por `get_current_user` → decodifica el JWT → confirma que el usuario existe y está activo.
- La autorización por rol (`RBAC`) se aplica con un dependency adicional, ej: `require_role(["org_admin", "manager"])`.

## Manejo de errores
- Excepciones de negocio centralizadas (ej: `NotFoundError`, `PermissionDeniedError`, `ValidationError`) definidas en `core/`.
- Un exception handler global en `main.py` las traduce a respuestas HTTP consistentes: mismo formato de error en toda la API.
```json
{
  "error": "NOT_FOUND",
  "message": "Customer not found",
  "details": null
}
```

## IA y Automatizaciones (por qué son módulos, no "features sueltas")
- `ai/service.py` expone funciones genéricas (`classify()`, `extract()`, `summarize()`) que internamente eligen el proveedor (Gemini por ahora) sin que el módulo que las llama (`tasks`, `automations`) sepa qué proveedor se está usando. Esto es lo que permite cambiar de proveedor de IA sin tocar el resto del sistema.
- `automations/service.py` es quien orquesta: lee triggers, evalúa condiciones (a veces llamando a `ai/service.py`), y ejecuta acciones (llamando a `tasks/service.py`, `notifications/service.py`, etc.), registrando cada paso en `automation_executions`.

## Próximos pasos técnicos (ya definidos, no se improvisan)
1. Configurar `core/config.py` y `core/database.py`.
2. Docker Compose con PostgreSQL + Redis.
3. Modelos de SQLAlchemy reales en `models.py` de cada módulo (siguiendo `DATABASE_DESIGN.md`).
4. Primera migración con Alembic.
5. Implementación del módulo `auth` (primer módulo funcional de punta a punta).
