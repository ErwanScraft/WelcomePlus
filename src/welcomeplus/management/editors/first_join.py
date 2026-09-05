import json

from endstone.form import ModalForm, TextInput, Toggle


class FirstJoinEditor:
    def __init__(self, manager) -> None:
        self.manager = manager
        self.config = manager.config

    def open(self, player) -> None:
        feature = self.config.get_feature("first_join")

        form = ModalForm(title="§aFirst Join")

        form.add_control(
            Toggle(
                "Enable first join message",
                default_value=feature["enabled"],
            )
        )

        form.add_control(
            TextInput(
                "Message",
                "Example: §eWelcome {player}!",
                default_value=feature["message"],
            )
        )

        form.on_submit = self._save
        form.on_close = self.manager.open

        player.send_form(form)

    def _save(self, player, result) -> None:
        try:
            values = self._parse_result(result)

            if len(values) != 2:
                raise ValueError("Invalid form response.")

            enabled = bool(values[0])
            message = self._require_text(
                values[1],
                "Message",
            )

            self.config.update_feature(
                "first_join",
                {
                    "enabled": enabled,
                    "message": message,
                },
            )

            player.send_message(
                "§aFirst join configuration saved."
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