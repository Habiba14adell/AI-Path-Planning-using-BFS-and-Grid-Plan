from collections import deque

import streamlit as st


ROWS = 22
COLUMNS = 16
START = (20, 3)

OBSTACLES = {
    (16, 0), (16, 1), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6),
    (17, 5), (18, 5), (19, 5), (21, 5), (15, 4), (13, 4), (12, 4),
    (12, 5), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (13, 11),
    (15, 11), (16, 11), (16, 12), (16, 13), (16, 14), (16, 15),
    (21, 11), (20, 11), (19, 11), (16, 10), (11, 4), (10, 4), (8, 4),
    (7, 4), (6, 4), (5, 4), (4, 4), (4, 3), (4, 2), (4, 1), (4, 0),
    (3, 0), (2, 0), (1, 0), (0, 0), (0, 1), (1, 1), (2, 1), (3, 1),
    (1, 2), (0, 2), (0, 3), (1, 3), (0, 4), (1, 4), (0, 12),
    (0, 13), (0, 14), (0, 15), (1, 15), (1, 14), (1, 13), (2, 14),
    (2, 15), (0, 5), (9, 4),
}

DESKS = [
    (2, 4), (1, 5), (0, 7), (0, 8), (1, 7), (1, 8), (1, 12), (2, 13),
    (4, 14), (4, 15), (5, 14), (5, 15), (6, 14), (6, 15), (7, 15),
    (12, 15), (13, 15), (14, 15), (4, 10), (4, 9), (5, 9), (5, 10),
    (6, 9), (6, 10), (7, 10), (14, 1), (7, 14), (7, 9),
]

COLORS = {
    "empty": "#ffffff",
    "obstacle": "#111111",
    "desk": "#e03131",
    "robot": "#89cff0",
    "goal": "#7393b3",
    "visited": "#51cf66",
    "path": "#ffd43b",
}


def neighbors(cell, goal):
    row, column = cell
    for row_delta, column_delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        next_cell = (row + row_delta, column + column_delta)
        if is_walkable(next_cell, goal):
            yield next_cell


def is_walkable(cell, goal=None):
    row, column = cell
    return (
        0 <= row < ROWS
        and 0 <= column < COLUMNS
        and cell not in OBSTACLES
        and (cell not in DESKS or cell == goal)
    )


def bfs(start, goal):
    queue = deque([start])
    parents = {start: None}
    visited_order = []

    while queue:
        current = queue.popleft()
        visited_order.append(current)

        if current == goal:
            return build_path(parents, goal), visited_order

        for neighbor in neighbors(current, goal):
            if neighbor not in parents:
                parents[neighbor] = current
                queue.append(neighbor)

    return [], visited_order


def build_path(parents, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parents[current]
    return list(reversed(path))


def build_route(goals, return_to_start):
    current = START
    full_path = []
    all_visited = []
    route_goals = list(goals)

    if return_to_start and route_goals:
        route_goals.append(START)

    for goal in route_goals:
        path, visited = bfs(current, goal)
        all_visited.extend(visited)

        if not path:
            return [], all_visited, goal

        if full_path:
            full_path.extend(path[1:])
        else:
            full_path.extend(path)
        current = goal

    return full_path, all_visited, None


def cell_label(cell):
    return f"Desk {DESKS.index(cell) + 1}: row {cell[0]}, column {cell[1]}"


def render_grid(path, visited, goals):
    path_cells = set(path)
    visited_cells = set(visited)
    goal_cells = set(goals)

    html = ['<div class="grid-board">']
    for row in range(ROWS):
        for column in range(COLUMNS):
            cell = (row, column)
            color_key = "empty"
            label = f"{row},{column}"

            if cell in OBSTACLES:
                color_key = "obstacle"
                label = "Obstacle"
            elif cell in DESKS:
                color_key = "desk"
                label = cell_label(cell)
            if cell in visited_cells:
                color_key = "visited"
                label = f"Visited {row},{column}"
            if cell in path_cells:
                color_key = "path"
                label = f"Path {row},{column}"
            if cell in goal_cells:
                color_key = "goal"
                label = f"Goal {row},{column}"
            if cell == START:
                color_key = "robot"
                label = "Robot start"

            html.append(
                f'<div class="grid-cell" title="{label}" '
                f'style="background:{COLORS[color_key]}"></div>'
            )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


st.set_page_config(page_title="Cafe Robot BFS Planner", layout="wide")

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.25rem;
            max-width: 1100px;
        }
        .grid-board {
            display: grid;
            grid-template-columns: repeat(16, minmax(18px, 28px));
            gap: 4px;
            width: fit-content;
            padding: 8px;
            background: #666;
        }
        .grid-cell {
            width: 100%;
            aspect-ratio: 1 / 1;
            border: 1px solid #333;
            box-sizing: border-box;
        }
        .legend {
            display: flex;
            flex-wrap: wrap;
            gap: 10px 14px;
            margin: 0.5rem 0 1rem;
        }
        .legend-item {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.9rem;
        }
        .swatch {
            width: 14px;
            height: 14px;
            border: 1px solid #333;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Cafe Robot BFS Planner")

with st.sidebar:
    st.header("Route Controls")
    selected_goal_labels = st.multiselect(
        "Choose up to 4 desk goals",
        options=[cell_label(desk) for desk in DESKS],
        default=[cell_label(DESKS[0])],
        max_selections=4,
    )
    return_to_start = st.checkbox("Return to coffee machine", value=True)
    show_visited = st.checkbox("Show visited cells", value=True)

selected_goals = [
    desk for desk in DESKS if cell_label(desk) in selected_goal_labels
]

path, visited, failed_goal = build_route(selected_goals, return_to_start)
visible_visited = visited if show_visited else []

legend_items = [
    ("Robot start", COLORS["robot"]),
    ("Desk", COLORS["desk"]),
    ("Goal", COLORS["goal"]),
    ("Obstacle", COLORS["obstacle"]),
    ("Visited", COLORS["visited"]),
    ("Path", COLORS["path"]),
]

legend_html = ['<div class="legend">']
for label, color in legend_items:
    legend_html.append(
        f'<span class="legend-item"><span class="swatch" '
        f'style="background:{color}"></span>{label}</span>'
    )
legend_html.append("</div>")
st.markdown("".join(legend_html), unsafe_allow_html=True)

if failed_goal:
    st.error(f"No path found to row {failed_goal[0]}, column {failed_goal[1]}.")
elif selected_goals:
    st.success(f"Route found with {max(len(path) - 1, 0)} movement steps.")
else:
    st.info("Choose at least one desk goal from the sidebar.")

render_grid(path, visible_visited, selected_goals)
