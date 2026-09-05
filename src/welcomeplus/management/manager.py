from endstone.form import ActionForm

from .editors.first_join import FirstJoinEditor
from .editors.join_message import JoinMessageEditor
from .editors.leave_message import LeaveMessageEditor
from .editors.sound import SoundEditor
from .editors.welcome import WelcomeEditor


class WelcomePlusManager:
    def __init__(self, plugin) -> None:
        self.plugin = plugin
        self.config = plugin._config_manager

        self.welcome_editor = WelcomeEditor(self)
        self.first_join_editor = FirstJoinEditor(self)
        self.join_message_editor = JoinMessageEditor(self)
        self.leave_message_editor = LeaveMessageEditor(self)
        self.sound_editor = SoundEditor(self)

    def open(self, player) -> None:
        form = ActionForm(
            title="§6§lWelcomePlus Manager",
            content=(
                "§7Manage your WelcomePlus configuration.\n\n"
                "§fSelect a feature to edit."
            ),
        )

        form.add_button(
            "§eWelcome Title",
            on_click=self.welcome_editor.open,
        )

        form.add_button(
            "§aFirst Join",
            on_click=self.first_join_editor.open,
        )

        form.add_button(
            "§bJoin Message",
            on_click=self.join_message_editor.open,
        )

        form.add_button(
            "§cLeave Message",
            on_click=self.leave_message_editor.open,
        )

        form.add_button(
            "§dJoin Sound",
            on_click=self.sound_editor.open,
        )

        player.send_form(form)