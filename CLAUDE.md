# Proyecto: Formulario de Servicios TCL

## Contexto

Este proyecto ya tiene diseño y plan de implementación **100% aprobados**. No hay nada que rediseñar ni preguntar — solo ejecutar el plan.

## Qué es esto

Formulario web FastAPI independiente para que clientes soliciten servicios de TCL Asesores. Guarda las respuestas en Airtable (tabla "Servicios"). Mismo estilo visual que el formulario de novedades en `C:\Users\USER\Desktop\airtable-location-form` (NO tocar ese proyecto).

## Estado actual

- Spec aprobado: `docs/superpowers/specs/2026-06-16-servicios-form-design.md`
- **Plan listo para ejecutar: `docs/superpowers/plans/2026-06-16-servicios-form.md`**
- Pendiente: crear los 5 archivos del proyecto (main.py, form.html, gracias.html, requirements.txt, render.yaml) + logo

## Qué hacer al abrir esta carpeta

Leer el plan en `docs/superpowers/plans/2026-06-16-servicios-form.md` y ejecutarlo task por task usando el skill `superpowers:executing-plans` o `superpowers:subagent-driven-development`.

## Stack

Python 3.9+, FastAPI, Uvicorn, Requests, python-multipart, HTML/CSS/JS puro.

## Airtable

- Base ID: `appLVSEg1Y2zIwvuM`
- Tabla: `Servicios`
- Token: variable de entorno `AIRTABLE_TOKEN` (mismo que usa airtable-location-form)

## Campos del formulario

| Param POST | Campo Airtable | Tipo input |
|---|---|---|
| nombre | Nombres | text |
| apellidos | Apellidos | text |
| empresa | Empresa | text |
| ciudad | Cuidad | text |
| telefono | Numero de contacto | tel |
| servicios (múltiple) | Servicio(s) de interés | checkboxes: Contabilidad, Revisoría fiscal, Tributario, Legal, Finanzas |
| cuentanos | Cuéntanos... | textarea |
| fecha + hora | Dia y horario... | date input + select 7AM-5PM → string combinado |

## Shell

PowerShell (Windows 11). Usar sintaxis PowerShell en comandos.
