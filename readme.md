# Matrix API

The Matrix API is a Flask-based RESTful API designed to control an LED matrix display. It integrates various functionalities including weather updates, pool art display, time display, Hilbert curve animation, and a wave function collapse (WFC) algorithm for generating patterns. This project also includes a CircuitPython component for interacting with the API from a microcontroller.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip for installing Python packages
- Virtual environment (optional but recommended)
- CircuitPython compatible hardware (for the CircuitPython part) using a Adafruit Matrix Portal M4

### Installation

1. Clone the repository to your local machine:

    ```sh
    git clone https://yourrepositoryurl.com/MatrixAPI.git
    ```

2. Navigate to the project directory:

    ```sh
    cd MatrixAPI
    ```

3. (Optional) Create and activate a virtual environment:

    ```sh
    python -m venv env
    .\env\Scripts\activate
    ```

4. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

5. Run the API server:

    ```sh
    python API.py
    ```

    The API will be available at `http://localhost:5000/api`.

## Usage

### Endpoints

- `/`: Method: `GET` Displays the current weather information on the LED matrix.
- `/api/frame`: Method: `GET`,  Params: `index` ~ Get the led values at the current index (varies per type).
- `/api/setframe`: Method: `GET`, Params: `type` ~ Sets the current frame to give according to the `type` param.
- `/api/wfc`: Metohd: `GET` Regenerate the WFC object and display.

### Screens

- pool: Will display a pool graphic, the temperature of the pool and the greenhouse temperature with a super secret number...
- weather: Will display the weather based on your current location.
- time: Displays an analog and digital clock for the current time.
- wfc: Generates a WFC screen, and then renders it pixel by pixel.
- hilbert: generates the points, then colours them according to the randomness.
  
### CircuitPython

The `circiutpy_files` directory contains CircuitPython code for interacting with the Matrix API from a microcontroller. Update the `YOUR_API_URL` variable in `code.py` to point to your running instance of the Matrix API.

## Development

### Adding New Screens

To add a new screen type to the Matrix API:

1. Implement the new functionality in a separate Python module.
2. Import and integrate your module in `API.py`.
3. Add a new endpoint to the Flask app for triggering your screen.

### Logging

The project uses Python's `logging` module for logging. Configure the logging level and format in `API.py`.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
