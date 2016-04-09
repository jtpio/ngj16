import os
import json
import sys

DIRNAME = os.path.dirname(__file__)

def send_message(text):
    return {
        'text': 'Hello there!',
        'options': ['To the left', 'To the right']
    }


class StateMachine:
    def __init__(self, json_filename, initial_state_name):
        json_file = open(json_filename, 'r')
        states_json = json.load(json_file)
        self.states = states_json["states"]
        self.triggers = states_json["triggers"]
        if self._is_valid_state(initial_state_name):
            print
            self.current_state_name = initial_state_name
        else:
            sys.exit(-1)

    def transtion_to_state_with_text(self, display_text):
        triggers = self.get_available_triggers_names()
        required_trigger = ""
        for trigger in triggers:
            if (self.get_display_text(trigger) == display_text):
                required_trigger = trigger

        if (required_trigger):
            self.transtion_to_state(required_trigger)

    def get_metadata(self, trigger_name):
        trigger = self._get_trigger(trigger_name)
        return trigger['metadata']

    def get_available_display_texts(self):
        triggers = self.get_available_triggers_names()
        texts = []
        for trigger in triggers:
            texts.append(self.get_display_text(trigger))
        return texts

    def get_display_text(self, trigger_name):
        trigger = self._get_trigger(trigger_name)
        return trigger['display_text']

    def get_available_triggers_names(self):
        current_state = self._get_current_state()
        return current_state['triggers']

    def transtion_to_state(self, trigger_name):
        assert(self._is_valid_trigger(trigger_name))
        trigger_source = self._get_source(trigger_name)
        assert(trigger_source == self.current_state_name)
        trigger_destination = self._get_destination(trigger_name)
        assert(self._is_valid_state(trigger_destination))
        print("Moving from " + self.current_state_name +
              " to " + trigger_destination)
        self.current_state_name = trigger_destination

    def _is_valid_state(self, state_name):
        return next(state for state in self.states
                    if state['name'] == state_name) is not None

    def _is_valid_trigger(self, trigger_name):
        return next(trigger for trigger in self.triggers
                    if trigger['name'] == trigger_name) is not None

    def _get_current_state(self):
        return next(state for state in self.states
                    if state['name'] == self.current_state_name)

    def _get_trigger(self, trigger_name):
        assert(self._is_valid_trigger(trigger_name))
        return next(trigger for trigger in self.triggers
                    if trigger['name'] == trigger_name)

    def _get_source(self, trigger_name):
        trigger = self._get_trigger(trigger_name)
        return trigger['source']

    def _get_destination(self, trigger_name):
        trigger = self._get_trigger(trigger_name)
        return trigger['destination']

if __name__ == '__main__':
    json_filename = sys.argv[1]
    state_manager = StateMachine(json_filename, 'Valley')
    # print(state_manager.get_current_state())
    available_triggers = state_manager.get_available_triggers_names()
    # print(state_manager.get_metadata(available_triggers[0]))
    # print(state_manager.get_display_text(available_triggers[1]))
    # print(state_manager._get_source(available_triggers[0]))
    # print(state_manager._get_destination(available_triggers[0]))
    # state_manager.transtion_to_state(available_triggers[0])
