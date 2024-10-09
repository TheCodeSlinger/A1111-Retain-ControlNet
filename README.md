# A1111-Retain-ControlNet

### Overview

**A1111-Retain-ControlNet** is an extension for [AUTOMATIC1111's Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) that allows users to retain ControlNet settings and images between console sessions. Additionally, this extension enables quick loading of saved ControlNet configurations, making it easier to reuse settings without having to manually reconfigure them each time.

This tool is particularly useful for artists, developers, and users who frequently experiment with different ControlNet settings and want to maintain consistent configurations across multiple sessions.

### Features

- **Save ControlNet Settings**: Save your ControlNet settings (as a `.pkl` file) with a custom name.
- **Load Saved Configurations**: Quickly load previously saved ControlNet configurations for use in your current session.
- **Retain ControlNet Settings Between Sessions**: Automatically reload ControlNet configurations after restarting the web UI, maintaining consistency across sessions.
- **Simple UI**: Use the extension's built-in UI to save and load configurations effortlessly.
- **Prevents Overwriting Existing Configurations**: Automatically checks if a configuration with the same name exists, avoiding accidental overwrites.

### Why I Made This

I created this extension to simplify the process of reusing ControlNet configurations in **AUTOMATIC1111's Web UI**. Often, I found myself repeatedly setting the same configurations when experimenting with different images or models. Instead of manually inputting these settings for every session, this extension saves the current ControlNet settings and allows them to be quickly reloaded when needed.

This is especially useful for users who experiment with multiple ControlNet models and want to maintain consistency or quickly switch between saved configurations without reconfiguring everything manually.

### Installation

To install the extension:

1. Clone this repository into the `extensions` directory of your **Stable Diffusion Web UI** installation:
   ```bash
   git clone https://github.com/TheCodeSlinger/A1111-Retain-ControlNet.git
