from StateMachine import StateMachine


class StateMachineManager:
    def __init__(self, json_filename, initial_state_name):
        self.state_manager = StateMachine(json_filename, initial_state_name)

    def send_message(self, message):
        metadata = self.state_manager.get_metadata_for_text(message)
        self.state_manager.transtion_to_state_with_text(message)
        return {
            'metadata': metadata,
            'triggers': self.state_manager.get_available_display_texts()
        }

    def get_current_display_texts(self):
        return self.state_manager.get_available_display_texts()
