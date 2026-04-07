class GameInputMapper:
    def map(self, punch=False, direction=None):
        inputs = []

        if direction == "RIGHT":
            inputs.append("→")
        elif direction == "LEFT":
            inputs.append("←")
        elif direction == "UP":
            inputs.append("↑")
        elif direction == "DOWN":
            inputs.append("↓")

        if punch:
            inputs.append("1")  # MK11 front punch

        return inputs