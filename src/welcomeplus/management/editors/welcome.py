import json

from endstone.form import ModalForm, Slider, TextInput, Toggle


class WelcomeEditor:
    def __init__(self, manager) -> None:
        self.manager = manager
        self.config = manager.config

    def open(self, player) -> None:
        feature = self.config.get_feature("welcome")

        form = ModalForm(title="§6Welcome Title")

        form.add_control(
            Toggle(
                "Enable welcome title",
                default_value=feature["enabled"],
            )
        )

        form.add_control(
            TextInput(
                "Title",
                "Example: §6Welcome, {player}!",
                default_value=feature["title"],
            )
        )

        form.add_control(
            TextInput(
                "Subtitle",
                "Example: §fEnjoy your time!",
                default_value=feature["subtitle"],
            )
        )

        form.add_control(
            Slider(
                "Fade In",
                0,
                100,
                1,
                default_value=feature["fade_in"],
            )
        )

        form.add_control(
            Slider(
                "Stay",
                0,
                200,
                1,
                default_value=feature["stay"],
            )
        )

        form.add_control(
            Slider(
                "Fade Out",
                0,
                100,
                1,
                default_value=feature["fade_out"],
            )
        )

        form.on_submit = self._save
        form.on_close = self.manager.open

        player.send_form(form)

    def _save(self, player, result) -> None:
        try:
            values = self._parse_result(result)

            self._validate_length(values, 6)

            enabled = bool(values[0])
            title = self._require_text(values[1], "Title")
            subtitle = self._require_text(values[2], "Subtitle")

            fade_in = int(values[3])
            stay = int(values[4])
            fade_out = int(values[5])

            if min(fade_in, stay, fade_out) < 0:
                raise ValueError(
                    "Duration values cannot be negative."
                )

            self.config.update_feature(
                "welcome",
                {
                    "enabled": enabled,
                    "title": title,
                    "subtitle": subtitle,
                    "fade_in": fade_in,
                    "stay": stay,
                    "fade_out": fade_out,
                },
            )

            player.send_message(
                "§aWelcome title configuration saved."
            )

        except Exception as error:
            player.send_message(
                f"§cFailed to save configuration: {error}"
            )

        self.manager.open(player)

    @staticmethod
    def _parse_result(result) -> list:
        if isinstance(result, list):
            return result

        if isinstance(result, str):
            data = json.loads(result)

            if isinstance(data, list):
                return data

        raise ValueError("Invalid form response.")

    @staticmethod
    def _validate_length(values: list, expected: int) -> None:
        if len(values) != expected:
            raise ValueError("Invalid form response.")

    @staticmethod
    def _require_text(value, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

        return value