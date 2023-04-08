from jinja2 import Environment, FileSystemLoader

import parser_bot


def generate_bot_code(bot_definition):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('bot_template.py.j2')

    bot_token = bot_definition.get_bot_token()
    states = bot_definition.get_states()

    rendered_code = template.render(bot_token=bot_token, states=states)

    with open('generated_bot.py', 'w') as f:
        f.write(rendered_code)


if __name__ == '__main__':
    # First, parse the YAML file to create a BotDefinition object
    bot_definition = parser_bot.parse_bot_definition("example.yaml")

    # Then, generate the bot code using the BotDefinition object
    generate_bot_code(bot_definition)
