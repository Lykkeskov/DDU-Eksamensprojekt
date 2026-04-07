class ActionProcessor:
    def process(self, actions):
        inputs = []

        for action in actions:
            if action == "FORWARD":
                inputs.append("→")
            elif action == "BACK":
                inputs.append("←")
            elif action == "DOWN":
                inputs.append("↓")
            elif action == "UP":
                inputs.append("↑")
            elif action == "PUNCH_1":
                inputs.append("1")
            elif action == "PUNCH_2":
                inputs.append("2")
            elif action == "KICK_1":
                inputs.append("3")
            elif action == "KICK_2":
                inputs.append("4")
            elif action == "BLOCK":
                inputs.append("BL")

        return inputs