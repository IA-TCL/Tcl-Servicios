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
