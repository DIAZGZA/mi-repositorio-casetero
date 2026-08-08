"""Plataforma de sensores para el Casetero 603."""
from datetime import datetime
import logging
import requests

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_STOP_ID

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, 
    config_entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback
) -> None:
    """Configura el sensor basándose en la entrada de configuración gráfica."""
    stop_id = config_entry.data[CONF_STOP_ID]
    async_add_entities([CaseteroParadaSensor(hass, stop_id)], True)

class CaseteroParadaSensor(SensorEntity):
    """Representación del tiempo de espera en una parada del Casetero."""

    def __init__(self, hass, stop_id):
        self.hass = hass
        self._stop_id = stop_id
        self._attr_native_value = "Desconocido"
        self._attr_extra_state_attributes = {}
        self._attr_name = f"Casetero Parada {stop_id}"
        self._attr_unique_id = f"casetero_603_{stop_id}"
        self._attr_icon = "mdi:bus-clock"

    def _fetch_data(self):
        """Llamada síncrona segura ejecutada fuera del hilo principal."""
        url = f"https://zaragoza.es{self._stop_id}"
        headers = {"Accept": "application/json", "User-Agent": "HomeAssistant-Casetero"}
        return requests.get(url, headers=headers, timeout=10)

    async def async_update(self) -> None:
        """Consulta los minutos restantes de forma asíncrona."""
        try:
            # Ejecuta la petición HTTP en un hilo secundario para evitar bloquear Home Assistant
            response = await self.hass.async_add_executor_job(self._fetch_data)
            
            if response.status_code == 200:
                data = response.json()
                destinos = data.get("destinos", [])
                
                buses_filtrados = [
                    d for d in destinos 
                    if "603" in d.get("linea", "") or "613" in d.get("linea", "")
                ]

                if buses_filtrados:
                    buses_filtrados.sort(key=lambda x: int(x.get("minutos", 999)))
                    primer_bus = buses_filtrados[0]
                    
                    self._attr_native_value = f"{primer_bus.get('minutos')} min"
                    self._attr_extra_state_attributes = {
                        "parada_solicitada": self._stop_id,
                        "destino_inmediato": primer_bus.get("destino"),
                        "proximas_llegadas": [
                            f"Línea {b.get('linea')} dir. {b.get('destino')}: {b.get('minutos')} min" 
                            for b in buses_filtrados
                        ],
                        "actualizado_en": datetime.now().isoformat()
                    }
                else:
                    self._attr_native_value = "Sin autobuses"
                    self._attr_extra_state_attributes = {
                        "parada_solicitada": self._stop_id,
                        "info": "No se aproximan autobuses de la línea 603/613 en las próximas horas."
                    }
            else:
                _LOGGER.error("La API de Zaragoza devolvió un código de error: %s", response.status_code)
                self._attr_native_value = "Error API"

        except Exception as e:
            _LOGGER.error("Error al actualizar la parada %s: %s", self._stop_id, e)
            self._attr_native_value = "Error de Red"
