# Restaurante SupoBase - Arquitectura Senior

Esta documentación describe la nueva estructura profesional del proyecto, diseñada para escalabilidad, seguridad y despliegue continuo.

## Estructura del Proyecto

```text
/Restaurante_SupoBase
  /backend
    /app
      main.py           # Fábrica de la Aplicación (Entry Point)
      /routes           # Blueprints (Controladores de API)
      /services         # Capa de Negocio (Lógica pura)
      /utils            # Helpers (Logging, Validaciones)
  /supabase
    /migrations         # SQL versionado para control de cambios
  /frontend
    /templates          # Plantillas Jinja2
    /static             # Assets (CSS, JS, Img)
  /docs                 # Documentación técnica
```

## Capas de la Aplicación

1. **Capa de Datos (Supabase)**: 
   - Seguridad mediante **RLS (Row Level Security)**.
   - Identidad gestionada por **Supabase Auth**.
   - Integridad mediante relaciones normalizadas (`orders` -> `order_items`).

2. **Capa de Servicios (Services)**:
   - Contiene la lógica de negocio pura.
   - Independiente de Flask; permite pruebas unitarias fáciles.
   - Interactúa directamente con el SDK de Supabase.

3. **Capa de Rutas (Blueprints)**:
   - Actúa como orquestador (BFF).
   - Valida entradas básicas y delega en los servicios.
   - Retorna respuestas JSON o renderiza plantillas.

4. **Observabilidad (Utils/Logging)**:
   - Implementa **Logging Estructurado en JSON**.
   - Facilita el monitoreo en entornos serverless como Vercel.

## Flujo de Trabajo Sugerido

1. **Cambios en DB**: Añadir un nuevo archivo en `/supabase/migrations`.
2. **Nueva Lógica**: Crear un método en el servicio correspondiente en `/backend/app/services`.
3. **Nuevo Endpoint**: Registrar la ruta en el Blueprint adecuado en `/backend/app/routes`.

---
Arquitectura diseñada por **Antigravity** para nivel Mid/Senior Developer.
