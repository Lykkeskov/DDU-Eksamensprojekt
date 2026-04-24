class ComboDetector:
    def detect(self, buffer_inputs):
        # Eksempel på kombinationer i mortal kombat (se Getdata.py for implementeret kombination)

        if buffer_inputs[-3:] == ["↓", "→", "1"]:
            return "FIREBALL"

        if buffer_inputs[-3:] == ["←", "→", "3"]:
            return "SPECIAL_KICK"

        return None