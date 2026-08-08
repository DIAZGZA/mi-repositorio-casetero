# 🚌 Home Assistant - El Casetero (Línea 603 Zaragoza)

[![hacs_badge](https://shields.io)](https://github.com)
[![License](https://shields.io)](LICENSE)
[![Home Assistant](https://shields.io)](https://home-assistant.io)

Componente personalizado (*Custom Component*) para **Home Assistant** que extrae automáticamente los horarios de la **Línea 603 (Zaragoza - Casetas)** directamente desde la web del Consorcio de Transportes del Área de Zaragoza (CTAAZ).

Muestra el tiempo restante o la hora exacta del próximo autobús y almacena toda la parrilla del día para integrarla en tus automatizaciones y paneles de control.

---

## 🚀 Características

* 🕒 **Estado en tiempo real:** Sensor que indica el próximo autobús disponible según la hora actual.
* 📋 **Atributos enriquecidos:** Listado completo con todos los horarios del día en los atributos del sensor (`todos_los_horarios_dia`).
* 🛌 **Modo nocturno:** Actualización automática a "Fin del servicio" cuando termina el horario diario.
* ⚡ **Liviano:** Optimizado con caché interna para no saturar la web de origen con peticiones innecesarias.

---

## 🛠️ Instalación

### Método 1: A través de HACS (Recomendado)

1. Abre **HACS** en tu instancia de Home Assistant.
2. Ve a la pestaña **Integraciones**.
3. Haz clic en los tres puntos de la esquina superior derecha y selecciona **Repositorios personalizados**.
4. Pega la URL de este repositorio: `https://github.com`.
5. En *Categoría*, selecciona **Integración** y pulsa **Añadir**.
6. Busca `Línea 603 El Casetero Zaragoza`, haz clic en descargar y **reinicia Home Assistant**.

### Método 2: Instalación Manual

1. Descarga el archivo `.zip` de este repositorio.
2. Copia la carpeta `custom_components/casetero_603/` dentro del directorio `config/` de tu instalación de Home Assistant.
3. Asegúrate de que la estructura queda así: `config/custom_components/casetero_603/sensor.py`.
4. **Reinicia Home Assistant**.

---

## ⚙️ Configuración

Añade las siguientes líneas a tu archivo `configuration.yaml`:

```yaml
sensor:
  - platform: casetero_603
```

---

## 📊 Visualización Avanzada en Lovelace

Puedes crear una tarjeta tipo **Markdown** avanzada en tu panel de Home Assistant para ver no solo el próximo autobús, sino también los tres siguientes de forma elegante:

```yaml
type: markdown
title: "🚍 Horarios Casetero 603"
content: >
  ### Próxima salida programada:
  # 🕒 **{{ states('sensor.casetero_603_zaragoza') }}**
  
  ---
  
  **Siguientes autobuses hoy:**
  {% set proximos = state_attr('sensor.casetero_603_zaragoza', 'siguiente_bus') %}
  {% if proximos and proximos | length > 1 %}
    - {{ proximos[1] }}
    {% if proximos | length > 2 %}- {{ proximos[2] }}{% endif %}
  {% else %}
    No hay más autobuses programados para hoy.
  {% endif %}
  
  *Última consulta: {{ state_attr('sensor.casetero_603_zaragoza', 'actualizado_en') | as_timestamp | timestamp_custom('%H:%M') }}*
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si detectas un fallo en el parseo de horarios debido a un cambio en la web del CTAAZ, por favor abre un **Issue** o envía un **Pull Request**.
