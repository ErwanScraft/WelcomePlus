from endstone.command import Command, CommandSender


class WelcomePlusCommand:
    def __init__(self, plugin) -> None:
        self.plugin = plugin

    def on_command(
        self,
        sender: CommandSender,
        command: Command,
        args: list[str],
    ) -> bool:
        if command.name != "welcomeplus":
            return False

        if not args or args == ["help"]:
            self._send_help(sender)
            return True

        if args == ["manage"]:
            return self._manage(sender)

        if args == ["reload"]:
            return self._reload(sender)

        sender.send_message("§cUnknown command.")
        sender.send_message("§eUsage: /welcomeplus help")
        return True

    @staticmethod
    def _send_help(sender: CommandSender) -> None:
        sender.send_message("§6§lWelcomePlus Commands")
        sender.send_message("§e/welcomeplus help §7- Show this help.")
        sender.send_message(
            "§e/welcomeplus manage §7- Open the configuration manager."
        )
        sender.send_message(
            "§e/welcomeplus reload §7- Reload configuration."
        )

    def _manage(self, sender: CommandSender) -> bool:
        # The form API requires a player as its target.
        if not hasattr(sender, "send_form"):
            sender.send_message(
                "§cThis command can only be used by a player."
            )
            return True

        if not sender.has_permission("welcomeplus.manage"):
            sender.send_message(
                "§cYou do not have permission to manage WelcomePlus."
            )
            return True

        self.plugin._manager.open(sender)
        return True

    def _reload(self, sender: CommandSender) -> bool:
        try:
            self.plugin._config_manager.load()
        except Exception as error:
            sender.send_message(
                f"§cFailed to reload WelcomePlus configuration: {error}"
            )
            self.plugin.logger.error(
                f"Failed to reload config.yml: {error}"
            )
            return False

        sender.send_message(
            "§aWelcomePlus configuration reloaded."
        )
        return True