from StateMachine import StateMachine


class StateMachineManager:
    def __init__(self, json_filename, initial_state_name):
        self.state_machine = StateMachine(json_filename, initial_state_name)

    def send_message(self, message):
        if (self.state_machine.is_valid_text(message)):
            metadata = self.state_machine.get_metadata_for_text(message)
            self.state_machine.transtion_to_state_with_text(message)
            return {
                'metadata': metadata,
                'triggers': self.state_machine.get_available_display_texts()
            }
        else:
            print("Invalid text message")

    def get_current_display_texts(self):
        return self.state_machine.get_available_display_texts()
