from pynput import mouse, keyboard
import time, threading

# Global variables to store mouse positions and control tracking state
mouse_positions = []
tracking_active = True

def start_mouse_tracking():
    """Begin tracking mouse clicks and save positions when the left button is pressed."""
    mouse_positions = []  # Reset the list to start fresh
    tracking_active = True

    def on_click(x, y, button, pressed):
        """Handles mouse click events and saves positions on left-click."""
        if pressed and button == mouse.Button.left:
            mouse_positions.append((x, y))
            print(f"Position saved: {x, y}")
            # Limit the size of the saved positions list to the last 5 positions
            if len(mouse_positions) > 5:
                mouse_positions.pop(0)

    def on_key_press(key):
        """Stops tracking when the 'Esc' key is pressed."""
        nonlocal tracking_active
        if key == keyboard.Key.esc:
            print("\nEsc key pressed. Stopping tracking.")
            tracking_active = False
            return False  # Stop the keyboard listener

    def track_mouse():
        """Tracks mouse clicks and manages keyboard listener in a separate thread."""
        with mouse.Listener(on_click=on_click) as mouse_listener:
            with keyboard.Listener(on_press=on_key_press) as keyboard_listener:
                while tracking_active:
                    time.sleep(0.1)
                # Print all collected positions after tracking stops
                print("\nCollected mouse positions:")
                for position in mouse_positions:
                    print(position)
                return mouse_positions

    # Run the mouse tracking in a separate thread
    mouse_thread = threading.Thread(target=track_mouse)
    mouse_thread.start()

def start_keyboard_listener():
    """Start the keyboard listener."""
    # This set will keep track of currently pressed keys
    current_keys = []

    def on_press(key):
        if key == keyboard.Key.esc:
            return False
        """Handle key press events."""
        try:
            # Regular keys
            print(f"Key pressed: {key.char}")
        except AttributeError:
            # Special keys
            print(f"Special key pressed: {key}")
        # Track currently pressed keys
        current_keys.append(key)

    def track_keyboard():
        # Create the keyboard listener with the defined callbacks
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
            print(current_keys)
            return current_keys
        
    Keybord_listenr = threading.Thread(target=track_keyboard)
    Keybord_listenr.start()