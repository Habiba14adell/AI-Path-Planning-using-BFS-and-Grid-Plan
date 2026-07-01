# Cafe Robot Path Planning

A Python path planning project for a cafe delivery robot. The robot moves through a grid-based cafe environment, avoids obstacles, and uses Breadth-First Search (BFS) to find paths to selected desk goals.

## Features

- Grid-based cafe environment
- Obstacles, desks, robot start position, and delivery goals
- Interactive goal selection using mouse clicks
- BFS path planning visualization
- Robot movement animation along the generated path
- Streamlit browser app for running the BFS planner without a Pygame window

## Project Structure

```text
.
+-- Environment.py       # Main application entry point
+-- app.py              # Streamlit browser app
+-- Grids.py             # Grid, cells, states, colors, obstacles, and desks
+-- Robots.py            # Robot behavior and BFS path planning
+-- Generalisation.py    # Experimental/custom grid setup screen
+-- requirements.txt     # Python package dependencies
+-- README.md
```

## Requirements

- Python 3.9 or later
- pip

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

Run the Pygame simulation:

```bash
python Environment.py
```

Run the Streamlit app:

```bash
streamlit run app.py
```

## How to Use

Pygame version:

- Click on red desk cells to choose delivery goals.
- The robot starts from the coffee machine area.
- The robot calculates a BFS path and moves toward the selected goal.
- Close the Pygame window to stop the program.

Streamlit version:

- Choose up to four desk goals from the sidebar.
- Toggle whether the robot should return to the coffee machine.
- View the BFS route, visited cells, obstacles, desks, and goals in the browser.

## Notes

- The project is designed for an AI planning/path planning assignment.
- `Generalisation.py` contains an alternate interface for manually choosing grid elements.

## License

This project is available for educational use.
