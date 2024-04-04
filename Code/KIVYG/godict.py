import json

class MyClass:
    def __init__(self):
        # Assuming these are some attributes of your class
        self.start_sig_box = "start_sig_box_value"
        self.start_sig = "start_sig_value"
        self.play_button2 = "play_button2_value"
        self.signal_type_spinner = "signal_type_spinner_value"
        

    def convert_to_json(self):
        widget_dict = {
            'start_sig_box': self.start_sig_box,
            'start_sig': self.start_sig,
            'play_button2': self.play_button2,
            'signal_type_spinner': self.signal_type_spinner,
            'phase_shift_label': self.phase_shift_label,
            'setup_param_label': self.setup_param_label,
            'amplitude_label': self.amplitude_label,
            'frequency_label': self.frequency_label,
            'offset_label': self.offset_label,
            'amplitude_label_box': self.amplitude_label_box,
            'frequency_label_box': self.frequency_label_box,
            'offset_label_box': self.offset_label_box,
            'phase_shift_label_box': self.phase_shift_label_box,
            'setup_param_box': self.setup_param_box,
            'amplitude_slider': self.amplitude_slider,
            'frequency_slider': self.frequency_slider,
            'offset_slider': self.offset_slider,
            'phase_shift_slider': self.phase_shift_slider
            
        }

        # Convert widget_dict to JSON
        widget_json = json.dumps(widget_dict, indent=4)

        # Print the JSON
        print(widget_json)

# Create an instance of MyClass
my_object = MyClass()
# Call the method to convert to JSON
my_object.convert_to_json()
