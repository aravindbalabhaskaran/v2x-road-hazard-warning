from dataclasses import dataclass


@dataclass
class WarningUpdate:
    previous_state: str
    current_state: str
    beep: bool


class WarningManager:
    """Manages hazard warning state transitions."""

    def __init__(self):
        self.current_state = "WHITE"

    def update(self, new_state: str) -> WarningUpdate:
        previous_state = self.current_state

        beep = (
            (previous_state == "WHITE" and new_state == "YELLOW")
            or
            (previous_state == "YELLOW" and new_state == "RED")
        )

        self.current_state = new_state

        return WarningUpdate(
            previous_state=previous_state,
            current_state=new_state,
            beep=beep,
        )