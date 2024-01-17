import tkinter as tk
from tkinter import ttk

def close_window():
    window.destroy()

def option1_selected():
    print("Return to home")

def option2_selected():
    print("Play the game again")

def create_rounded_button(parent, text, command):
    # Create a canvas to draw the rounded rectangle
    canvas = tk.Canvas(parent, width=100, height=30, highlightthickness=0)

    # Draw a rounded rectangle
    rounded_rectangle = canvas.create_rounded_rectangle(0, 0, 100, 30, radius=8, fill='red', outline='gray')

    # Add text to the button
    text_id = canvas.create_text(50, 15, text=text, fill='black')

    # Bind the button functionality
    canvas.bind('<Button-1>', lambda event: command())

    return canvas

# Add a rounded rectangle drawing method to the Canvas widget
def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
    points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]

    return self.create_polygon(points, **kwargs, smooth=True)

# Inject the create_rounded_rectangle method into the Canvas class
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle

# Create the main window
window = tk.Tk()
window.title("AlertBox")

# Remove the maximize and minimize buttons
window.attributes('-toolwindow', True)
window.attributes('-topmost', 1)

# Set the window size
window_width = 406
window_height = 264

# Get screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window position to center
left_position = (screen_width - window_width) // 2
top_position = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{left_position}+{top_position}")

# Create a frame to hold the buttons
frame = tk.Frame(window)

# Create two rounded buttons
button1 = create_rounded_button(frame, "Home", option1_selected)
button1.pack(side="left", padx=10)

button2 = create_rounded_button(frame, "Play Again", option2_selected)
button2.pack(side="right", padx=10)

# Pack the frame at the bottom of the window
frame.pack(side="bottom", pady=10)

# Create two labels for displaying two lines of text in the middle
text_line1 = "It's a tie"

label1 = tk.Label(window, text=text_line1, font=("Helvetica", 16))
label1.place(relx=0.5, rely=0.15, anchor="n")

label2 = tk.Label(window, text=text_line2, font=("Helvetica", 16))
label2.place(relx=0.5, rely=0.45, anchor="center")

# Run the main loop
window.mainloop()
