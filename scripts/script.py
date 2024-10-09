import os
import importlib
from datetime import datetime
import pickle  # Import pickle for serialization
import gradio as gr
from modules import scripts, processing
from modules.processing import StableDiffusionProcessingImg2Img

class RetainControlNet(scripts.Script):
    def __init__(self):
        super().__init__()
        self.controlNetModule = None  # Placeholder for the ControlNet module
        # Directory to store saved configurations
        self.config_dir = os.path.join(os.path.dirname(__file__), "rcn_configs")
        os.makedirs(self.config_dir, exist_ok=True)
        # Initialize saved configurations
        self.saved_configs = self.get_saved_configs()
        # Switch to ensure process runs only once per generation
        self.has_run = False

    def title(self):
        return "RetainControlNet"

    def show(self, is_img2img):
        return scripts.AlwaysVisible
        
    def update_dropdown(self):
        new_choices = ["None"] + self.get_saved_configs()
        return gr.Dropdown.update(choices=new_choices)

    def ui(self, is_img2img):
        with gr.Accordion("Retain ControlNet Settings", open=False):
            with gr.Row():
                config_name = gr.Textbox(
                    label="Configuration Name",
                    value="",
                    placeholder="Enter a name to save ControlNet settings",
                    interactive=True
                )
                saved_configs = gr.Dropdown(
                    choices=["None"] + self.saved_configs,
                    label="Load Saved Configuration",
                    value="None",
                    interactive=True
                )
                update_button = gr.Button("Update")

        update_button.click(
            fn=self.update_dropdown,
            inputs=[],
            outputs=saved_configs
        )


        return [config_name, saved_configs]

    def process(self, p: StableDiffusionProcessingImg2Img, config_name: str, selected_config: str):
        if self.has_run:
            return
            
        if selected_config == None or selected_config == "None":
            if config_name == None or config_name == "":
                return p

        # Set the switch to prevent further runs during this generation
        self.has_run = True

        # Dynamically import the ControlNet module if not already loaded
        if self.controlNetModule is None:
            try:
                self.controlNetModule = importlib.import_module(
                    'extensions.sd-webui-controlnet.scripts.external_code', 'external_code'
                )
                print("[RetainControlNet] ControlNet module loaded successfully.")
            except ImportError:
                self.controlNetModule = None
                print("[RetainControlNet] Failed to load ControlNet module.")
                return

        if not self.controlNetModule:
            return

        # Save Configuration if config_name is provided
        if config_name:
            self.save_configuration(config_name, p)
            # Refresh saved configurations and reset config name
            self.saved_configs = self.get_saved_configs()
            return

        # Load Configuration if selected_config is provided and not "None"
        if selected_config and selected_config != "None":
            self.load_configuration(selected_config, p)

    def postprocess(self, p: StableDiffusionProcessingImg2Img, processed, *args):
        # Reset the switch after processing is complete
        self.has_run = False

    def get_saved_configs(self):
        """Retrieve a list of saved configuration names."""
        configs = []
        for filename in os.listdir(self.config_dir):
            if filename.endswith(".pkl"):  # Updated to .pkl
                config_name = os.path.splitext(filename)[0]
                configs.append(config_name)
        return configs

    def save_configuration(self, config_name, p: StableDiffusionProcessingImg2Img):
        """Save the current ControlNet settings to a pickle file."""
        # Sanitize the config_name to create a valid filename
        sanitized_name = "".join([c if c.isalnum() or c in (' ', '_', '-') else '_' for c in config_name]).strip()
        if not sanitized_name:
            sanitized_name = f"config_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        filename = f"{sanitized_name}.pkl"  # Changed extension to .pkl
        filepath = os.path.join(self.config_dir, filename)

        # Avoid overwriting existing configurations by appending a timestamp if necessary
        if os.path.exists(filepath):
            print(f"[RetainControlNet] Already Exists (skipping save): '{filepath}'")
            #timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S")
            #filename = f"{sanitized_name}{timestamp}.pkl"
            #filepath = os.path.join(self.config_dir, filename)
            return

        try:
            # Get the current ControlNet settings as a list of units
            control_net_list = self.controlNetModule.get_all_units_in_processing(p)

            # Serialize the list using pickle
            with open(filepath, 'wb') as f:
                pickle.dump(control_net_list, f)

            print(f"[RetainControlNet] Configuration '{filename}' saved successfully.")
        except Exception as e:
            print(f"[RetainControlNet] Error saving configuration '{filename}': {e}")

    def load_configuration(self, config_name, p: StableDiffusionProcessingImg2Img):
        """Load ControlNet settings from a pickle file and apply them to 'p'."""
        filename = f"{config_name}.pkl"  # Changed extension to .pkl
        filepath = os.path.join(self.config_dir, filename)

        if not os.path.exists(filepath):
            print(f"[RetainControlNet] Configuration file '{filename}' does not exist.")
            return

        try:
            # Deserialize the ControlNet settings from the pickle file
            with open(filepath, 'rb') as f:
                control_net_list = pickle.load(f)

            # Use ControlNet's method to update the processing job with the loaded configurations
            self.controlNetModule.update_cn_script_in_processing(p, control_net_list)

            print(f"[RetainControlNet] Configuration '{filename}' loaded successfully.")
        except Exception as e:
            print(f"[RetainControlNet] Error loading configuration '{filename}': {e}")

