import yaml


class BotDefinition:
    def __init__(self, yaml_file):
        with open(yaml_file, "r") as f:
            self.data = yaml.safe_load(f)

    def get_bot_token(self):
        return self.data["bot"]["token"]

    def get_start_message(self):
        return self.data["bot"]["start_message"]

    def get_states(self):
        return self.data["states"]


def parse_bot_definition(yaml_file):
    return BotDefinition(yaml_file)


if __name__ == "__main__":
    bot_definition = parse_bot_definition("example.yaml")
    print(bot_definition.get_bot_token())
    print(bot_definition.get_start_message())
    print(bot_definition.get_states())
