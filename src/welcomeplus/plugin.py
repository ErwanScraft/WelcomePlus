from endstone.plugin import Plugin
from endstone.event import event_handler, PlayerJoinEvent


class WelcomePlusPlugin(Plugin):
    api_version = "0.11"

    def on_enable(self) -> None:
        self.save_default_config()
        self.reload_config()
        self.register_events(self)
        self.logger.info("Welcome Plus enabled!")

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        config = self.config
    
        event.player.send_title(
            config.get("title", "§6Selamat Datang!"),
            config.get("subtitle", "§fNikmati permainan di server kami"),
            config.get("fade_in", 10),
            config.get("stay", 70),
            config.get("fade_out", 20),
        )