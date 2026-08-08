"""Flujo de configuración para el Casetero 603."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_STOP_ID

class Casetero603ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gestión del flujo de configuración por interfaz gráfica."""
    
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Primer paso al añadir la integración manualmente."""
        errors = {}
        
        if user_input is not None:
            stop_id = user_input[CONF_STOP_ID].strip()
            
            if not stop_id.isdigit():
                errors["base"] = "invalid_stop_id"
            else:
                # Evita que el usuario configure la misma parada dos veces
                await self.async_set_unique_id(f"casetero_603_{stop_id}")
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"Casetero - Parada {stop_id}", 
                    data={CONF_STOP_ID: stop_id}
                )

        # Esquema limpio y directo
        data_schema = vol.Schema({
            vol.Required(CONF_STOP_ID): str,
        })

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema, 
            errors=errors
        )

