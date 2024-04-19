
import random

# Base creatures
creatures_by_size = {
    'small': {
        'creatures': {
            'crab': {
                'left_arm': 'crab pincer',
                'right_arm': 'crab pincer',
                'back_legs': 'crab legs',
                'torso': 'crab torso',
                'head': 'crab head',
                'tail': None,
                'wings': None,
                'extras': None
            },
            'scorpion': {
                'left_arm': 'scorpion pincer',
                'right_arm': 'scorpion pincer',
                'back_legs': 'scorpion legs',
                'torso': 'scorpion torso',
                'head': 'scorpion head',
                'tail': 'scorpion stinger',
                'wings': None,
                'extras': None
            },
            'bat': {
                'left_arm': 'bat claws',
                'right_arm': 'bat claws',
                'back_legs': 'bat legs',
                'torso': 'bat torso',
                'head': 'bat head',
                'tail': None,
                'wings': 'bat wings',
                'extras': None
            },
            'squirrel': {
                'left_arm': 'squirrel paw',
                'right_arm': 'squirrel paw',
                'back_legs': 'squirrel legs',
                'torso': 'squirrel torso',
                'head': 'squirrel head',
                'tail': None,
                'wings': None,
                'extras': None
             },
            'snake': {
                'left_arm': None,
                'right_arm': None,
                'back_legs': None,
                'torso': 'snake torso',
                'head': 'snake head',
                'tail': None,
                'wings': None,
                'extras': None
            },
            'rat': {
                'left_arm': 'rat paw',
                'right_arm': 'rat paw',
                'back_legs': 'rat paws',
                'torso': 'rat torso',
                'head': 'rat head',
                'tail': None,
                'wings': None,
                'extras': None
            },
            'centipede': {
                'left_arm': None,
                'right_arm': None,
                'back_legs': 'centipede legs',
                'torso': 'centipede torso',
                'head': 'centipede head',
                'tail': None,
                'wings': None,
                'extras': None
    },
            
        },
        'parts': {
            'left_arm': ['spider leg',],
            'right_arm': ['spider leg',],
            'back_legs': ['spide legs'],
            'torso': ['spider torso'],
            'head': ['cobra head'],
            'tail': ['spider stinger'],
            'wings': ['buterfly wings', 'moth wings', 'dragonfly wings'],
            'extras' : ['beetle horn']
        }
    },
    'medium': {
        'creatures': {
            'dog': {
                'left_arm': 'dog paw',
                'right_arm': 'dog paw',
                'back_legs': 'dog paws',
                'torso': 'dog torso',
                'head': 'dog head',
                'tail': None,
                'wings': None,
                'extras': None
             },
    
            'giant rat': {
                'left_arm': 'rat paw',
                'right_arm': 'rat paw',
                'back_legs': 'rat paws',
                'torso': 'rat torso',
                'head': 'rat head',
                'tail': None,
                'wings': None,
                'extras': None
            },
            'monkey': {
                'left_arm': 'monkey paw',
                'right_arm': 'monkey paw',
                'back_legs': 'monkey paws',
                'torso': 'monkey torso',
                'head': 'monkey head',
                'tail': 'monkey tail',
                'wings': None,
                'extras': None
            },
            'giant roach': {
                'left_arm': 'giant roach leg',
                'right_arm': 'giant roach leg',
                'back_legs': 'giant roach legs',
                'torso': 'giant roach torso',
                'head': 'giant roach head',
                'tail': None,
                'wings': None,
                'extras': None
            },
        },
        'parts': {
            'left_arm': [],
            'right_arm': [],
            'back_legs': [],
            'torso': ['turtle shell'],
            'head': ['wolf head', 'panther head'],
            'tail': [],
            'wings': [None],
            'extras' : ['antlers']
        }
    },
    'large': {
        'creatures': {
            'bear': {
                'left_arm': 'bear paws',
                'right_arm': 'bear paws',
                'back_legs': 'bear paws',
                'torso': 'bear torso',
                'head': 'bear head',
                'tail': None,
                'wings': None,
                'extras': None
            },
            'rothe': {
                'left_arm': 'rothe hooves',
                'right_arm': 'rothe hooves',
                'back_legs': 'rothe hooves',
                'torso': 'rothe torso',
                'head': 'rothe head',
                'tail': None,
                'wings': None,
                'extras': None
            },
        },
        'parts': {
            'left_arm': ['panther claw', 'large pincer', 'human hand'],
            'right_arm': ['panther claw', 'large pincer', 'human hand'],
            'back_legs': ['human legs'],
            'torso': [],
            'head': [],
            'tail': [],
            'wings': [None],
            'extras' : ['rhinoceros horn']
        }
    },
    'gargantuan': {
        'creatures': {
            'sandworm': {
                'left_arm': None,
                'right_arm': None,
                'back_legs': None,
                'torso': 'sandworm torso',
                'head': 'sandworm head',
                'tail': None,
                'wings': None,
                'extras': None
            },
            'purple worm': {
                'left_arm': None,
                'right_arm': None,
                'back_legs': None,
                'torso': 'purple worm torso',
                'head': 'purple worm head',
                'tail': None,
                'wings': None,
                'extras': None
            },
        },
        'parts': {
            'left_arm': [],
            'right_arm': [],
            'back_legs': [],
            'torso': [],
            'head': [],
            'tail': ['gargantuan stinger'],
            'wings': ['gargantuan leather wings', 'gargantuan feather wings', 'gargantuan membrane wings'],
            'extras' : []
        }
    }
}

# Generate hybrid creature with cero to two mod
def create_hybrid():
    category = random.choice(list(creatures_by_size.keys()))
    creatures = creatures_by_size[category]['creatures']
    base_creature = random.choice(list(creatures.keys()))
    base_parts = creatures[base_creature].copy()

    num_parts_to_modify = random.randint(0, 2)
    parts_to_modify = random.sample(list(base_parts.keys()), k=num_parts_to_modify)
    for part in parts_to_modify:
        if part in creatures_by_size[category]['parts']:
            base_parts[part] = random.choice(creatures_by_size[category]['parts'][part])

    return base_parts

print(create_hybrid())