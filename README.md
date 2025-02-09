# CS2 POV Player

## 📌 Project Description
CS2 POV Player is a Python-based tool designed to **automate and enhance the experience of watching CS2 demo files**. It allows users to:

- Select a `.dem` file via a graphical user interface (GUI).
- Parse the demo to extract player and round information.
- Automatically **skip to specific rounds** or follow a player's POV.
- **Manually skip rounds** using a hotkey (`N`).
- **Exit to the main menu** after the last round is played.
- Integrate with **OBS WebSocket** for automatic recording.

This tool is useful for **analysts, content creators, and competitive players** who need a streamlined way to review match footage efficiently.

---

## 🚀 Installation Instructions
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/nickdevroye/cs2pov-player.git
cd cs2pov-player
```

### **2️⃣ Create and Activate a Virtual Environment**
- **Windows (PowerShell):**
  ```sh
  python -m venv venv
  venv\Scripts\Activate
  ```
- **macOS/Linux:**
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Configure Settings**
Modify the `config.json` file (see the Configuration section below) to match your system setup.

---

## 📖 Usage Examples
### **Run the GUI for Easy Demo Selection**
```sh
python scripts/gui.py
```
This will launch a graphical interface where you can select your demo file and player.

### **Run a Demo Directly from the Command Line**
```sh
python scripts/pov_player.py demo_name.dem player_name
```
Example:
```sh
python scripts/pov_player.py astralis-vs-wildcard-m1-inferno.dem dev1ce
```

### **Skipping Rounds Manually**
- While watching a demo, press **`N`** to skip to the next round.
- On the **last round**, pressing `N` will **exit to the main menu** (`disconnect`).

---

## ⚙ Configuration Details
The tool requires a `config.json` file stored in the `config/` directory. Example:
```json
{
    "obs_host": "192.168.1.206",
    "obs_port": 4455,
    "obs_password": "your_obs_password",
    "game_path": "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo\\"
}
```

### **Configuration Fields:**
- **`obs_host`**: The local IP of the machine running OBS WebSocket.
- **`obs_port`**: The WebSocket port configured in OBS (default: `4455`).
- **`obs_password`**: The WebSocket password set in OBS.
- **`game_path`**: The directory where CS2 demo files are stored.

---

## 🤝 Contributing Guidelines
We welcome contributions! To contribute:

1. **Fork the repository** and create a new branch:
   ```sh
   git checkout -b feature-branch-name
   ```
2. **Make your changes following PEP 8 guidelines**.
3. **Run tests** (if applicable) before submitting.
4. **Commit and push your changes**:
   ```sh
   git commit -m "Added feature XYZ"
   git push origin feature-branch-name
   ```
5. **Submit a pull request (PR)** and describe your changes.

For major feature proposals, please open an issue first to discuss the implementation details.

---

## 📜 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📩 Support & Contact
For questions or issues, please open an [issue on GitHub](https://github.com/nickdevroye/cs2pov-player/issues).

Happy coding! 🚀

