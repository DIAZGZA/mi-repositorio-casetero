# 🚌 El Casetero (Línea 603) - Zaragoza para Home Assistant

Esta integración te permite realizar un seguimiento en tiempo real y diferido de los horarios de la **Línea 603 (Zaragoza - Casetas)**, operada por el Consorcio de Transportes del Área de Zaragoza (CTAAZ).

Evita perder el autobús teniendo siempre a mano el próximo horario de salida directamente en los paneles de tu casa.

---

## ✨ Características principales

* **Próximo autobús:** Muestra de forma dinámica la hora de la siguiente salida programada según el momento del día.
* **Parrilla completa:** Guarda en los atributos del sensor todos los horarios de la jornada actual (útil para crear tarjetas personalizadas).
* **Gestión de fin de servicio:** Cambia automáticamente el estado a "Fin del servicio" cuando pasa el último autobús de la noche.

---

## 🛠️ Instalación rápida a través de HACS

Para añadir este repositorio a tu Home Assistant sigue estos pasos:

1. Entra en el panel de **HACS** en tu Home Assistant.
2. Haz clic en los **tres puntos verticales** de la esquina superior derecha y selecciona **Repositorios personalizados**.
3. Pega la URL de este repositorio de GitHub.
4. En la sección *Categoría*, selecciona **Integración**.
5. Haz clic en **Añadir**.
6. Busca la integración como `Línea 603 El Casetero Zaragoza` e instálala.
7. **Reinicia** Home Assistant para aplicar los cambios.

---

## ⚙️ Configuración básica

Una vez instalado mediante HACS, añade la siguiente configuración en tu archivo `configuration.yaml` y reinicia de nuevo:

```yaml
sensor:
  - platform: casetero_603
```

---

## 📊 Ejemplo de Tarjeta para tu Interfaz (Lovelace)

Puedes usar una tarjeta tipo `Markdown` en tu panel para visualizar los próximos autobuses de forma elegante utilizando plantillas:

```yaml
type: markdown
title: "🚍 Próximo Casetero 603"
content: >
  El próximo autobús sale a las: **{{ states('sensor.casetero_603_zaragoza') }}**
  
  *Última actualización de la parrilla: {{ state_attr('sensor.casetero_603_zaragoza', 'actualizado_en') | as_timestamp | timestamp_custom('%H:%M') }}*
```
