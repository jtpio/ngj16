from StateMachine import StateMachine


class StateMachineManager:
    def __init__(self, json_filename, initial_state_name):
        self.state_manager = StateMachine(json_filename, initial_state_name)

    def send_message(self, message):
        self.state_manager.transtion_to_state_with_text(message)
        return {
            'metadata': self.state_manager.get_metadata_for_text(message),
            'triggers': self.state_manager.get_available_display_texts()
        }
