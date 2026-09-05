import json

from endstone.form import ModalForm, Slider, TextInput, Toggle


class SoundEditor:
    def __init__(self, manager) -> None:
        self.manager = manager
        self.config = manager.config

    def open(self, player) -> None:
        feature = self.config.get_feature("sound")

        form = ModalForm(title="§dJoin Sound")

        form.add_control(
            Toggle(
                "Enable join sound",
                default_value=feature["enabled"],
            )
        )

        form.add_control(
            TextInput(
                "Sound",
                "Example: random.levelup",
                default_value=feature["name"],
            )
        )

        form.add_control(
            Slider(
                "Volume",
                0,
                2,
                0.1,
                default_value=feature["volume"],
            )
        )

        form.add_control(
            Slider(
                "Pitch",
                0,
                2,
                0.1,
                default_value=feature["pitch"],
            )
        )

        form.on_submit = self._save
        form.on_close = self.manager.open

        player.send_form(form)

    def _save(self, player, result) -> None:
        try:
            values = self._parse_result(result)

            if len(values) != 4:
                raise ValueError("Invalid form response.")

            enabled = bool(values[0])
            name = self._require_text(
                values[1],
                "Sound",
            )

            volume = float(values[2])
            pitch = float(values[3])

            if not 0 <= volume <= 2:
                raise ValueError(
                    "Volume must be between 0 and 2."
                )

            if not 0 <= pitch <= 2:
                raise ValueError(
                    "Pitch must be between 0 and 2."
                )

            self.config.update_feature(
                "sound",
                {
                    "enabled": enabled,
                    "name": name,
                    "volume": volume,
                    "pitch": pitch,
                },
            )

            player.send_message(
                "§aJoin sound configuration saved."
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
    def _require_text(value, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

        return value