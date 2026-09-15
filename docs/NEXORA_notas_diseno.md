# NEXORA AI — Notas de dirección visual (para el Día 5)

> **DECISIÓN CERRADA — aplica a partir de aquí en todo el código.**
> No es un punto de partida a discutir cada vez: todo componente que se escriba desde el Día 5 debe seguir este sistema de diseño. Esto evita reescribir UI a mitad de proyecto.

Objetivo: que NO se vea como el típico dashboard de portafolio de LinkedIn (sidebar morado-azul + cards con sombra + tabla). Referencias: Linear, Raycast, herramientas de terminal/observabilidad — no plantillas de admin genéricas.

## Dirección elegida (definitiva)
1. **Identidad visual base (toda la app):** estética "centro de control operativo" — Linear / Raycast / Vercel Dashboard. Espacio negativo generoso, tipografía protagonista, bordes definidos (no sombras difusas), color usado con moderación.
2. **Módulo de IA y Automatizaciones (el diferenciador del producto):** panel de copiloto conversacional a un costado + automatizaciones representadas como línea de tiempo/pipeline (Trigger → IA → Condición → Acción), no como tabla.
3. **Extra de pulido (Día 14, no prioritario ahora):** buscador de comandos rápido estilo Raycast (Ctrl+K).

## Regla técnica obligatoria: Design Tokens (para permitir tema claro/oscuro sin refactor)
Todo color, tipografía y espaciado se define como **variable CSS (token)**, nunca "hardcodeado" directo en un componente.

Ejemplo de la estructura de tokens que usaremos (Tailwind + CSS variables):
```css
:root[data-theme="dark"] {
  --bg-base: #0A0A0B;
  --bg-surface: #141416;
  --border: #26262A;
  --text-primary: #F4F4F5;
  --text-secondary: #A1A1AA;
  --accent: #3B82F6;
  --success: #22C55E;
  --error: #EF4444;
  --warning: #EAB308;
}

:root[data-theme="light"] {
  --bg-base: #FFFFFF;
  --bg-surface: #F4F4F5;
  --border: #E4E4E7;
  --text-primary: #18181B;
  --text-secondary: #52525B;
  --accent: #2563EB;
  --success: #16A34A;
  --error: #DC2626;
  --warning: #CA8A04;
}
```
- El toggle de tema solo cambia el atributo `data-theme` en el `<html>` (o `class`), guardado en el estado del usuario (idealmente persistido en su perfil en BD, no solo localStorage, ya que NEXORA es multi-tenant con cuentas reales).
- **Ningún componente debe usar un color fijo como `bg-[#141416]` directo.** Siempre a través del token/clase de Tailwind mapeada a la variable (ej. `bg-surface`, `text-primary`).
- Esto se configura UNA vez en el Día 5 (setup de Tailwind + tokens) y después se respeta en todo el código restante — por eso es importante dejarlo bien armado desde el principio y no "ya lo arreglo después".

## Principios generales
- **Espacio negativo generoso.** No llenar cada pixel con una card. Dejar respirar el contenido.
- **Bordes definidos, no sombras difusas.** Un borde de 1px sutil comunica más "producto real" que un `box-shadow` grande.
- **Color casi monocromático + UN acento.** Fondo oscuro neutro (no morado), texto en escala de grises, y un solo color vibrante reservado para acciones/estados importantes (éxito, alerta, foco).
- **Tipografía como protagonista.** El tamaño y peso de la fuente hacen jerarquía, no el color.
- **Densidad de información alta pero ordenada** (como Linear/Raycast) en vez de "cards gigantes con poco contenido" (look genérico de plantilla).

## Paleta de color (punto de partida, ajustar en Día 5)
- Fondo base: `#0A0A0B` (casi negro, no azul-negro)
- Fondo secundario/cards: `#141416`
- Bordes: `#26262A`
- Texto principal: `#F4F4F5`
- Texto secundario: `#A1A1AA`
- Acento único: elegir UNO — verde lima `#A3E635`, o naranja quemado `#F97316`, o un azul eléctrico poco común `#3B82F6` con muy poco uso (evitar el morado/violeta, está sobreusado en SaaS de IA)
- Estados: éxito `#22C55E`, error `#EF4444`, advertencia `#EAB308` (usar con moderación, no como fondo de card completo)

## Tipografía
- Headers / marca: una sans-serif con carácter (ej. **Space Grotesk**, **Geist**, o **General Sans**) — no Inter/Roboto default
- Datos, números, código, IDs: **monoespaciada** (ej. **JetBrains Mono**, **IBM Plex Mono**) — refuerza sensación de "herramienta técnica seria"
- Cuerpo de texto: la misma sans-serif de headers, en peso regular

## Ideas de layout distintas al dashboard genérico
1. **Vista principal tipo copiloto:** panel de chat con la IA a un costado (fijo), y el "resultado" (tareas creadas, automatizaciones disparadas) apareciendo como tarjetas generadas en tiempo real al lado, no como un menú estático.
2. **Automatizaciones como línea de tiempo/pipeline**, no tabla: cada ejecución se ve como un flujo horizontal de pasos (Trigger → IA → Condición → Acción) con estados animados, similar a un pipeline de CI/CD.
3. **Comandos rápidos estilo Raycast** (Cmd+K / Ctrl+K) para navegar y ejecutar acciones sin mouse — se ve inmediatamente "pro".
4. **Números y métricas con tipografía mono grande**, sin íconos decorativos de relleno.

## Referencias a revisar antes del Día 5
- linear.app (blog de diseño, tienen posts explicando decisiones de UI)
- raycast.com
- Vercel Dashboard (vercel.com) — buen ejemplo de dark mode con acento mínimo
- Buscar en Dribbble/Mobbin: "developer tool dashboard dark mode" (evitar buscar "admin dashboard", ahí sale todo el look genérico que queremos evitar)

## Qué evitar explícitamente
- Sidebar azul con ícono de rayo/cohete genérico
- Cards con gradiente de fondo
- Emojis grandes decorativos en vacíos de datos (ej. 📬 "no jobs yet")
- Paleta morado + azul + rosa (el combo "IA startup" sobreusado en 2024-2026)
- Iconografía de "flat illustration" genérica (personas 3D, ilustraciones de stock)

---
*Este documento es un punto de partida, no una decisión final. Revisar y ajustar en el Día 5 con la skill de diseño de frontend antes de implementar.*
