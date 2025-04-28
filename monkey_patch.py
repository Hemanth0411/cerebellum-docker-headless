# monkey_patch.py
from cerebellum import BrowserActionType
from state_tracker import StateTracker
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from cerebellum.utils import parse_xdotool

state_tracker = StateTracker()

def custom_take_action(self, next_action, current_state):
    print(f"DEBUG: Next action: {next_action.action}, coordinate: {getattr(next_action, 'coordinate', None)}, text: {getattr(next_action, 'text', None)}")
    try:
        if next_action.action in (BrowserActionType.SCREENSHOT, BrowserActionType.CURSOR_POSITION):
            pass
        elif next_action.action == BrowserActionType.MOUSE_MOVE:
            if not next_action.coordinate:
                raise ValueError("Coordinate is required for mouse_move action")
            if not state_tracker.update_state("mouse_move", coordinate=(next_action.coordinate.x, next_action.coordinate.y)):
                print("Redundant mouse move detected. Skipping...")
                return
        elif next_action.action == BrowserActionType.TYPE:
            if not next_action.text:
                raise ValueError("Text is required for type action")
            if not state_tracker.update_state("type", text=next_action.text):
                print("Redundant text input detected or not allowed. Skipping...")
                return
        elif next_action.action == BrowserActionType.LEFT_CLICK:
            if not state_tracker.update_state("left_click"):
                print("Redundant left click detected. Skipping...")
                return

        # Rest of the original take_action logic
        action_builder = ActionBuilder(self.driver)

        if next_action.action == BrowserActionType.KEY:
            if not next_action.text:
                raise ValueError("Text is required for key action")
            key_strokes = parse_xdotool(next_action.text)
            for modifier in key_strokes.modifiers:
                action_builder.key_action.key_down(modifier)
            for key in key_strokes.keys:
                action_builder.key_action.send_keys(key)
            for modifier in reversed(key_strokes.modifiers):
                action_builder.key_action.key_up(modifier)
            action_builder.perform()
        elif next_action.action == BrowserActionType.TYPE:
            action_builder.key_action.send_keys(next_action.text)
            action_builder.perform()
        elif next_action.action == BrowserActionType.MOUSE_MOVE:
            action_builder.pointer_action.move_to_location(next_action.coordinate.x, next_action.coordinate.y)
            action_builder.perform()
        elif next_action.action == BrowserActionType.LEFT_CLICK:
            action_builder.pointer_action.click()
            action_builder.perform()
        # Add other action types as needed
    except Exception as e:
        print(f"Error in custom_take_action: {e}")