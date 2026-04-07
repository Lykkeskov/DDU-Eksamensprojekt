class ComboDetector:
    def detect(self, buffer_inputs):
        # Example MK-style combos

        if buffer_inputs[-3:] == ["↓", "→", "1"]:
            return "FIREBALL"

        if buffer_inputs[-3:] == ["←", "→", "3"]:
            return "SPECIAL_KICK"

        return None