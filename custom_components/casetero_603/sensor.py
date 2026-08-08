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
    async_add_entities([CaseteroParadaSensor(stop_id)], True)

class CaseteroParadaSensor(SensorEntity):
    """Representación del tiempo de espera en una parada del Casetero."""

    def __init__(self, stop_id):
        self._stop_id = stop_id
        self._state = "Desconocido"
        self._attr_extra_state_attributes = {}
        self._attr_name = f"Casetero Parada {stop_id}"
        self._attr_unique_id = f"casetero_603_{stop_id}"
        self._attr_icon = "mdi:bus-clock"

    @property
    def state(self):
        return self._state

    def update(self):
        """Consulta los minutos restantes para la parada configurada."""
        try:
            # Endpoint oficial del Ayuntamiento / CTAAZ para postes urbanos e interurbanos
            url = f"https://zaragoza.es{self._stop_id}"
            headers = {"Accept": "application/json", "User-Agent": "HomeAssistant-Casetero"}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                destinos = data.get("destinos", [])
                
                # Filtramos las estimaciones que correspondan a la línea 603 (Casetero habitual) o 613
                buses_filtrados = [
                    d for d in destinos 
                    if "603" in d.get("linea", "") or "613" in d.get("linea", "")
                ]

                if buses_filtrados:
                    # Ordenamos por tiempo de llegada (minutos)
                    buses_filtrados.sort(key=lambda x: int(x.get("minutos", 999)))
                    primer_bus = buses_filtrados[0]
                    
                    # El estado principal pasa a ser los minutos que le faltan al primer bus
                    self._state = f"{primer_bus.get('minutos')} min"
                    
                    # Almacenamos el resto de buses en los atributos
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
                    self._state = "Sin autobuses"
                    self._attr_extra_state_attributes = {
                        "parada_solicitada": self._stop_id,
                        "info": "No se aproximan autobuses de la línea 603/613 en las próximas horas."
                    }
            else:
                _LOGGER.error("La API de Zaragoza devolvió un código de error: %s", response.status_code)
                self._state = "Error API"

        except Exception as e:
            _LOGGER.error("Error al actualizar la parada %s: %s", self._stop_id, e)
            self._state = "Error de Red"
