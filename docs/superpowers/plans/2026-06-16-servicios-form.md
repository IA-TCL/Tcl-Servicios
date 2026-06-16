# Formulario de Servicios TCL — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crear un servidor web FastAPI independiente en `C:\Users\USER\Desktop\Servicios` con un formulario de 8 campos que guarda respuestas en Airtable (tabla "Servicios"), con el mismo estilo visual verde oscuro del formulario de novedades existente.

**Architecture:** FastAPI sirve el formulario HTML desde `templates/`, recibe el POST `/submit`, construye el payload y llama a la API REST de Airtable para crear un registro. Sin geolocalización de IP. Desplegable en Render.com vía `render.yaml`.

**Tech Stack:** Python 3.9+, FastAPI, Uvicorn, Requests, python-multipart, HTML/CSS/JS puro.

---

### Task 1: Scaffold del proyecto

**Files:**
- Create: `requirements.txt`
- Create: `render.yaml`
- Create: `static/` (carpeta)
- Copy: logo desde proyecto existente → `static/logo.png`

- [ ] **Step 1: Crear carpetas**

```powershell
New-Item -ItemType Directory -Force "C:\Users\USER\Desktop\Servicios\static"
New-Item -ItemType Directory -Force "C:\Users\USER\Desktop\Servicios\templates"
```

Expected: carpetas creadas sin error.

- [ ] **Step 2: Copiar logo**

```powershell
Copy-Item "C:\Users\USER\Desktop\airtable-location-form\static\logo.png" "C:\Users\USER\Desktop\Servicios\static\logo.png"
```

Expected: archivo `static\logo.png` presente.

- [ ] **Step 3: Crear requirements.txt**

Contenido de `C:\Users\USER\Desktop\Servicios\requirements.txt`:
```
fastapi
uvicorn
requests
python-multipart
```

- [ ] **Step 4: Crear render.yaml**

Contenido de `C:\Users\USER\Desktop\Servicios\render.yaml`:
```yaml
services:
  - type: web
    name: tcl-servicios
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

- [ ] **Step 5: Inicializar git y commit**

```powershell
cd C:\Users\USER\Desktop\Servicios
git init
git add requirements.txt render.yaml static/logo.png
git commit -m "chore: scaffold proyecto servicios"
```

---

### Task 2: Backend (main.py)

**Files:**
- Create: `C:\Users\USER\Desktop\Servicios\main.py`

- [ ] **Step 1: Crear main.py con el contenido siguiente**

```python
import os
from pathlib import Path
from typing import List
from urllib.parse import quote

import requests
from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

TEMPLATES = Path("templates")

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "appLVSEg1Y2zIwvuM")
AIRTABLE_TABLE = os.getenv("AIRTABLE_TABLE", "Servicios")


@app.api_route("/", methods=["GET", "HEAD"])
async def root(request: Request):
    if request.method == "HEAD":
        return Response(status_code=200)
    return RedirectResponse("/form")


@app.get("/form", response_class=HTMLResponse)
async def form():
    return (TEMPLATES / "form.html").read_text(encoding="utf-8")


@app.post("/submit")
async def submit(
    nombre: str = Form(...),
    apellidos: str = Form(...),
    empresa: str = Form(...),
    ciudad: str = Form(...),
    telefono: str = Form(...),
    cuentanos: str = Form(...),
    fecha: str = Form(...),
    hora: str = Form(...),
    servicios: List[str] = Form(default=[]),
):
    dia_horario = f"{fecha} a las {hora}"

    fields = {
        "Nombres": nombre,
        "Apellidos": apellidos,
        "Empresa": empresa,
        "Cuidad": ciudad,
        "Numero de contacto": telefono,
        "Servicio(s) de interés": servicios,
        "Cuéntanos...": cuentanos,
        "Dia y horario...": dia_horario,
    }
    fields = {k: v for k, v in fields.items() if v}

    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{quote(AIRTABLE_TABLE)}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"fields": fields, "typecast": True}

    debug_info = (
        f"URL: {url}\n"
        f"BASE_ID: {AIRTABLE_BASE_ID}\n"
        f"TABLE: {AIRTABLE_TABLE}\n"
        f"TOKEN configurado: {'SI' if AIRTABLE_TOKEN else 'NO'}\n"
        f"Campos enviados: {fields}"
    )

    try:
        print("FIELDS:", fields)
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
    except Exception as exc:
        print("EXCEPCION al llamar Airtable:", exc)
        return HTMLResponse(
            f"<h2>Error al conectar con Airtable</h2>"
            f"<pre>{exc}</pre>"
            f"<hr><pre>{debug_info}</pre>",
            status_code=500,
        )

    if resp.status_code not in (200, 201):
        print("ERROR Airtable:", resp.status_code, resp.text)
        return HTMLResponse(
            f"<h2>Error Airtable {resp.status_code}</h2>"
            f"<pre>{resp.text}</pre>"
            f"<hr><pre>{debug_info}</pre>",
            status_code=500,
        )

    return RedirectResponse("/gracias", status_code=303)


@app.get("/gracias", response_class=HTMLResponse)
async def gracias():
    return (TEMPLATES / "gracias.html").read_text(encoding="utf-8")
```

- [ ] **Step 2: Verificar sintaxis**

```powershell
cd C:\Users\USER\Desktop\Servicios
python -c "import ast; ast.parse(open('main.py').read()); print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```powershell
git add main.py
git commit -m "feat: backend FastAPI rutas y envio a Airtable"
```

---

### Task 3: Página de confirmación (gracias.html)

**Files:**
- Create: `C:\Users\USER\Desktop\Servicios\templates\gracias.html`

- [ ] **Step 1: Crear gracias.html**

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>¡Gracias!</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 32px 16px;
            background-color: #1b3129;
            background-image:
                radial-gradient(ellipse at 15% 40%, rgba(61,107,89,.45) 0%, transparent 55%),
                radial-gradient(ellipse at 85% 15%, rgba(42,64,56,.6)  0%, transparent 50%),
                radial-gradient(ellipse at 55% 85%, rgba(26,53,48,.5)  0%, transparent 50%);
        }

        .card {
            background: #fff;
            border-radius: 20px;
            padding: 44px 48px 48px;
            width: 100%;
            max-width: 480px;
            box-shadow: 0 24px 64px rgba(0,0,0,.28), 0 4px 16px rgba(0,0,0,.12);
            border-top: 4px solid #2A4038;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            animation: slideUp .55s cubic-bezier(.16,1,.3,1) both;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(32px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .logo-img { width: 200px; height: auto; display: block; margin-bottom: 24px; }

        .divider {
            border: none;
            height: 1px;
            width: 100%;
            background: linear-gradient(to right, transparent, #d1d5db, transparent);
            margin-bottom: 32px;
        }

        .icon-wrap {
            width: 68px;
            height: 68px;
            background: #dcfce7;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 22px;
            animation: scaleIn .45s cubic-bezier(.175,.885,.32,1.275) .35s both,
                       pulse 2.5s ease 1.2s infinite;
        }

        @keyframes scaleIn {
            from { opacity: 0; transform: scale(.4); }
            to   { opacity: 1; transform: scale(1); }
        }

        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 0 0   rgba(22,163,74,.25); }
            50%       { box-shadow: 0 0 0 12px rgba(22,163,74,.0);  }
        }

        .icon-wrap svg {
            width: 32px; height: 32px;
            stroke: #16a34a; stroke-width: 2.5;
            fill: none; stroke-linecap: round; stroke-linejoin: round;
            overflow: visible;
        }

        .icon-wrap svg polyline {
            stroke-dasharray: 40;
            stroke-dashoffset: 40;
            animation: drawCheck .5s ease .8s forwards;
        }

        @keyframes drawCheck { to { stroke-dashoffset: 0; } }

        h1 {
            font-size: 24px; font-weight: 800; color: #111827;
            margin-bottom: 10px; letter-spacing: -.3px;
            animation: fadeIn .4s ease .5s both;
        }

        p {
            font-size: 14px; color: #6b7280; line-height: 1.7;
            animation: fadeIn .4s ease .65s both;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to   { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="card">
        <img src="/static/logo.png" alt="TCL" class="logo-img">
        <div class="divider"></div>
        <div class="icon-wrap">
            <svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
        </div>
        <h1>¡Solicitud enviada!</h1>
        <p>Hemos recibido tu solicitud correctamente.<br>Pronto nos pondremos en contacto contigo.</p>
    </div>
</body>
</html>
```

- [ ] **Step 2: Commit**

```powershell
git add templates/gracias.html
git commit -m "feat: pagina de confirmacion gracias.html"
```

---

### Task 4: Formulario principal (form.html)

**Files:**
- Create: `C:\Users\USER\Desktop\Servicios\templates\form.html`

- [ ] **Step 1: Crear form.html**

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Solicitud de Servicios</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 32px 16px;
            background-color: #1b3129;
            background-image:
                radial-gradient(circle, rgba(255,255,255,.055) 1px, transparent 1px),
                radial-gradient(ellipse at 15% 40%, rgba(61,107,89,.45) 0%, transparent 55%),
                radial-gradient(ellipse at 85% 15%, rgba(42,64,56,.60) 0%, transparent 50%),
                radial-gradient(ellipse at 55% 85%, rgba(26,53,48,.50) 0%, transparent 50%);
            background-size: 28px 28px, 100% 100%, 100% 100%, 100% 100%;
        }

        .card {
            background: linear-gradient(160deg, #ffffff 0%, #f8faf9 100%);
            border-radius: 20px;
            padding: 40px 48px 36px;
            width: 100%;
            max-width: 820px;
            box-shadow: 0 24px 64px rgba(0,0,0,.28), 0 4px 16px rgba(0,0,0,.12);
            border-top: 4px solid #2A4038;
            animation: slideUp .55s cubic-bezier(.16,1,.3,1) both;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(32px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .logo { margin-bottom: 24px; }
        .logo-img { height: auto; width: 180px; display: block; }

        .header { border-left: 3px solid #2A4038; padding-left: 14px; margin-bottom: 24px; }

        h1 { font-size: 28px; font-weight: 800; color: #111827; margin-bottom: 5px; letter-spacing: -0.4px; }

        .subtitle { font-size: 13px; color: #6b7280; line-height: 1.6; font-style: italic; }

        .divider {
            border: none; height: 1px;
            background: linear-gradient(to right, #2A4038 0%, #d1d5db 30%, transparent 100%);
            margin-bottom: 28px;
        }

        /* Grid de 6 columnas:
           - campos normales: span 3 (= mitad del ancho, simula 2 columnas)
           - fila teléfono/fecha/hora: span 2 cada uno (= tercios)
           - servicios y cuéntanos: span 6 (ancho completo) */
        .grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 20px 36px;
        }

        .col-3 { grid-column: span 3; }
        .col-2 { grid-column: span 2; }
        .col-6 { grid-column: span 6; }

        .field {
            opacity: 0;
            animation: fieldIn .45s cubic-bezier(.16,1,.3,1) both;
        }
        .field:nth-child(1) { animation-delay: .20s; }
        .field:nth-child(2) { animation-delay: .28s; }
        .field:nth-child(3) { animation-delay: .36s; }
        .field:nth-child(4) { animation-delay: .44s; }
        .field:nth-child(5) { animation-delay: .52s; }
        .field:nth-child(6) { animation-delay: .60s; }
        .field:nth-child(7) { animation-delay: .68s; }
        .field:nth-child(8) { animation-delay: .76s; }
        .field:nth-child(9) { animation-delay: .84s; }

        @keyframes fieldIn {
            from { opacity: 0; transform: translateY(14px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .field label {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            font-weight: 600;
            color: #374151;
            margin-bottom: 4px;
            letter-spacing: .1px;
        }

        .field label svg { color: #2A4038; flex-shrink: 0; }

        .field .hint { font-size: 11.5px; color: #9ca3af; line-height: 1.5; margin-bottom: 8px; font-style: italic; }

        .input-wrap { position: relative; }

        .input-wrap .icon {
            position: absolute;
            left: 12px; top: 50%;
            transform: translateY(-50%);
            color: #c4c9d4;
            pointer-events: none;
            transition: color .2s;
        }

        .input-wrap:focus-within .icon { color: #2A4038; }

        .field input,
        .field select {
            width: 100%;
            padding: 10px 12px 10px 38px;
            font-size: 14px;
            font-family: inherit;
            border: 1.5px solid #e5e7eb;
            border-radius: 10px;
            color: #111827;
            background: #f9fafb;
            transition: border-color .2s, box-shadow .2s, background .2s;
            cursor: pointer;
        }

        .field input::placeholder { color: #c4c9d4; font-style: italic; }

        .field input:hover,
        .field select:hover { border-color: #c8ced8; background: #fff; }

        .field input:focus,
        .field select:focus {
            outline: none;
            border-color: #2A4038;
            background: #fff;
            box-shadow: 0 0 0 3px rgba(42,64,56,.1);
        }

        .field textarea {
            width: 100%;
            padding: 10px 12px;
            font-size: 14px;
            font-family: inherit;
            border: 1.5px solid #e5e7eb;
            border-radius: 10px;
            color: #111827;
            background: #f9fafb;
            resize: vertical;
            min-height: 100px;
            transition: border-color .2s, box-shadow .2s, background .2s;
        }

        .field textarea::placeholder { color: #c4c9d4; font-style: italic; }

        .field textarea:hover { border-color: #c8ced8; background: #fff; }

        .field textarea:focus {
            outline: none;
            border-color: #2A4038;
            background: #fff;
            box-shadow: 0 0 0 3px rgba(42,64,56,.1);
        }

        /* Pills de checkboxes */
        .checkboxes-wrap { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 4px; }

        .checkbox-pill {
            display: flex;
            align-items: center;
            gap: 7px;
            padding: 8px 16px;
            border: 1.5px solid #e5e7eb;
            border-radius: 50px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            color: #374151;
            background: #f9fafb;
            transition: border-color .2s, background .2s, color .2s;
            user-select: none;
        }

        .checkbox-pill:hover { border-color: #2A4038; background: #fff; }

        .checkbox-pill input[type="checkbox"] { display: none; }

        .checkbox-pill.checked { border-color: #2A4038; background: #2A4038; color: #fff; }

        /* Footer */
        .footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 32px;
            padding-top: 22px;
            border-top: 1px solid #f3f4f6;
        }

        .btn-clear {
            background: none; border: none;
            color: #1b3129; font-size: 13px; font-family: inherit; font-weight: 500;
            cursor: pointer; display: flex; align-items: center; gap: 6px;
            padding: 8px 12px; border-radius: 8px;
            transition: background .15s, color .15s;
        }

        .btn-clear:hover { background: #f3f4f6; color: #3d4350; }

        .btn-submit {
            position: relative; overflow: hidden;
            background: linear-gradient(135deg, #2A4038 0%, #3d6b59 100%);
            color: #fff; border: none; border-radius: 10px;
            padding: 11px 36px; font-size: 14px; font-weight: 600;
            font-family: inherit; letter-spacing: .3px;
            cursor: pointer; transition: transform .2s, box-shadow .2s;
            box-shadow: 0 2px 10px rgba(42,64,56,.35);
        }

        .btn-submit::after {
            content: ''; position: absolute;
            top: 0; left: -80%; width: 55%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,.22), transparent);
            transform: skewX(-20deg); transition: left .55s ease;
        }

        .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(42,64,56,.4); }
        .btn-submit:hover::after { left: 150%; }
        .btn-submit:active { transform: translateY(0); box-shadow: 0 2px 10px rgba(42,64,56,.35); }
        .btn-submit:disabled { opacity: .65; cursor: not-allowed; transform: none; }

        @media (max-width: 580px) {
            .card { padding: 28px 20px 24px; }
            .col-3, .col-2, .col-6 { grid-column: span 6; }
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="logo">
            <img src="/static/logo.png" alt="TCL" class="logo-img">
        </div>

        <div class="header">
            <h1>Solicitud de servicios</h1>
            <p class="subtitle">Complete el formulario y nos pondremos en contacto con usted.</p>
        </div>

        <div class="divider"></div>

        <form action="/submit" method="post" id="main-form">
            <div class="grid">

                <!-- Nombres -->
                <div class="field col-3">
                    <label for="nombre">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                        Nombres
                    </label>
                    <p class="hint">Ingrese su nombre o nombres.</p>
                    <div class="input-wrap">
                        <input id="nombre" name="nombre" type="text" placeholder="Ej. María Fernanda" required>
                        <span class="icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
                    </div>
                </div>

                <!-- Apellidos -->
                <div class="field col-3">
                    <label for="apellidos">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                        Apellidos
                    </label>
                    <p class="hint">Ingrese sus apellidos completos.</p>
                    <div class="input-wrap">
                        <input id="apellidos" name="apellidos" type="text" placeholder="Ej. González Torres" required>
                        <span class="icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
                    </div>
                </div>

                <!-- Empresa -->
                <div class="field col-3">
                    <label for="empresa">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M16 6h.01M12 6h.01M12 10h.01M8 10h.01M16 10h.01M12 14h.01M8 14h.01M16 14h.01"/></svg>
                        Empresa
                    </label>
                    <p class="hint">Nombre de su empresa u organización.</p>
                    <div class="input-wrap">
                        <input id="empresa" name="empresa" type="text" placeholder="Ej. Grupo XYZ S.A.S" required>
                        <span class="icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M16 6h.01M12 6h.01M12 10h.01M8 10h.01M16 10h.01M12 14h.01M8 14h.01M16 14h.01"/></svg></span>
                    </div>
                </div>

                <!-- Ciudad -->
                <div class="field col-3">
                    <label for="ciudad">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                        Ciudad
                    </label>
                    <p class="hint">Ciudad donde se encuentra su empresa.</p>
                    <div class="input-wrap">
                        <input id="ciudad" name="ciudad" type="text" placeholder="Ej. Bogotá" required>
                        <span class="icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg></span>
                    </div>
                </div>

                <!-- Teléfono -->
                <div class="field col-2">
                    <label for="telefono">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.42 2 2 0 0 1 3.6 1.24h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9a16 16 0 0 0 6 6l.92-.92a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                        Número de contacto
                    </label>
                    <p class="hint">Teléfono o celular.</p>
                    <div class="input-wrap">
                        <input id="telefono" name="telefono" type="tel" placeholder="Ej. 300 123 4567" required>
                        <span class="icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.42 2 2 0 0 1 3.6 1.24h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9a16 16 0 0 0 6 6l.92-.92a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg></span>
                    </div>
                </div>

                <!-- Fecha preferida -->
                <div class="field col-2">
                    <label for="fecha">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
                        Fecha preferida
                    </label>
                    <p class="hint">Día para la reunión.</p>
                    <div class="input-wrap">
                        <input id="fecha" name="fecha" type="date" required>
                        <span class="icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg></span>
                    </div>
                </div>

                <!-- Horario preferido -->
                <div class="field col-2">
                    <label for="hora">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                        Horario preferido
                    </label>
                    <p class="hint">Seleccione la hora.</p>
                    <div class="input-wrap">
                        <select id="hora" name="hora" required>
                            <option value="" disabled selected>-- Seleccione --</option>
                            <option value="7:00 AM">7:00 AM</option>
                            <option value="8:00 AM">8:00 AM</option>
                            <option value="9:00 AM">9:00 AM</option>
                            <option value="10:00 AM">10:00 AM</option>
                            <option value="11:00 AM">11:00 AM</option>
                            <option value="12:00 PM">12:00 PM</option>
                            <option value="1:00 PM">1:00 PM</option>
                            <option value="2:00 PM">2:00 PM</option>
                            <option value="3:00 PM">3:00 PM</option>
                            <option value="4:00 PM">4:00 PM</option>
                            <option value="5:00 PM">5:00 PM</option>
                        </select>
                        <span class="icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></span>
                    </div>
                </div>

                <!-- Servicio(s) de interés -->
                <div class="field col-6">
                    <label>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
                        Servicio(s) de interés
                    </label>
                    <p class="hint">Seleccione uno o más servicios.</p>
                    <div class="checkboxes-wrap">
                        <label class="checkbox-pill">
                            <input type="checkbox" name="servicios" value="Contabilidad">
                            Contabilidad
                        </label>
                        <label class="checkbox-pill">
                            <input type="checkbox" name="servicios" value="Revisoría fiscal">
                            Revisoría fiscal
                        </label>
                        <label class="checkbox-pill">
                            <input type="checkbox" name="servicios" value="Tributario">
                            Tributario
                        </label>
                        <label class="checkbox-pill">
                            <input type="checkbox" name="servicios" value="Legal">
                            Legal
                        </label>
                        <label class="checkbox-pill">
                            <input type="checkbox" name="servicios" value="Finanzas">
                            Finanzas
                        </label>
                    </div>
                </div>

                <!-- Cuéntanos -->
                <div class="field col-6">
                    <label for="cuentanos">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                        Cuéntanos
                    </label>
                    <p class="hint">Descríbanos brevemente su necesidad o consulta.</p>
                    <textarea id="cuentanos" name="cuentanos" placeholder="Escriba aquí su consulta o necesidad..." required></textarea>
                </div>

            </div>

            <div class="footer">
                <button type="button" class="btn-clear" id="btn-clear">&#8635; Borrar información</button>
                <button type="submit" class="btn-submit" id="btn-submit">Enviar &rarr;</button>
            </div>
        </form>
    </div>

    <script>
        // Actualizar estado visual de pills al cambiar el checkbox
        document.querySelectorAll('.checkbox-pill input[type="checkbox"]').forEach(function(cb) {
            cb.addEventListener('change', function() {
                this.closest('.checkbox-pill').classList.toggle('checked', this.checked);
            });
        });

        // Limpiar formulario + estado visual de pills
        document.getElementById('btn-clear').addEventListener('click', function() {
            document.getElementById('main-form').reset();
            document.querySelectorAll('.checkbox-pill').forEach(function(pill) {
                pill.classList.remove('checked');
            });
        });

        // Validar al menos un servicio y deshabilitar botón al enviar
        document.getElementById('main-form').addEventListener('submit', function(e) {
            var checked = document.querySelectorAll('input[name="servicios"]:checked');
            if (checked.length === 0) {
                e.preventDefault();
                alert('Por favor seleccione al menos un servicio de interés.');
                return;
            }
            var btn = document.getElementById('btn-submit');
            btn.disabled = true;
            btn.textContent = 'Enviando…';
        });

        // Bloquear números en campos de texto
        document.querySelectorAll('input[type="text"]').forEach(function(input) {
            input.addEventListener('input', function() {
                this.value = this.value.replace(/[0-9]/g, '');
            });
        });
    </script>
</body>
</html>
```

- [ ] **Step 2: Commit**

```powershell
git add templates/form.html
git commit -m "feat: formulario principal 8 campos estilo TCL"
```

---

### Task 5: Prueba local end-to-end

**Files:** ninguno (solo verificación)

- [ ] **Step 1: Instalar dependencias**

```powershell
cd C:\Users\USER\Desktop\Servicios
pip install -r requirements.txt
```

Expected: instalación sin errores.

- [ ] **Step 2: Levantar servidor con token de Airtable**

```powershell
$env:AIRTABLE_TOKEN = "TU_TOKEN_AQUI"
$env:AIRTABLE_TABLE = "Servicios"
uvicorn main:app --reload --port 8001
```

Abrir `http://localhost:8001/form` en el navegador.

- [ ] **Step 3: Verificar apariencia visual**

Confirmar:
- Fondo verde oscuro con puntos, card blanca con borde verde en la parte superior
- Logo TCL visible, título "Solicitud de servicios"
- 7 campos de texto/fecha/hora con iconos a la izquierda
- 5 pills (Contabilidad, Revisoría fiscal, Tributario, Legal, Finanzas) — se marcan en verde al hacer clic
- Textarea "Cuéntanos" de ancho completo
- Animaciones de entrada escalonadas

- [ ] **Step 4: Enviar prueba y verificar Airtable**

Llenar todos los campos, seleccionar al menos un servicio, clic en "Enviar".

Verificar:
- Redirige a `/gracias` con animación del check verde
- En Airtable (tabla "Servicios") aparece el nuevo registro con todos los campos

- [ ] **Step 5: Commit final**

```powershell
git add docs/
git commit -m "chore: proyecto servicios completo y listo para deploy"
```
