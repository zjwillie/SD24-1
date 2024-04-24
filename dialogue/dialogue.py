dialogue = {
    "start": {
        "text": "You are standing in a small town. There's a path leading to the forest to the north, and a road going into the city to the south.",
        "options": {
            "Head north into the forest": "forest",
            "Go south into the city": "city"
        }
    },
    "forest": {
        "text": "You walk for a while until you reach a clearing with a large, ancient-looking tree.",
        "options": {
            "Examine the tree": "tree",
            "Go back to the town": "start"
        }
    },
    "tree": {
        "text": "The tree is covered in moss and looks like it's been here for hundreds of years.",
        "options": {
            "Go back": "forest"
        }
    },
    "city": {
        "text": "The city is bustling with activity. You see a shop nearby.",
        "options": {
            "Enter the shop": "shop",
            "Go back to the town": "start"
        }
    },
    "shop": {
        "text": "The shopkeeper greets you warmly.",
        "options": {
            "Go back": "city"
        }
    }
}

def game_loop():
    location = "start"
    while True:
        print(dialogue[location]["text"])
        choice = input("Options: " + ", ".join(dialogue[location]["options"].keys()) + "\n")
        if choice in dialogue[location]["options"]:
            location = dialogue[location]["options"][choice]
        else:
            print("Invalid option.")

game_loop()