"""template conftest."""
import json

import pytest

from homeassistant.setup import async_setup_component

from tests.common import assert_setup_component, async_mock_service


@pytest.fixture
def calls(hass):
    """Track calls to a mock service."""
    return async_mock_service(hass, "test", "automation")


@pytest.fixture
def config_addon():
    """Add entra configuration items."""
    return None


@pytest.fixture
async def start_ha(hass, count, domain, config_addon, config, caplog):
    """Do setup of integration."""
    if config_addon:
        for key, value in config_addon.items():
            config = config.replace(key, value)
        config = json.loads(config)
    with assert_setup_component(count, domain):
        assert await async_setup_component(
            hass,
            domain,
            config,
        )

    await hass.async_block_till_done()
    await hass.async_start()
    await hass.async_block_till_done()


@pytest.fixture
async def caplog_setup_text(caplog):
    """Return setup log of integration."""
    yield caplog.text
