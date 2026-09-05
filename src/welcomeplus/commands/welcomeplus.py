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
            sender.send_message("§6§lWelcomePlus Commands")
            sender.send_message("§e/welcomeplus help §7- Show this help.")
            sender.send_message("§e/welcomeplus reload §7- Reload configuration.")
            return True

        if args == ["reload"]:
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

            sender.send_message("§aWelcomePlus configuration reloaded.")
            return True

        sender.send_message("§cUnknown command.")
        sender.send_message("§eUsage: /welcomeplus help")
        return True