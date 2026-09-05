import yaml

from endstone.command import Command, CommandSender
from endstone.event import PlayerJoinEvent, PlayerQuitEvent, event_handler
from endstone.plugin import Plugin

from .commands.welcomeplus import WelcomePlusCommand


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
        self._load_players()
    
        self._command = WelcomePlusCommand(self)
        self.register_events(self)
    
        self.logger.info("WelcomePlus enabled!")

    def _load_config(self) -> None:
        config_path = self.data_folder / "config.yml"
    
        with config_path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    
        if not isinstance(config, dict):
            raise ValueError("config.yml must contain a YAML mapping.")
    
        self._config = config
    
    def _load_players(self) -> None:
        players_path = self.data_folder / "players.yml"
    
        if not players_path.exists():
            self._players = set()
            return
    
        with players_path.open("r", encoding="utf-8") as file:
            players = yaml.safe_load(file) or []
    
        if not isinstance(players, list):
            raise ValueError("players.yml must contain a YAML list.")
    
        self._players = {str(player) for player in players}
    
    def _save_players(self) -> None:
        players_path = self.data_folder / "players.yml"
    
        with players_path.open("w", encoding="utf-8") as file:
            yaml.safe_dump(
                sorted(self._players),
                file,
                allow_unicode=True,
                default_flow_style=False,
            )
    
    def _is_first_join(self, player) -> bool:
        player_id = str(player.unique_id)
    
        if player_id in self._players:
            return False
    
        self._players.add(player_id)
        self._save_players()
    
        return True
    
    def _get_feature_config(self, feature: str) -> dict:
        config = self._config.get(feature, {})
    
        if not isinstance(config, dict):
            raise ValueError(f"'{feature}' must be a YAML mapping.")
    
        return config
    
    def _replace_placeholders(self, text: str, player_name: str) -> str:
        return text.replace("{player}", player_name)

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        player = event.player
        player_name = player.name
        first_join = self._is_first_join(player)
    
        welcome = self._get_feature_config("welcome")

        if welcome["enabled"]:
            player.send_title(
                self._replace_placeholders(welcome["title"], player_name),
                self._replace_placeholders(welcome["subtitle"], player_name),
                welcome["fade_in"],
                welcome["stay"],
                welcome["fade_out"],
            )
        
        sound = self._get_feature_config("sound")

        if sound["enabled"]:
            player.play_sound(
                player.location,
                sound["name"],
                sound["volume"],
                sound["pitch"],
            )
            
        first_join_config = self._get_feature_config("first_join")

        if first_join and first_join_config["enabled"]:
            player.server.broadcast_message(
                self._replace_placeholders(
                    first_join_config["message"],
                    player_name,
                )
            )
    
        join_message = self._get_feature_config("join_message")
    
        if join_message["enabled"]:
            player.server.broadcast_message(
                self._replace_placeholders(
                    join_message["message"],
                    player_name,
                )
            )
    
    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent) -> None:
        player = event.player
        leave_message = self._get_feature_config("leave_message")
    
        if leave_message["enabled"]:
            player.server.broadcast_message(
                self._replace_placeholders(
                    leave_message["message"],
                    player.name,
                )
            )
    
    def on_command(
        self,
        sender: CommandSender,
        command: Command,
        args: list[str],
    ) -> bool:
        return self._command.on_command(sender, command, args)