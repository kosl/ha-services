import logging

from cli_base.cli_tools.verbosity import setup_logging
from cli_base.systemd.api import ServiceControl
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa

from ha_services.cli_app import app
from ha_services.cli_app.settings import get_user_settings
from ha_services.example import DemoSettings, SystemdServiceInfo


logger = logging.getLogger(__name__)


@app.command
def systemd_debug(verbosity: TyroVerbosityArgType):
    """
    Print Systemd service template + context + rendered file content.
    """
    setup_logging(verbosity=verbosity)
    user_settings: DemoSettings = get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).debug_systemd_config()


@app.command
def systemd_setup(verbosity: TyroVerbosityArgType):
    """
    Write Systemd service file, enable it and (re-)start the service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    user_settings: DemoSettings = get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).setup_and_restart_systemd_service()


@app.command
def systemd_remove(verbosity: TyroVerbosityArgType):
    """
    Write Systemd service file, enable it and (re-)start the service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    user_settings: DemoSettings = get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).remove_systemd_service()


@app.command
def systemd_status(verbosity: TyroVerbosityArgType):
    """
    Display status of systemd service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    user_settings: DemoSettings = get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).status()


@app.command
def systemd_stop(verbosity: TyroVerbosityArgType):
    """
    Stops the systemd service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    user_settings: DemoSettings = get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).stop()
