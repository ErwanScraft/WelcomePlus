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
            title="WelcomePlus",
            content="Select a feature to configure.",
        )
    
        form.add_button(
            "Welcome",
            on_click=self.welcome_editor.open,
        )
    
        form.add_button(
            "First Join",
            on_click=self.first_join_editor.open,
        )
    
        form.add_button(
            "Join Message",
            on_click=self.join_message_editor.open,
        )
    
        form.add_button(
            "Leave Message",
            on_click=self.leave_message_editor.open,
        )
    
        form.add_button(
            "Join Sound",
            on_click=self.sound_editor.open,
        )
    
        player.send_form(form)