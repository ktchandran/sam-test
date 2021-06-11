"""
AppConfig Helper class
"""
import json
import socket
from typing import Any, Dict, Optional, Union

import boto3


class AppConfigHelper:
    """

    """
    def __init__(
            self,
            appconfig_application: str,
            appconfig_environment: str,
            appconfig_profile: str,
            max_config_age: int,
            configuration_version: str,
            session: Optional[boto3.Session] = None,
            client_id: Optional[str] = None,
    ) -> None:

        if isinstance(session, boto3.Session):
            self._client = session.client("appconfig")
        else:
            self._client = boto3.client("appconfig")
        self._appconfig_profile = appconfig_profile
        self._appconfig_environment = appconfig_environment
        self._appconfig_application = appconfig_application
        self._configuration_version = configuration_version
        if max_config_age < 15:
            raise ValueError("max_config_age must be at least 15 seconds")
        self._max_config_age = max_config_age
        if client_id is None:
            self._client_id = socket.gethostname()
        else:
            self._client_id = client_id
        self._config = None  # type: Union[None, Dict[Any, Any], str, bytes]
        self.update_config()

    @property
    def appconfig_profile(self) -> str:
        """The profile in use."""
        return self._appconfig_profile

    @property
    def appconfig_environment(self) -> str:
        """The environment in use."""
        return self._appconfig_environment

    @property
    def appconfig_application(self) -> str:
        """The application in use."""
        return self._appconfig_application

    @property
    def config_version(self) -> str:
        """The configuration version last received."""
        return self._configuration_version

    @property
    def config(self) -> Union[None, Dict[Any, Any], str, bytes]:
        return self._config

    def update_config(self) -> None:
        response = self._client.get_configuration(
            Application=self._appconfig_application,
            Environment=self._appconfig_environment,
            Configuration=self._appconfig_profile,
            ClientId=self._client_id,
            ClientConfigurationVersion=self._configuration_version,
        )
        content = response["Content"].read()  # type: bytes
        try:
            self._config = json.loads(content.decode("utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(error.msg) from error