from src.hazards.warning_manager import WarningManager


manager = WarningManager()


states = [
    "WHITE",
    "YELLOW",
    "YELLOW",
    "RED",
    "RED",
    "YELLOW",
    "WHITE",
]


for state in states:
    update = manager.update(state)

    print(
        f"{update.previous_state} -> "
        f"{update.current_state} | "
        f"Beep: {update.beep}"
    )