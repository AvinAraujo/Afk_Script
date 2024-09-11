from pynput import mouse, keyboard
import time, threading

# Global variables
mouse_positions = []
tracking = True

def start_mouse_tracking():
    """Start tracking the mouse position and save only when left click is pressed."""
    global mouse_positions, tracking
    mouse_positions = []  # Reset the list to start fresh
    tracking = True  # Reset tracking flag

    def on_click(x, y, button, pressed):
        """Handle mouse click events."""
        if pressed and button == mouse.Button.left:
            # Save the position when left click is pressed
            mouse_positions.append((x, y))
            print(f"Position saved: {(x, y)}")
            # Optionally limit the size of the saved positions list
            if len(mouse_positions) > 5:  # Adjust the limit as needed
                mouse_positions.pop(0)

    def on_key_press(key):
        """Handle keyboard events to stop tracking on 'Esc' key press."""
        global tracking
        if key == keyboard.Key.esc:
            print("\nEsc key pressed. Stopping tracking.")
            tracking = False
            return False  # Stop the keyboard listener

    def track_mouse():
        """Function to track mouse position in a separate thread."""
        # Start the mouse listener in the background
        with mouse.Listener(on_click=on_click) as mouse_listener:
            # Start the keyboard listener in the background
            with keyboard.Listener(on_press=on_key_press) as keyboard_listener:
                try:
                    while tracking:
                        time.sleep(0.1)
                except KeyboardInterrupt:
                    print("\nStopped tracking mouse position.")
                finally:
                    # Ensure the listeners are stopped
                    mouse_listener.stop()
                    keyboard_listener.stop()

                # Print all collected positions after stopping
                print("\nCollected mouse positions:")
                for pos in mouse_positions:
                    print(pos)

    # Run the mouse tracking in a separate thread
    mouse_thread = threading.Thread(target=track_mouse)
    mouse_thread.start()

def start_keyboard_listener():
    """Start the keyboard listener."""
    # This set will keep track of currently pressed keys
    current_keys = set()

    def on_press(key):
        """Handle key press events."""
        try:
            # Regular keys
            print(f"Key pressed: {key.char}")
        except AttributeError:
            # Special keys
            print(f"Special key pressed: {key}")

        # Track currently pressed keys
        current_keys.add(key)

        # Example: Check for a specific combination (Ctrl+C)
        if all(k in current_keys for k in [keyboard.Key.ctrl_l, keyboard.KeyCode(char='c')]):
            print("Ctrl+C combination detected")

    def on_release(key):
        """Handle key release events."""
        print(f"Key released: {key}")

        # Remove the key from the set of currently pressed keys
        current_keys.discard(key)

        # Stop listener if Esc is pressed
        if key == keyboard.Key.esc:
            return False

    # Create the keyboard listener with the defined callbacks
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
        print(current_keys)