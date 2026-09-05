import yaml

from endstone.event import PlayerJoinEvent, PlayerQuitEvent, event_handler
from .commands.welcomeplus import WelcomePlusCommand
from endstone.command import Command, CommandSender
from endstone.plugin import Plugin


class WelcomePlusPlugin(Plugin):
    api_version = "0.11"
    authors = ["ErwanScraft"]
    commands = {
        "welcomeplus": {
            "description": "Manage WelcomePlus.",
            "usages": [
                "/welcomeplus help",
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
        }
    }

    def on_enable(self) -> None:
        self.save_resources("config.yml")
        self._load_config()
        self._command = WelcomePlusCommand(self)
        self.register_events(self)
        self.logger.info("Welcome Plus enabled!")

    def _load_config(self) -> None:
        config_path = self.data_folder / "config.yml"
    
        with config_path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file) or {}
    
        if not isinstance(config, dict):
            raise ValueError("config.yml must contain a YAML mapping.")
    
        self._config = config
    
    def _replace_placeholders(self, text: str, player_name: str) -> str:
        return text.replace("{player}", player_name)

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        player_name = event.player.name
        welcome = self._config.get("welcome", {})
    
        event.player.send_title(
            self._replace_placeholders(
                welcome.get("title", "§6Welcome, {player}!"),
                player_name,
            ),
            self._replace_placeholders(
                welcome.get("subtitle", "§fEnjoy your time on our server!"),
                player_name,
            ),
            welcome.get("fade_in", 10),
            welcome.get("stay", 70),
            welcome.get("fade_out", 20),
        )
    
        join_message = self._config.get("join_message", {})
    
        if join_message.get("enabled", True):
            event.player.server.broadcast_message(
                self._replace_placeholders(
                    join_message.get("message", "§a+ §f{player} joined the server."),
                    player_name,
                )
            )
    
    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent) -> None:
        leave_message = self._config.get("leave_message", {})
    
        if leave_message.get("enabled", True):
            event.player.server.broadcast_message(
                self._replace_placeholders(
                    leave_message.get("message", "§c- §f{player} left the server."),
                    event.player.name,
                )
            )
    
    def on_command(
        self,
        sender: CommandSender,
        command: Command,
        args: list[str],
    ) -> bool:
        return self._command.on_command(sender, command, args)