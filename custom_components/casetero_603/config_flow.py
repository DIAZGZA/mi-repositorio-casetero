"""Flujo de configuración para el Casetero 603."""
import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv

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
                # El título que se mostrará en la lista de integraciones instaladas
                return self.async_create_entry(
                    title=f"Casetero - Parada {stop_id}", 
                    data={CONF_STOP_ID: stop_id}
                )

        # Formulario que verá el usuario
        data_schema = vol.Schema({
            vol.Required(CONF_STOP_ID): cv.string,
        })

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema, 
            errors=errors
        )
