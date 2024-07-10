# Matrix API

The Matrix API is a Flask-based RESTful API designed to control an LED matrix display. It integrates various functionalities including weather updates, pool art display, time display, Hilbert curve animation, and a wave function collapse (WFC) algorithm for generating patterns. This project also includes a CircuitPython component for interacting with the API from a microcontroller.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip for installing Python packages
- Virtual environment (optional but recommended)
- CircuitPython compatible hardware (for the CircuitPython part)

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

- `/api/weather`: Displays the current weather information on the LED matrix.
- `/api/pool`: Displays pool art on the LED matrix.
- `/api/time`: Displays the current time on the LED matrix.
- `/api/hilbert`: Displays a Hilbert curve animation on the LED matrix.
- `/api/wfc`: Generates and displays a pattern using the wave function collapse algorithm.

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