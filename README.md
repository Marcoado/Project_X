# Timerzone - Computer Activity Simulator

A Python application that simulates computer activity by automatically generating mouse movements and keyboard inputs. This tool can be useful for keeping your computer active, testing applications, or simulating user behavior.

## Features

- **Keyboard Simulation**: Automatically presses specified keys at configurable intervals (CPM - Clicks Per Minute)
- **Mouse Simulation**: Generates subtle mouse movements to simulate user activity
- **Multiple Interfaces**: 
  - Command-line interface for quick usage
  - Graphical user interface (GUI) for easy configuration
  - Windows Service for background operation
  - WSL/Linux service support
- **Configurable Parameters**:
  - Adjustable keyboard press frequency
  - Customizable key selection
  - Mouse movement intervals
  - Randomization options for more natural behavior
- **Cross-Platform**: Works on Windows and Linux (WSL)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Windows-specific Dependencies

On Windows, the following additional packages are required:
- `pywin32` (for Windows service functionality)

These are automatically included in the requirements.txt file.

## Usage

### 1. Command Line Interface

Run the simulator directly from the command line:

```bash
python main.py [options]
```

**Available Options:**
- `--cpm N`: Set clicks per minute (default: 120)
- `--key KEY`: Specify which key to press (default: space)
- `--mouse-interval N`: Mouse movement interval in seconds (default: 5.0)
- `--mouse-enable`: Enable mouse simulation (default: enabled)
- `--no-mouse`: Disable mouse simulation
- `--duration N`: Run for N seconds (0 = infinite, default: 0)
- `--randomize-interval`: Add slight randomness to intervals
- `--list-keys`: List all supported keys and exit

**Examples:**
```bash
# Basic usage with default settings
python main.py

# Simulate 60 key presses per minute with F15 key
python main.py --cpm 60 --key f15

# Disable mouse simulation, run for 300 seconds
python main.py --no-mouse --duration 300

# Add randomization for more natural behavior
python main.py --randomize-interval
```

### 2. Graphical User Interface

Launch the GUI application:

```bash
python ui.py
```

The GUI provides:
- Easy configuration of all simulation parameters
- Start/Stop controls
- Save configuration to `config.json`
- Real-time parameter adjustment

### 3. Windows Service

Install as a Windows service for background operation:

```bash
# Install the service
python service.py install

# Start the service
python service.py start

# Stop the service
python service.py stop

# Remove the service
python service.py remove
```

The service reads configuration from `config.json` and runs continuously in the background.

### 4. WSL/Linux Service

For WSL or Linux systems, use the provided installation script:

```bash
# Install with default settings
./scripts/install_wsl_service.sh

# Install with custom virtual environment
./scripts/install_wsl_service.sh --venv /path/to/venv

# Install for specific user
./scripts/install_wsl_service.sh --user username
```

## Configuration

### Configuration File (config.json)

The application can be configured using a `config.json` file:

```json
{
  "cpm": 120,
  "key": "space",
  "mouse_enable": true,
  "mouse_interval": 5.0,
  "randomize_interval": false
}
```

**Configuration Parameters:**
- `cpm`: Clicks per minute (keyboard presses)
- `key`: Key to press (e.g., "space", "f15", "ctrl")
- `mouse_enable`: Enable/disable mouse simulation
- `mouse_interval`: Seconds between mouse movements
- `randomize_interval`: Add randomness to timing intervals

### Supported Keys

Use `python main.py --list-keys` to see all supported keys. Common keys include:
- `space`, `enter`, `tab`
- `f1` through `f24`
- `ctrl`, `alt`, `shift`
- `up`, `down`, `left`, `right`
- And many more...

## Safety Features

- **Failsafe**: Move mouse to top-left corner to stop simulation
- **Graceful Shutdown**: Proper cleanup when stopping
- **Error Handling**: Robust error handling and logging
- **Resource Management**: Efficient thread management

## File Structure

```
Project_X/
├── main.py              # Command-line interface
├── ui.py                # Graphical user interface
├── simulator.py         # Core simulation logic
├── service.py           # Windows service implementation
├── service_wsl.py       # WSL/Linux service implementation
├── config.json          # Configuration file
├── requirements.txt     # Python dependencies
├── scripts/
│   └── install_wsl_service.sh  # WSL service installer
└── README.md           # This file
```

## Troubleshooting

### Common Issues

1. **Permission Errors (Windows Service)**:
   - Run as Administrator when installing/removing services
   - Ensure proper permissions for service account

2. **Import Errors**:
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Service Not Starting**:
   - Check Windows Event Viewer for error details
   - Verify `config.json` exists and is valid
   - Ensure Python path is correct in service configuration

4. **Mouse/Keyboard Not Working**:
   - Check if another application is blocking input
   - Verify failsafe is not triggered (mouse in top-left corner)
   - Test with different keys or mouse intervals

### Logs and Debugging

- **Windows Service**: Check Windows Event Viewer
- **WSL Service**: Use `journalctl --user -u simulator.service`
- **Command Line**: Output appears in terminal

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational and testing purposes. Please use responsibly and in accordance with your organization's policies.

## Disclaimer

This tool is designed for legitimate purposes such as:
- Keeping computers active during presentations
- Testing application behavior
- Simulating user activity for development

Please ensure you have proper authorization before using this tool in any environment, and use it responsibly.
