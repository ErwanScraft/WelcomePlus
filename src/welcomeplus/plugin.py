from endstone.plugin import Plugin
from endstone.event import event_handler, PlayerJoinEvent


class WelcomePlusPlugin(Plugin):
    api_version = "0.11"

    def on_enable(self) -> None:
        self.register_events(self)
        self.logger.info("Welcome Plus enabled!")

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        event.player.send_title(
            "§6Selamat Datang!",
            "§fNikmati permainan di server kami",
            10,
            70,
            20,
        )