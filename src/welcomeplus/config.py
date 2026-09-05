import yaml


class WelcomePlusConfig:
    def __init__(self, plugin) -> None:
        self.path = plugin.data_folder / "config.yml"
        self.data: dict = {}

    def load(self) -> None:
        with self.path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        if not isinstance(config, dict):
            raise ValueError("config.yml must contain a YAML mapping.")

        self.data = config

    def get_feature(self, name: str) -> dict:
        feature = self.data.get(name)

        if not isinstance(feature, dict):
            raise ValueError(f"'{name}' must be a YAML mapping.")

        return feature