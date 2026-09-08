from endstone.command import Command, CommandSender
from endstone.plugin import Plugin

from .commands.welcomeplus import WelcomePlusCommand
from .config import WelcomePlusConfig
from .motd import MotdConfig
from .events import PlayerEvents
from .management import WelcomePlusManager
from .player_data import PlayerData


class WelcomePlusPlugin(Plugin):
    api_version = "0.11"
    authors = ["ErwanScraft"]

    commands = {
        "welcomeplus": {
            "description": "Manage WelcomePlus.",
            "usages": [
                "/welcomeplus help",
                "/welcomeplus manage",
                "/welcomeplus reload",
            ],
            "aliases": ["wp"],
            "permissions": ["welcomeplus.command"],
        }
    }

    permissions = {
        "welcomeplus.command": {
            "description": "Allows using WelcomePlus commands.",
            "default": "op",
        },
        "welcomeplus.manage": {
            "description": (
                "Allows managing WelcomePlus configuration."
            ),
            "default": "op",
        },
    }

    def on_enable(self) -> None:
        self.save_resources("config.yml")
        self.save_resources("motd.yml")
        
        self._config_manager = WelcomePlusConfig(self)
        self._config_manager.load()
        
        self._motd_config = MotdConfig(self)
        self._motd_config.load()
    
        self._player_data = PlayerData(self)
        self._player_data.load()
    
        self._manager = WelcomePlusManager(self)
        self._command = WelcomePlusCommand(self)
    
        self.register_events(
            PlayerEvents(
                self._config_manager,
                self._player_data,
                self._motd_config,
            )
        )
    
        self.logger.info("WelcomePlus enabled!")

    def on_command(
        self,
        sender: CommandSender,
        command: Command,
        args: list[str],
    ) -> bool:
        return self._command.on_command(
            sender,
            command,
            args,
        )