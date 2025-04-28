# state_tracker.py
class StateTracker:
    def __init__(self):
        self.last_mouse_position = None
        self.last_search_query = None
        self.last_action = None
        self.action_count = {}
        self.max_attempts = 3
        self.must_type_next = False  # <-- NEW

    def update_state(self, action, coordinate=None, text=None):
        if action not in self.action_count:
            self.action_count[action] = 0
        self.action_count[action] += 1
        if self.action_count[action] > self.max_attempts:
            print(f"Warning: Action '{action}' has been attempted too many times")
            return False

        if action == "mouse_move":
            if coordinate and (not self.last_mouse_position or 
                abs(coordinate[0] - self.last_mouse_position[0]) > 5 or 
                abs(coordinate[1] - self.last_mouse_position[1]) > 5):
                self.last_mouse_position = coordinate
                return True
            return False
        elif action == "left_click":
            self.last_action = "left_click"
            self.must_type_next = True  # <-- Set flag after click
            return True
        elif action == "type":
            if self.must_type_next:
                self.must_type_next = False  # <-- Clear flag after typing
                return True
            print("Type action not allowed: must type immediately after click on input field.")
            return False
        return True