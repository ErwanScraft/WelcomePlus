class MotdConfig:
    def __init__(self, plugin) -> None:
        self.path = plugin.data_folder / "motd.yml"
        self.text = ""

    def load(self) -> None:
        self.text = self.path.read_text(
            encoding="utf-8"
        ).strip()

    def get(self) -> str:
        return self.text