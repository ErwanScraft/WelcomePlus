from endstone.event import PlayerJoinEvent, PlayerQuitEvent, event_handler


class PlayerEvents:
    def __init__(
        self,
        config,
        player_data,
        webhook,
    ) -> None:
        self.config = config
        self.player_data = player_data
        self.webhook = webhook

    @staticmethod
    def _replace_placeholders(
        text: str,
        player_name: str,
    ) -> str:
        return text.replace("{player}", player_name)

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        player = event.player
        player_name = player.name

        self._handle_welcome(player, player_name)
        self._handle_first_join(player, player_name)
        self._handle_join_sound(player)
        self._handle_join_message(player, player_name)
        
        self.webhook.dispatch(
            "player.join",
            {
                "player": {
                    "name": player.name,
                    "uuid": str(player.unique_id),
                },
            },
        )

    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent) -> None:
        player = event.player
        leave_message = self.config.get_feature("leave_message")

        if not leave_message["enabled"]:
            return

        player.server.broadcast_message(
            self._replace_placeholders(
                leave_message["message"],
                player.name,
            )
        )

    def _handle_welcome(self, player, player_name: str) -> None:
        welcome = self.config.get_feature("welcome")

        if not welcome["enabled"]:
            return

        player.send_title(
            self._replace_placeholders(
                welcome["title"],
                player_name,
            ),
            self._replace_placeholders(
                welcome["subtitle"],
                player_name,
            ),
            welcome["fade_in"],
            welcome["stay"],
            welcome["fade_out"],
        )

    def _handle_first_join(self, player, player_name: str) -> None:
        first_join = self.config.get_feature("first_join")

        if not first_join["enabled"]:
            return

        if not self.player_data.is_first_join(player):
            return

        player.server.broadcast_message(
            self._replace_placeholders(
                first_join["message"],
                player_name,
            )
        )

    def _handle_join_sound(self, player) -> None:
        sound = self.config.get_feature("sound")

        if not sound["enabled"]:
            return

        player.play_sound(
            player.location,
            sound["name"],
            sound["volume"],
            sound["pitch"],
        )

    def _handle_join_message(self, player, player_name: str) -> None:
        join_message = self.config.get_feature("join_message")

        if not join_message["enabled"]:
            return

        player.server.broadcast_message(
            self._replace_placeholders(
                join_message["message"],
                player_name,
            )
        )