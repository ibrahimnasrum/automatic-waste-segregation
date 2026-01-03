import serial
import serial.tools.list_ports
import time
import threading
import tkinter as tk
from tkinter import ttk, Label, Button
from PIL import Image, ImageTk
import cv2
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from roboflow import Roboflow
import tempfile
import os
import time

# Initialize serial communication variables
ser = None
serial_port = None

# Initialize Roboflow
rf = Roboflow(api_key="eIaTL8oTeoBPqflo5nlV")             #eIaTL8oTeoBPqflo5nlV
project = rf.workspace("roomclassification").project("recycle_waste")
model = project.version(3).model

# Initialize Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file(r"D:\BMCT\SelfProject\2024\IDP - AUTOMATI WASTE SEGREEGATION\New_Code\IntgrationofIOT\credential_api.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet_id = "1N8xN1-jFJoJpZWd9dHyafuZJRh2kIMfSbCzNX7qjT3E"
sheet = client.open_by_key(sheet_id).sheet1

# Update the spreadsheet with material and timestamp
def update_spreadsheet(material):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([material, timestamp])
    print(f"Updated sheet: {material} at {timestamp}")


# Function to capture and classify an image using Roboflow
def capture_and_classify(cap, result_label, captured_image_label):
    global captured_image
    ret, frame = cap.read()
    if ret:
        # Save the captured frame
        captured_image = frame.copy()
        display_captured_image(captured_image, captured_image_label)

        # Save the captured frame as a temporary image file for Roboflow inference
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file_path = temp_file.name
            cv2.imwrite(temp_file_path, captured_image)

            # Make prediction using Roboflow
            prediction = model.predict(temp_file_path).json()

            # Extract the top class and confidence from the prediction
            top_class = prediction['predictions'][0]['top']  # Use 'top' for the top predicted class
            top_confidence = prediction['predictions'][0]['confidence']

            # Display the top class and confidence score
            result_label.config(text=f"Predicted Class: {top_class} | Confidence: {top_confidence*100:.2f}%")
            
            # Map the predicted class to the corresponding command
            if top_class == 'glass':
                send_command('a')  # Send 'a' for Glass
                update_spreadsheet(top_class)
            elif top_class == 'metal':
                send_command('b')  # Send 'b' for Metal
                update_spreadsheet(top_class)
            elif top_class == 'plastic':
                send_command('c')  # Send 'c' for Plastic
                update_spreadsheet(top_class)
            elif top_class == 'paper':
                send_command('d')  # Send 'd' for Paper
                update_spreadsheet(top_class)
            else:
                print(f"Unknown class: {top_class}")

            time.sleep(1)
            # Clean up the temporary file
            os.remove(temp_file_path)
        
# Function to send a command and update the spreadsheet for manual input
def manual_command(material, command):
    send_command(command)
    update_spreadsheet(material)

# Function to display the live camera feed
def update_camera_display(cap, live_camera_label):
    ret, frame = cap.read()
    if ret:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        live_camera_label.imgtk = imgtk
        live_camera_label.configure(image=imgtk)
    
    live_camera_label.after(10, update_camera_display, cap, live_camera_label)

# Function to display the captured image
def display_captured_image(frame, captured_image_label):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    captured_image_label.imgtk = imgtk
    captured_image_label.configure(image=imgtk)

# Initialize serial communication functions
def connect_serial(port):
    global ser
    try:
        ser = serial.Serial(port, 9600, timeout=1)
        time.sleep(2)  # Wait for the connection to initialize
        print(f"Connected to {port} at 9600 baud.")
        start_listening_for_responses()  # Start listening for Arduino responses
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def send_command(command):
    disable_buttons()
    global ser
    if ser and ser.is_open:
        try:
            ser.write(command.encode())
            print(f"Sent: {command}")
        except Exception as e:
            print(f"Error sending command: {e}")
    else:
        print("Serial port not connected.")

def refresh_ports():
    ports = [port.device for port in serial.tools.list_ports.comports()]
    com_port_dropdown['values'] = ports
    if ports:
        com_port_dropdown.set(ports[0])
    else:
        com_port_dropdown.set("No Ports Available")

def select_port():
    global serial_port
    port = com_port_dropdown.get()
    if port and connect_serial(port):
        serial_port_label.config(text=f"Connected to {port}")
        enable_buttons()
    else:
        serial_port_label.config(text="Connection Failed")

def enable_buttons():
    button_a.state(["!disabled"])
    button_b.state(["!disabled"])
    button_c.state(["!disabled"])
    button_d.state(["!disabled"])

def disable_buttons():
    button_a.state(["disabled"])
    button_b.state(["disabled"])
    button_c.state(["disabled"])
    button_d.state(["disabled"])

def listen_for_responses():
    global ser
    while True:
        if ser and ser.is_open:
            try:
                response = ser.readline().decode().strip()
                if response:
                    print(f"Arduino response: {response}")
                    if response == 'i':
                        enable_buttons()
            except Exception as e:
                print(f"Error reading response: {e}")
                break
        else:
            time.sleep(0.1)

def start_listening_for_responses():
    listener_thread = threading.Thread(target=listen_for_responses, daemon=True)
    listener_thread.start()

def toggle_mode():
    if mode_switch.get() == "Manual Operation":
        manual_frame.grid()  # Show manual operation frame
        future_frame.grid_remove()  # Hide future operation frame
        enable_buttons()
    else:
        manual_frame.grid_remove()  # Hide manual operation frame
        future_frame.grid()  # Show future operation frame
        disable_buttons()

def refresh_table(tree, sheet):
    # Fetch the latest data
    values_list = sheet.sheet1.get('D1:E5')
    
    # Clear the existing data in the Treeview
    for row in tree.get_children():
        tree.delete(row)
    
    # Insert the updated data into the Treeview
    for row in values_list[1:]:  # Skip the header row (row[0])
        tree.insert("", "end", values=row)

    
# Function to create and display the Treeview table
def create_table(frame):
    # Spreadsheet ID and sheet reference
    sheet = client.open_by_key(sheet_id)
    values_list = sheet.sheet1.get('D1:E5')
    tree_frame = ttk.Frame(frame)
    tree_frame.grid(row=4, column=0, padx=10, pady=10, sticky=tk.NSEW)

    tree = ttk.Treeview(tree_frame, columns=("Class", "Status"), show="headings")
    tree.heading("Class", text="Class")
    tree.heading("Status", text="Status")

    # Configure columns
    tree.column("Class", anchor=tk.W)  # Left-align the "Class" column
    tree.column("Status", anchor=tk.CENTER)  # Center-align the "Status" column

    # Insert the data into the Treeview widget
    for row in values_list[1:]:  # Skip the header row (row[0])
        tree.insert("", "end", values=row)

    # Add a scrollbar to the Treeview widget
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Pack the Treeview widget
    tree.pack(padx=10, pady=10)
    
    # Add the refresh button
    refresh_button = ttk.Button(tree_frame, text="Refresh", command=lambda: refresh_table(tree, sheet))
    refresh_button.pack(pady=10)
    

# Initialize the GUI application
app = tk.Tk()
app.title("Serial Communication with Arduino")

# Top Frame for Serial Port Selection
top_frame = ttk.Frame(app)
top_frame.pack(fill=tk.X, padx=10, pady=5)

serial_port_label = ttk.Label(top_frame, text="No Serial Port Connected")
serial_port_label.grid(row=0, column=0, padx=5, sticky=tk.W)

com_port_dropdown = ttk.Combobox(top_frame, state="readonly")
com_port_dropdown.grid(row=0, column=1, padx=5)

refresh_button = ttk.Button(top_frame, text="Refresh Ports", command=refresh_ports)
refresh_button.grid(row=0, column=2, padx=5)

select_port_button = ttk.Button(top_frame, text="Connect", command=select_port)
select_port_button.grid(row=1, column=2, padx=5, pady=5)

# Mode Switch
mode_switch = tk.StringVar(value="Manual Operation")
mode_toggle = ttk.Checkbutton(
    top_frame, text="Manual Operation", variable=mode_switch, onvalue="Manual Operation",
    offvalue="Future Operation", command=toggle_mode
)
mode_toggle.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

# Main Frame for Modes
main_frame = ttk.Frame(app)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Manual Operation Frame
manual_frame = ttk.Frame(main_frame)
manual_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N)

button_a = ttk.Button(manual_frame, text="Glass", command=lambda: manual_command('glass', 'a'), width=20, padding=10)
button_a.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

button_b = ttk.Button(manual_frame, text="Metal", command=lambda: manual_command('metal', 'b'), width=20, padding=10)
button_b.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

button_c = ttk.Button(manual_frame, text="Plastic", command=lambda: manual_command('plastic', 'c'), width=20, padding=10)
button_c.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

button_d = ttk.Button(manual_frame, text="Paper", command=lambda: manual_command('paper', 'd'), width=20, padding=10)
button_d.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# Ensure that the columns expand to fill the space
manual_frame.grid_columnconfigure(0, weight=1)

# Status Table
create_table(manual_frame)

# Initially disable the buttons
disable_buttons()


# Future Operation Frame (Webcam)
future_frame = ttk.Frame(main_frame)
future_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N)
future_frame.grid_remove()  # Hide initially

live_camera_label = Label(future_frame)
live_camera_label.grid(row=0, column=0, padx=10, pady=10)

captured_image_label = Label(future_frame)
captured_image_label.grid(row=0, column=1, padx=10, pady=10)

result_label = Label(future_frame, text="Predicted Class: None | Confidence: 0.00%")
result_label.grid(row=2, column=0, columnspan=2)

capture_button = Button(future_frame, text="Capture and Classify", 
                        command=lambda: capture_and_classify(cap, result_label, captured_image_label))
capture_button.grid(row=1, column=0, columnspan=2, pady=10)

# Open the camera
cap = cv2.VideoCapture(1)  # 1 for external camera, adjust if necessary

# Start the camera feed update loop
update_camera_display(cap, live_camera_label)

# Populate the COM port dropdown initially
refresh_ports()

# Run the GUI application
app.mainloop()

# Release the camera when the program ends
cap.release()
cv2.destroyAllWindows()