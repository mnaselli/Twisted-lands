import random

# Base creatures
base_creatures = {
    'scorpion': {
        'left_arm': 'scorpion pincer',
        'right_arm': 'scorpion pincer',
        'back_legs': 'scorpion legs',
        'torso': 'scorpion torso',
        'head': 'scorpion head',
        'tail': 'scorpion stinger',
        'wings': None
    },
    'bear': {
        'left_arm': 'bear paws',
        'right_arm': 'bear paws',
        'back_legs': 'bear paws',
        'torso': 'bear torso',
        'head': 'bear head',
        'tail': None,
        'wings': None
    },
    'dog': {
        'left_arm': 'dog paw',
        'right_arm': 'bear paw',
        'back_legs': 'dog paws',
        'torso': 'dog torso',
        'head': 'dog head',
        'tail': None,
        'wings': None
    },
    'crab': {
        'left_arm': 'crab pincer',
        'right_arm': 'crab pincer',
        'back_legs': 'crab legs',
        'torso': 'crab torso',
        'head': 'crab head',
        'tail': None,
        'wings': None
    },
    'squirrel': {
        'left_arm': 'squirrel paw',
        'right_arm': 'squirrel paw',
        'back_legs': 'squirrel legs',
        'torso': 'squirrel torso',
        'head': 'squirrel head',
        'tail': None,
        'wings': None
    },
    'snake': {
        'left_arm': None,
        'right_arm': None,
        'back_legs': None,
        'torso': 'snake torso',
        'head': 'snake head',
        'tail': None,
        'wings': None
    },
    'rat': {
        'left_arm': 'rat paw',
        'right_arm': 'rat paw',
        'back_legs': 'rat paws',
        'torso': 'rat torso',
        'head': 'rat head',
        'tail': None,
        'wings': None
    },
    'giant rat': {
        'left_arm': 'rat paw',
        'right_arm': 'rat paw',
        'back_legs': 'rat paws',
        'torso': 'rat torso',
        'head': 'rat head',
        'tail': None,
        'wings': None
    },
    'rabid rat': {
        'left_arm': 'rat paw',
        'right_arm': 'rat paw',
        'back_legs': 'rat paws',
        'torso': 'rat torso',
        'head': 'rabid rat head',
        'tail': None,
        'wings': None
    },
    'monkey': {
        'left_arm': 'monkey paw',
        'right_arm': 'monkey paw',
        'back_legs': 'monkey paws',
        'torso': 'monkey torso',
        'head': 'monkey head',
        'tail': 'monkey tail',
        'wings': None
    },
    'rothe': {
        'left_arm': 'rothe hooves',
        'right_arm': 'rothe hooves',
        'back_legs': 'rothe hooves',
        'torso': 'rothe torso',
        'head': 'rothe head',
        'tail': None,
        'wings': None
    },
    'centipede': {
        'left_arm': None,
        'right_arm': None,
        'back_legs': 'centipede legs',
        'torso': 'centipede torso',
        'head': 'centipede head',
        'tail': None,
        'wings': None
    },

}

# Body parts
alternatives = {
    'left_arm': ['eagle claws', 'frog legs'],
    'right': ['eagle claws', 'frog legs'],
    'back_legs': ['lion legs', 'horse hooves', 'frog legs'],
    'torso': ['turtle shell', 'human torso'],
    'head': ['wolf head', 'shark head', 'bird head'],
    'tail': ['crocodile tail', 'fox tail'],
    'wings': ['bat wings', 'butterfly wings', 'bird wings']
}

# Generate hybrid creature with cero to two mod
def generate_hybrid():
    base_name, base_creature = random.choice(list(base_creatures.items()))
    modified_creature = base_creature.copy()

    parts_to_modify = random.sample(list(base_creature.keys()), k=random.randint(0, 2))
    
    for part in parts_to_modify:
        if part in alternatives and alternatives[part]:
            modified_creature[part] = random.choice(alternatives[part])

    return base_name, modified_creature