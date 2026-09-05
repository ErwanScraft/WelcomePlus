import yaml

from endstone.event import PlayerJoinEvent, event_handler
from endstone.plugin import Plugin


class WelcomePlusPlugin(Plugin):
    api_version = "0.11"

    def on_enable(self) -> None:
        self.save_resources("config.yml")
        self._load_config()
        self.register_events(self)
        self.logger.info("Welcome Plus enabled!")

    def _load_config(self) -> None:
        config_path = self.data_folder / "config.yml"

        with config_path.open("r", encoding="utf-8") as file:
            self._config = yaml.safe_load(file) or {}

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        event.player.send_title(
            self._config.get("title", "§6Selamat Datang!"),
            self._config.get("subtitle", "§fNikmati permainan di server kami"),
            self._config.get("fade_in", 10),
            self._config.get("stay", 70),
            self._config.get("fade_out", 20),
        )