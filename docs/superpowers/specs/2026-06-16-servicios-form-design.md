# Diseño: Formulario de Servicios TCL

**Fecha:** 2026-06-16  
**Proyecto:** `C:\Users\USER\Desktop\Servicios`  
**Estado:** Aprobado

---

## Resumen

Formulario web independiente para que clientes o prospectos soliciten información sobre los servicios de TCL. Los datos se guardan en Airtable (misma base que el formulario de novedades, tabla diferente). Sin geolocalización de IP.

---

## Arquitectura

**Stack:** Python + FastAPI + HTML/CSS puro + Uvicorn  
**Deploy:** Render.com (servicio web independiente, plan free)

### Estructura de archivos

```
Servicios/
├── main.py
├── requirements.txt
├── render.yaml
├── static/
│   └── logo.png
└── templates/
    ├── form.html
    └── gracias.html
```

### Rutas

| Método | Ruta | Descripción |
|---|---|---|
| GET / HEAD | `/` | Redirige a `/form` |
| GET | `/form` | Muestra el formulario |
| POST | `/submit` | Procesa y guarda en Airtable |
| GET | `/gracias` | Página de confirmación |

---

## Integración con Airtable

- **Base ID:** `appLVSEg1Y2zIwvuM` (misma que formulario de novedades)
- **Tabla:** `Servicios`
- **Token:** misma variable de entorno `AIRTABLE_TOKEN`

### Variables de entorno (Render)

| Variable | Valor |
|---|---|
| `AIRTABLE_TOKEN` | Token personal de Airtable |
| `AIRTABLE_BASE_ID` | `appLVSEg1Y2zIwvuM` |
| `AIRTABLE_TABLE` | `Servicios` |

---

## Campos del formulario

| Campo HTML | Nombre en Airtable | Tipo input | Validación |
|---|---|---|---|
| `nombre` | Nombres | `text` | required, sin números |
| `apellidos` | Apellidos | `text` | required, sin números |
| `empresa` | Empresa | `text` | required |
| `ciudad` | Cuidad | `text` | required |
| `telefono` | Numero de contacto | `tel` | required |
| `servicios` | Servicio(s) de interés | checkboxes múltiples | al menos 1 requerido |
| `cuentanos` | Cuéntanos... | `textarea` | required |
| `fecha` | Dia y horario... | `date` + `select` hora | required |

### Opciones de "Servicio(s) de interés"
- Contabilidad
- Revisoría fiscal
- Tributario
- Legal
- Finanzas

### Opciones de hora (select)
7:00 AM, 8:00 AM, 9:00 AM, 10:00 AM, 11:00 AM, 12:00 PM, 1:00 PM, 2:00 PM, 3:00 PM, 4:00 PM, 5:00 PM

El campo "Dia y horario..." se envía a Airtable como un string combinado: `"2026-06-20 a las 9:00 AM"`.

---

## Layout del formulario

Mismo estilo visual que el formulario de novedades (tema verde oscuro `#1b3129` / `#2A4038`, card blanca, fuente Inter, animaciones CSS de entrada).

```
┌─────────────────────────────────────────┐
│  [Logo TCL]                             │
│  Solicitud de servicios                 │
│  ─────────────────────────────────────  │
│                                         │
│  [ Nombres        ] [ Apellidos       ] │
│  [ Empresa        ] [ Ciudad          ] │
│  [ Nro. contacto  ] [ Fecha  ] [ Hora ] │
│                                         │
│  Servicio(s) de interés                 │
│  ☐ Contabilidad  ☐ Revisoría fiscal     │
│  ☐ Tributario    ☐ Legal  ☐ Finanzas    │
│                                         │
│  [ Cuéntanos... (textarea)            ] │
│                                         │
│  [↺ Borrar]                [Enviar →]   │
└─────────────────────────────────────────┘
```

- Filas 1-2: grid 2 columnas (igual al formulario actual)
- Fila 3: grid 3 columnas (teléfono, fecha, hora)
- Servicios: checkboxes estilizados como pills, ancho completo
- Cuéntanos: textarea, ancho completo
- Responsive: colapsa a 1 columna en pantallas < 580px

---

## Comportamiento JavaScript

- Deshabilitar botón "Enviar" al hacer submit (previene doble envío)
- Bloquear números en campos de texto (Nombres, Apellidos, Empresa, Ciudad)
- Validar que al menos un checkbox de servicios esté marcado antes de enviar

---

## Manejo de errores

- Si Airtable responde con error: página HTML con código de estado y detalle del error (igual al formulario actual)
- Campos vacíos: validación nativa HTML5 (`required`)

---

## render.yaml

```yaml
services:
  - type: web
    name: tcl-servicios
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Lo que NO incluye

- Geolocalización por IP
- Autenticación
- Base de datos propia
- Captcha
