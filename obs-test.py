from obswebsocket import obsws, requests
import time

# Define connection parameters
host = "192.168.1.206"
port = 4455
password = "TMhEIwLqry1qMpwV"

# Create an instance of obsws
ws = obsws(host, port, password)

try:
    # Connect to OBS WebSocket server
    ws.connect()
    print("Connected to OBS WebSocket server")

    # Get the current recording directory
    recording_directory = ws.call(requests.GetRecordDirectory()).getRecordDirectory()
    print(f"Current recording directory: {recording_directory}")

    # Optionally, set a new recording directory
    new_directory = "C:\\Your\\New\\Directory"
    ws.call(requests.SetRecordDirectory(RecordDirectory=new_directory))
    print(f"New recording directory set to: {new_directory}")

    # Start recording
    ws.call(requests.StartRecording())
    print("Recording started")
    # Wait for some time (e.g., 10 seconds)
    time.sleep(10)

    # Stop recording
    ws.call(requests.StopRecording())
    print("Recording stopped")

finally:
    # Disconnect from OBS WebSocket server
    ws.disconnect()
    print("Disconnected from OBS WebSocket server")