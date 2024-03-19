import imgui
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import cv2

# Dummy data for visualization
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Callback function for rendering the visualization
def render_visualization():
    global x, y

    # Begin ImGui window
    imgui.begin("Visualization", True)

    # Add a plot
    imgui.plot_lines("Sine Wave", x, y)

    # End ImGui window
    imgui.end()

# Main loop for rendering the ImGui visualization
def main():
    while not imgui.should_close():
        imgui.new_frame()

        # Render the visualization
        render_visualization()

        # Render ImGui
        imgui.render()
        imgui_impl.opengl3_render_draw_data(imgui.get_draw_data())

# Initialize ImGui
imgui.create_context()
imgui_impl = imgui.get_impl()
imgui_impl.enable_keyboard_navigation = False

# Main function
if __name__ == "__main__":
    main()
