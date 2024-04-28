import json

def load_json(path):
    """
    Load a JSON file from a given path.

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data.
    """
    with open(path, 'r') as f:
        return json.load(f)

def write_json(path, data):
    """
    Write data to a JSON file.

    Args:
        path (str): The path to the JSON file.
        data (dict): The data to write.
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def check_conditions(conditions, player_data):
    """
    Check if all conditions are met.

    Args:
        conditions (dict): The conditions to check.
        player_data (dict): The player's data.

    Returns:
        bool: True if all conditions are met, False otherwise.
    """
    for condition, value in conditions.items():
        if condition == 'karma':
            player_karma = player_data.get('karma', 0)
            if not (value.get('min', 0) <= player_karma <= value.get('max', 100)):
                return False
        elif player_data.get(condition, False) != value:
            return False
    return True

def simulate_dialogue(dialogue_data, world_data):
    """
    Simulate a dialogue based on the given data.

    Args:
    dialogue_data (dict): The dialogue data.
    world_data (dict): The world data.

    Returns:
    dict: A dictionary of actions captured during the dialogue.
    """
    dialogue_id = 'dialogue_01'  # Start with the first dialogue
    actions_taken = {}  # Dictionary to store the actions taken

    while True:
        dialogue = dialogue_data[dialogue_id]
        player_karma = world_data['player_data'].get('karma', 0)

        # Select the text that meets all conditions and has the highest min karma that the player's karma is above or equal to
        text = max((text for text in dialogue['text'] if check_conditions(text.get('conditions', {}), world_data['player_data'])), key=lambda text: text.get('conditions', {}).get('karma', {}).get('min', 0))

        print(text['content'].format(player_name=world_data['player_data']['player_name']))

        # Store the actions in the actions_taken dictionary
        actions = text.get('actions', {})
        actions_taken.update(actions)

        # If end_dialogue is true, end the dialogue and return the actions_taken
        if actions.get('end_dialogue', False):
            return actions_taken

        # Process responses
        for i, response in enumerate(dialogue['responses']):
            conditions = response.get('conditions', {})

            # Check if all conditions are met
            if check_conditions(conditions, world_data['player_data']):
                print(f"{i+1}. {response['text']}")

        # Get user input
        user_input = int(input("Select a response: ")) - 1

        # Store the actions in the actions_taken dictionary
        actions = dialogue['responses'][user_input].get('actions', {})
        actions_taken.update(actions)

        # If end_dialogue is true, end the dialogue and return the actions_taken
        if actions.get('end_dialogue', False):
            return actions_taken

        # Move to the next dialogue
        dialogue_id = dialogue['responses'][user_input]['next']

def update_world_data(actions_taken, world_data):
    """
    Update the world data based on the actions taken during the dialogue.

    Args:
        actions_taken (dict): The actions taken during the dialogue.
        world_data (dict): The world data.

    Returns:
        dict: The updated world data.
    """
    for action, value in actions_taken.items():
        if action in world_data['player_data']:
            world_data['player_data'][action] = value

    return world_data

def main():
    """
    The main function to run the dialogue simulation.
    """
    # Load the dialogue and world data
    dialogue_data = load_json('dialogue/testing/test_dialogue.json')
    world_data = load_json('dialogue/testing/test_world_data.json')

    # Run the dialogue simulation
    dialogue_results = simulate_dialogue(dialogue_data, world_data)

    # Update the world data based on the dialogue results
    update_world_data(dialogue_results, world_data)

if __name__ == "__main__":
    main()