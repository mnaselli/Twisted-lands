# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 23:38:49 2024

@author: Matts 
"""
import pygame
import pygame_gui
import random
import json
import copy
pygame.init()
pygame.font.init()
pygame.mixer.init()
# =============================================================================
# CLASSES
# =============================================================================


# =============================================================================
# =============================================================================
# # Slide
# =============================================================================
# =============================================================================


class Slide:
    def __init__(self,slide_id, text_template, category,test = None,city_advancement = None,button_text = None, spell = None,item = None, previous_slide = None, success_slide_id = None, fail_slide_id = None, linked_slide_id=None, is_combat=False,background =None):
        self.slide_id = slide_id
        self.text = text_template
        self.text_template = text_template
        self.category = category 
        self.linked_slide_id = linked_slide_id if linked_slide_id is not None else []
        self.is_combat = is_combat
        self.background = background
        self.previous_slide = previous_slide
        self.city_advancement = city_advancement if city_advancement is not None else 10 #aca despues lo pongo en random
        self.use_spell = spell
        self.use_item = item
        self.button_text = button_text if button_text is not None else ["Move forward"]
        self.test = test
        self.success_slide_id = success_slide_id
        self.fail_slide_id = fail_slide_id

    def is_terminal(self):
        return not self.linked_slide_id and not self.success_slide_id



def getSlidebyID(slide_id):
    for category in slides.values():
        for slide in category:  
            if slide.slide_id == slide_id:  
                return slide  

# =============================================================================
# =============================================================================
# # Body parts
# =============================================================================
# =============================================================================

class BodyPart:
    def __init__(self, name, max_hp, armor, dodge_offset=0, is_vital=False):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.armor = armor
        self.dodge_offset = dodge_offset
        self.conditions = set()
        self.is_vital = is_vital
        self.owner = None

    def take_damage(self, damage):
        effective_damage = max(0, damage - self.armor)
        self.current_hp -= effective_damage
        self.current_hp = max(0, self.current_hp)  # Prevent HP from going negative
        self.update_conditions()
        if self.is_important and self.current_hp == 0:
            return "combat_end"
        return "continue"
    
    def update_conditions(self):
        if self.current_hp == 0:
            self.conditions.add("destroyed")
        elif self.current_hp <= self.max_hp / 2:
            self.conditions.add("damaged")
        else:
            self.conditions.discard("damaged")

    def heal(self, amount):
        if self.current_hp > 0:  # Cannot heal a destroyed body part
            self.current_hp += amount
            self.current_hp = min(self.current_hp, self.max_hp)
            self.update_conditions()

    @property
    def dodge(self):
        if self.owner:
            return self.owner.dodge + self.dodge_offset
        return self.dodge_offset




# =============================================================================
# =============================================================================
# # Character 
# =============================================================================
# =============================================================================


class Character:
    def __init__(self,name,job,strength,agility,lore,faith):
        self.name = name
        self.level = 1
        self.experience = 0
        self.job = job
        self._strength = strength
        self._agility = agility
        self._lore = lore 
        self._faith = faith
        self.endurance = 100
        self.current_endurance = 100
        self.sustenance = 100
        self.current_sustenance = 100
        self.accuracy = 0.75
        self._dodge = 0.4
        self.crit_chance = 0.15
        self.carry_weight_base = 50
# =============================================================================
#         self.armor = 10
# =============================================================================
        self._spell_rating_base = 1
        self._ritual_rating_base = 1
        self.block = 0.1
        self.parry = 0.1
        self.perks = []
        self.spells_known = []
        self.rituals_known = []
        self.body_parts = {
            'Torso': BodyPart('Torso', 100, 5, is_vital=True),
            'Left Arm': BodyPart('Left Arm', 50,3,dodge_offset=0.05),
            'Right Arm': BodyPart('Right Arm', 50, 3,dodge_offset=0.05),
            'Head': BodyPart('Head', 30, 4, is_vital=True,dodge_offset=0.1),
            'Legs': BodyPart('Legs', 80, 4,dodge_offset=0.05)
        }
        # Assign owner to body parts
        for part in self.body_parts.values():
            part.owner = self
# =============================================================================
#         self.head_hp = 20
#         self.current_head_hp = 20
#         self.torso_hp = 50
#         self.current_torso_hp = 50
#         self.rarm_hp = 10
#         self.current_rarm_hp = 10
#         self.larm_hp = 10
#         self.current_larm_hp = 10
#         self.legs_hp = 10
#         self.current_legs_hp = 10
# =============================================================================
        self.initiative = 40
        self.initial_initiative = 0
        self.inventory = []
        self.equipped_weapon = None
        self.available_weapons = []
        self.equipped_armor = None
        
        
        @property
        def dodge(self):
            return self._dodge
        
        @dodge.setter
        def dodge(self, value):
            self._dodge = value


        def take_damage(self, body_part_name, damage):
            if body_part_name in self.body_parts:
                critical_destroyed = self.body_parts[body_part_name].take_damage(damage)
                if critical_destroyed:
                    print(f"Critical body part {body_part_name} destroyed! Critical situation!")
                self.body_parts[body_part_name].update_condition()
            else:
                print(f"No such body part: {body_part_name}")

        
        
    def copy_for_combat(self):
        """Create a deep copy of the character for combat purposes."""
        return copy.deepcopy(self)
    
    def update_after_combat(self, combat_character):
        
        self.current_endurance = combat_character.current_endurance
        self.current_head_hp = combat_character.current_head_hp
        self.current_torso_hp = combat_character.current_torso_hp
        self.current_larm_hp = combat_character.current_larm_hp
        self.current_rarm_hp = combat_character.current_torso_hp
        self.current_legs_hp = combat_character.current_legs_hp
        
    
    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        self._strength = value

    @property
    def agility(self):
        return self._agility

    @agility.setter
    def agility(self, value):
        self._agility = value

    @property
    def lore(self):
        return self._lore

    @lore.setter
    def lore(self, value):
        self._lore = value

    @property
    def faith(self):
        return self._faith

    @faith.setter
    def faith(self, value):
        self._faith = value
    
    
    @property
    def dodge(self):
        return self._dodge + 0.1 * self.agility

    @property
    def carry_weight(self):
        return self._carry_weight_base + self.strength * 5

    @property
    def spell_rating(self):
        return self._spell_rating_base + 0.5 * self.lore

    @property
    def ritual_rating(self):
        return self._ritual_rating_base + 0.5 * self.faith

    def equip_item(self, item):
        # Check if an item of the same type is already equipped and unequip it first
        if item.item_type == 'weapon':
            if self.equipped_weapon:
                self.unequip_item('weapon')
            self.equipped_weapon = item
            self.available_weapons.append(item)
        elif item.item_type == 'armor':
            if self.equipped_armor:
                self.unequip_item('armor')
            self.equipped_armor = item
        
        # Apply the new item's effects
        self.apply_item_effects(item)
    
    def unequip_item(self, item_type):
        # Only try to unequip if there is an item equipped in the slot
        if item_type == 'weapon' and self.equipped_weapon:
            self.remove_item_effects(self.equipped_weapon)
            self.equipped_weapon = None
        elif item_type == 'armor' and self.equipped_armor:
            self.remove_item_effects(self.equipped_armor)
            self.equipped_armor = None
    
    def apply_item_effects(self, item):
        # Apply stat modifiers and special abilities from the item
        for stat, modifier in item.stat_modifiers:
            setattr(self, stat, getattr(self, stat) + modifier)


    def remove_item_effects(self, item):
        # Reverse stat modifiers when an item is unequipped
        for stat, modifier in item.stat_modifiers:
            setattr(self, stat, getattr(self, stat) - modifier)
            

    def get_attack_damage(self, chosen_weapon_name):
        # Search for the weapon by name in available_weapons
        weapon = next((item for item in self.available_weapons if item.name == chosen_weapon_name), None)
        if weapon:
            # Calculate damage using the found weapon's damage range and character's stats
            return random.randint(weapon.min_damage, weapon.max_damage) + max(self._strength, self._agility)
        else:
            # Optionally handle the case where no weapon is found
            return 1 + max(self._strength, self._agility)  # Default damage or consider raising an exception
        
        
        
        
        
        




# =============================================================================
# =============================================================================
# # Creature
# =============================================================================
# =============================================================================

class Creature:
    def __init__(self,name):
        self.name = name
        self.endurance = 100
        self.current_endurance = 100
        self.accuracy = 0.8
        self._dodge = 0.05
        self.crit_chance = 0.30
        self.armor = 10
        self._spell_rating_base = 1
        self.block = 0
        self.parry = 0
        self.perks = []
        self.spells_known = []
        self.head_hp = 20
        self.torso_hp = 50
        self.rarm_hp = 10
        self.larm_hp = 10
        self.legs_hp = 10
        self.inventory = []
        self.initiative = 20
        self.initial_initiative = 0
        self.equipped_weapon = None
        self.equipped_armor = None
#        self.available_actions = [bite_attack,claw_attack]



# =============================================================================
# =============================================================================
# # ITEMS
# =============================================================================
# =============================================================================

class Item:
    def __init__(self, name, item_type, min_damage=None,max_damage=None, stat_modifiers=None, special_abilities=None):
        self.name = name
        self.item_type = item_type
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.stat_modifiers = stat_modifiers if stat_modifiers else []
        self.special_abilities = special_abilities if special_abilities else []

def increase_speed(character):
    character.agility += 1 
def heal(character):
    character.health += 10

def create_item(name):
    # Iterate through each category in the items dictionary
    for category in items.values():
        # Look for the item by name
        for item in category:
            if item.name == name:
                # Found the item, create a new instance and return it
                return Item(item.name, item.item_type, item.min_damage, item.max_damage, item.stat_modifiers, item.special_abilities)
    # If item not found, return None or raise an error
    return None


# =============================================================================
# GAME DEF
# =============================================================================

items = {
    "armor": [
        Item("Boots of Swiftness","armor",stat_modifiers=[("agility", 1)],special_abilities=[increase_speed])
    ],
    "weapon": [
        Item("shortsword","weapon",min_damage = 5,max_damage = 10,stat_modifiers=[("strength",2)]),     
        Item("Axe","weapon",min_damage = 5,max_damage = 14,stat_modifiers=[("strength",2)]),
        Item("Bow","weapon",min_damage = 5,max_damage = 5,stat_modifiers=[("agility",2)]),
        Item("Quarterstaff","weapon",min_damage = 3,max_damage = 8,stat_modifiers=[("strength",2)]) 
    ],
    "consumable": [
        Item("potion","consumable",special_abilities=[heal])
    ] 
    }





slides = {
    "start": [
        Slide("0","","start",is_combat= True),
    ],
    "wild": [
        #Slide("wild1","You're wandering in a dense forest. Birds are chirping.","wild"),
        #Slide("wild2","A clearing in the forest reveals a peaceful river.","wild"),
        Slide("wild3","The path leads you to the edge of a cliff with a breathtaking view.","wild"),
        #Slide("wild4","A clearing in the forest reveals a giant tree.","wild", linked_slide_id=["chainGiantTree1","chainGiantTree2","chainGiantTree3"]),
        #Slide("wild5","You enter the grove. [/color] flowers surround you filling the air with a [/smellqual] aroma of [/smell]. The birds sing, filling you with [/emotion].","wild"),
        Slide("wild6","You are crossing a bridge and it starts to break","wild", success_slide_id=["bridge_success"],fail_slide_id=["bridge_fail1","bridge_fail2"],button_text = ["run fast to the end","take a big jump"],test = ["agility","strength"]),
    ],
    "city": [
        Slide("Saklas","You arrive to the city of Saklas","city",linked_slide_id=["TheTavernavcle","Divineprovidence","Temple"],button_text = ["visit The Tavernavcle","visit Divine providence","visit Temple"],background="city"),
        Slide("Iyao","You arrive to the city of Iyao","city",linked_slide_id=["TheLongRest","ScalpelSteel","Hospital"],button_text = ["visit The Long Rest","visit Scalpel Steel","visit Hospital"],background="city"),
        Slide("Bapth ","You arrive to the city of Bapth ","city",linked_slide_id=["Champion’sFeast","Hero’sArsenal","Granforja"],button_text = ["visit Champion’s Feast","visit Hero’s Arsenal","Gran forja"],background="city"),
    ],
    "chain": [
        Slide("chainGiantTree1","You approach the giant tree and as you blink it dissapears","chain",background = "woodbackground"),
        Slide("chainGiantTree2","You approach the giant tree and as you blink it dissapears22","chain",background = "woodbackground"),
        Slide("chainGiantTree3","You go around the giant tree, and the trunk seems endless","chain",background = "woodbackground")
    ],
    "test": [
        Slide("bridge_success","You reach the other side of the bridge safely","test"),
        Slide("bridge_fail1","You are not fast enough and fall taking X damage","test"),
        Slide("bridge_fail2","Your jump is not long enough and you fall taking X damage","test"),
    ],
    "character": [
        Slide("character_info","","character")
    ],
    "tavern": [
        Slide("TheTavernavcle","Taverna Saklas","tavern",background="city"),
        Slide("TheLongRest","Taverna Iyao","tavern",background="city"),
        Slide("Champion’sFeast","Taverna Bapth","tavern",background="city")
    ],
    "shop": [
        Slide("Divineprovidence","shop Saklas","shop",background="city"),
        Slide("ScalpelSteel","shop Iyao","shop",background="city"),
        Slide("Hero’sArsenal","shop Bapth","shop",background="city")
        ],
    "sp_ed": [
        Slide("Temple","Temple Saklas","sp_ed",background="city"),
        Slide("Hospital","Hospital Iyao","sp_ed",background="city"),
        Slide("Granforja","Gran forja Bapth","sp_ed",background="city")
        ],
    "combat": [
        Slide("combat","","combat")
        ]
}


text_options = {
    "[/color]": ["purple", "red", "yellow", "green", "black", "white", "brown", "orange", "grey", "indigo", "maroon", "golden", "silver", "pink", "azure", "violet", "translucent", "blue", "scarlet", "vermillion", "cherry", "cerulean", "viridescent", "lime", "amber", "beige", "bordeaux", "vinaceus", "burgundy", "colourless", "chalky", "dark", "inky", "ochre", "iridescent", "opalescent", "prismatic"],
    "[/colorqual]": ["pale", "strong", "faint", "spotty", "uniform", "deep", "faded", "shimmering", "oily", "intense", "reflective", "metallic", "shiny", "glossy", "fluorescent", "opaque", "glowing", "vivid"],
    "[/smell]": ["roses", "lavender", "powder", "blood", "metal", "corpses", "rot", "mold", "dirt", "excrement", "ozone", "chemicals", "brine", "fish", "fruit", "carrion", "burning", "sweat", "petrichor"],
    "[/emotionpositive]": ["happiness", "tranquility", "valor", "bravery", "hope", "energy", "satisfaction", "cheerfulness", "courage"],
    "[/emotionnegative]": ["sadness", "fear", "foreboding", "dread", "hopelessness", "fatigue", "despair", "angst", "anger"],
    "[/emotion]": ["dread", "joy", "peace", "excitement", "anxiety"],
    "[/smellqual]": ["faint", "strong", "weak", "barely perceptible", "pungent", "invasive", "notorious"],
}

backgrounds_paths = {
    "default": "background/obsidian.png",
    "forest": "background/woodbackground.png",
    "city": "background/stonebackground.png",
}

# =============================================================================
# CONFIG
# =============================================================================


font = pygame.font.SysFont('Arial', 30)
clock = pygame.time.Clock()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
ui_manager = pygame_gui.UIManager(window_size,"transparent.json")
loaded_backgrounds = {key: pygame.image.load(path).convert() for key, path in backgrounds_paths.items()}


# =============================================================================
# BUTTONS
# =============================================================================


button_wild = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 550), (200, 50)),
                                           text='Wild',
                                           manager=ui_manager)

button_city = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 550), (120, 50)),
                                           text='Visit city',
                                           manager=ui_manager)

# =============================================================================
# =============================================================================
# # CHARACTER BUTTONS
# =============================================================================
# =============================================================================

button_character = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((710, 10), (50, 30)),
                                                text='C',
                                                manager=ui_manager)

button_body_mind = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 300), (150, 50)),
                                           text='BODY AND MIND',
                                           manager=ui_manager)

button_quest = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 360), (120, 50)),
                                           text='QUEST',
                                           manager=ui_manager)

# =============================================================================
# =============================================================================
# # COMBAT BUTTONS
# =============================================================================
# =============================================================================

button_Attack = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 500), (130, 40)),
                                           text='Attack',
                                           manager=ui_manager)
button_Skill = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 500), (130, 40)),
                                           text='Skill',
                                           manager=ui_manager)
button_Spell = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 500), (130, 40)),
                                           text='Spell',
                                           manager=ui_manager)
button_Consumables = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 550), (130, 40)),
                                           text='Consumable',
                                           manager=ui_manager)
button_Status = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 550), (130, 40)),
                                           text='Status',
                                           manager=ui_manager)
button_Escape = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 550), (130, 40)),
                                           text='Escape',
                                           manager=ui_manager)








button_body_mind.hide()
button_quest.hide()
button_wild.hide()
# =============================================================================
# GLOBALS
# =============================================================================

sound_effects = {
    
    "soundcategory1":[pygame.mixer.Sound('sounds/Combat/AxeHit1.mp3'),
                      pygame.mixer.Sound('sounds/Combat/BluntHit1.mp3'),
                      pygame.mixer.Sound('sounds/Combat/StaffHit1.mp3'),
                      pygame.mixer.Sound('sounds/Combat/StaffHit2.mp3')
                     ],
    'AxeHit1': pygame.mixer.Sound('sounds/Combat/AxeHit1.mp3'),
    'BluntHit1': pygame.mixer.Sound('sounds/Combat/BluntHit1.mp3'),
    'StaffHit1': pygame.mixer.Sound('sounds/Combat/StaffHit1.mp3'),
    'StaffHit2': pygame.mixer.Sound('sounds/Combat/StaffHit2.mp3'),
    'UnarmedHit1': pygame.mixer.Sound('sounds/Combat/UnarmedHit1.mp3'),
    'BlockMelee1': pygame.mixer.Sound('sounds/Combat/BlockMelee1.mp3'),
    'BlockMelee2': pygame.mixer.Sound('sounds/Combat/BlockMelee2.mp3'),
    'BlockRaged1': pygame.mixer.Sound('sounds/Combat/BlockRanged1.mp3'),
    'MissMelee1': pygame.mixer.Sound('sounds/Combat/MissMelee1.mp3'),
    'MissRanged1': pygame.mixer.Sound('sounds/Combat/MissRanged1.mp3'),
    'ParryMelee1': pygame.mixer.Sound('sounds/Combat/ParryMelee1.mp3'),
    
}  
 

def set_all_volumes(sound_effects, volume):
    for sound in sound_effects.values():
        if isinstance(sound, list):  # Check if the entry is a list
            for s in sound:
                s.set_volume(volume)
        elif isinstance(sound, pygame.mixer.Sound):  # Check if the entry is a Sound object
            sound.set_volume(volume)

# Set the volume for all sounds to 50%
set_all_volumes(sound_effects, 0.5)

   
current_category = "start"


current_slide = getSlidebyID("0")

city_distance = 0
background_image = loaded_backgrounds.get(current_slide.background, loaded_backgrounds["default"])

button_paths_linked = []
button_paths_ids_linked = []
button_paths_test = []
button_paths_ids_test = []
button_paths_combat = []
button_paths_ids_combat = []

testy = Character("Testycle","Test character",1,1,1,1)
shortsword = create_item("shortsword")
axe = create_item("Axe")
bow = create_item("Bow")
quarterstaff = create_item("Quarterstaff")
testy.equip_item(shortsword)
testy.available_weapons.append(axe)
testy.available_weapons.append(quarterstaff)
creature = Creature("Giant Rat")
character_window_reference = None
current_slide_text = current_slide.text




# =============================================================================
# DEBUG 
# =============================================================================

is_debug_mode = False
debug_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 10), (140, 30)), manager=ui_manager, visible=0)
debug_input.set_text('Enter var name')


def toggle_debug_mode():
    global is_debug_mode
    is_debug_mode = not is_debug_mode
    if is_debug_mode:
        debug_input.show()
    else:
        debug_input.hide()

# =============================================================================
# FUNCIONES
# =============================================================================


def play_random_sound(category):
    if category in sound_effects:
        sound_to_play = random.choice(sound_effects[category])
        sound_to_play.play()
    else:
        print(f"No such category: {category}")


def generate_dynamic_text(template_text, options_dict):
    for placeholder, choices in options_dict.items():
        if placeholder in template_text:
            template_text = template_text.replace(placeholder, random.choice(choices), 1)
    return template_text

def draw_box_with_border(window, text, box_config, font_path="UglyQua.ttf"):
    font_size = box_config.get("font_size", 24)
    font = pygame.font.Font(font_path, font_size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_width, text_height = text_surface.get_size()

    padding = 10  # Adjust the padding around the text
    box_width = text_width + 2 * padding
    box_height = text_height + 2 * padding
    position = box_config["position"]

    # Create and fill the box surface
    box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    box_surface.fill(box_config["box_color"])

    # Draw the text onto the box surface
    box_surface.blit(text_surface, (padding, padding))

    # Draw the border
    pygame.draw.rect(box_surface, box_config["border_color"], (0, 0, box_width, box_height), box_config["border_thickness"])

    # Blit the box surface onto the main window
    window.blit(box_surface, position)

def display_character_info(character):
    
    button_wild.hide()
    button_city.hide()
    button_body_mind.show()
    button_quest.show()
    
    for btn in button_paths_linked + button_paths_test:
        btn.hide()
    
    
    
    with open("boxes_config.json", "r") as file:
        boxes_config = json.load(file)["boxes"]
        
    texts= [f"{character.name}  Level: {character.level} {character.job}",
            f"ATTRIBUTES \n Strength: {character.strength} \n Agility: {character.agility} \n Lore: {character.lore} \n Faith: {character.faith}",
            f"SECONDARY \n Accuracy: {character.accuracy} \n Dodge: {character._dodge} \n Crit chance: {character.crit_chance} \n Weight: 0 / {character.carry_weight_base} \n Armor  \n Block: {character.block} \n Parry: {character.parry} \n Dodge: {character.armor} \n Spell Skill: {character._spell_rating_base} \n Ritual Skill: {character._ritual_rating_base}" ,
            f"SURVIVAL \n Endurance: {character.current_endurance}/{character.endurance} \n Sustenance: {character.current_sustenance}/{character.sustenance} \n Corruption: ph/ph"
            ]
    
    for text, box in zip(texts, boxes_config):
        draw_box_with_border(window, text, box)


def basic_attack(character,creature,chosen_weapon):

     damage = character.get_attack_damage(chosen_weapon)
     return damage

 
def basic_attack2(character,creature):
    weapon_chosen = None
    while weapon_chosen is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

def clean_combat_buttons():
    global button_paths_combat, button_paths_ids_combat
    for btn in button_paths_combat:
        btn.kill()
    button_paths_combat.clear()
    button_paths_ids_combat.clear()
    bg_middle = pygame.transform.scale(loaded_backgrounds["default"], (800/3, 390))
    window.blit(bg_middle, (800/3, 60))
    

def choose_weapon(ui_manager,window,character):
    global button_paths_combat, button_paths_ids_combat
    clock = pygame.time.Clock()  # Ensure you have a clock to manage updates

    if button_paths_combat:
        clean_combat_buttons()
    for index, weapon in enumerate(character.available_weapons):
        btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 100 + index * 60), (200, 50)),
            text=weapon.name,
            manager=ui_manager    
        )
        button_paths_combat.append(btn)
        button_paths_ids_combat.append((weapon.name, index))

    weapon_chosen = None
    while weapon_chosen is None:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in button_paths_combat:
                    index = button_paths_combat.index(event.ui_element)
                    weapon_chosen = button_paths_ids_combat[index][0]
                    clean_combat_buttons()
                    break

            ui_manager.process_events(event)
        
        ui_manager.update(time_delta)
        ui_manager.draw_ui(window)
        pygame.display.update()

    # Clean up buttons after choice
    clean_combat_buttons()
    return weapon_chosen




def claw_attack(character,creature):
    damage = random.randint(4, 8)
   # character.current_endurance = character.current_endurance - damage
    return damage

def combat_background(ui_manager,window):
    window_width, window_height = 800, 600
    # Calculate the height for each section
    top_height = window_height // 10  # Change this to adjust the size of the top section
    bottom_height = window_height // 4  # Change this to adjust the size of the bottom section
    middle_height = window_height - (top_height + bottom_height)
    
    # Create surfaces for the top and bottom sections
    top_surface = pygame.Surface((window_width, top_height))
    bottom_surface = pygame.Surface((window_width, bottom_height))
    
    # Fill the top and bottom surfaces with black
    top_surface.fill((0, 0, 0))
    bottom_surface.fill((0, 0, 0))
    
    # Load and scale the middle section image
    bg_middle = pygame.transform.scale(loaded_backgrounds["default"], (window_width, middle_height))
    
    # Blit the top, middle, and bottom sections onto the window
    window.blit(top_surface, (0, 0))  # Top section at the top of the window
    window.blit(bg_middle, (0, top_height))  # Middle section below the top section
    window.blit(bottom_surface, (0, top_height + middle_height))  # Bottom section below the middle section


def wait_for_player_action(ui_manager,window,character,creature):
    action = None

    # Event loop to wait for player's action
    while action is None:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            
            # You would have defined your combat action buttons earlier and passed them here
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_Attack:
                    chosen_weapon = choose_weapon(ui_manager,window,character)
                    action = 'attack'

            # Pass the event to the UIManager
            ui_manager.process_events(event)

        # Update the UI manager and draw the UI
        ui_manager.update(time_delta)  # time_delta is the time since the last loop
        ui_manager.draw_ui(window)  # window_surface is your main display surface

        # Update the display
        pygame.display.update()

        clock.tick(60)

    return action,chosen_weapon

def process_character_action(character_action,chosen_weapon,character,creture,left_info_box,right_info_box,character_turn_number):
    if character_action == "attack":
        damage = basic_attack(character, creature,chosen_weapon)
        flag = dodge_block_parry(character, creature)
        text = f"Turn {character_turn_number}                "
        if flag == "dodged":
            damage = 0
            text += "\n Your attack misses the Creature, dealing no damage!"
            sound_effects['MissMelee1'].play()
        elif flag == "blocked":
            damage_blocked = 0.5*damage
            damage = damage*0.5
            text += f"\n Your attack was blocked, dealing {damage}! ({damage_blocked} damage lost)"
            sound_effects['BlockMelee1'].play()
        elif flag == "parried":
            damage_parried = damage*0.25
            damage = damage*0.75
            text += f"\n Your attack was parried, dealing {damage}! ({damage_parried} damage lost)" 
        else:
            text += f"\n Your {chosen_weapon} hits the Creature for {damage} damage"
            if chosen_weapon == "Axe":
                sound_effects['AxeHit1'].play()
            elif chosen_weapon == "Quarterstaff":
                sound_effects['StaffHit2'].play()
        
        
        creature.endurance = creature.endurance - damage
        left_info_box = update_combat_text(left_info_box, text)
        return left_info_box

def process_creature_action(creature_action,character,creture,left_info_box,right_info_box,creature_turn_number):
    damage = claw_attack(character, creature)
    flag = dodge_block_parry(character, creature)
    text = f"Turn {creature_turn_number}                "
    if flag == "dodged":
        damage = 0
        text += "\n The Creature lounges, but you manage to dodge!"
    elif flag == "blocked":
        damage_blocked = 0.5*damage
        damage = damage*0.5
        text += f"\n You block the Creature attack, receiveing {damage} ({damage_blocked} damage mitigated)"
    elif flag == "parried":
        damage_parried = damage*0.25
        damage = damage*0.75
        text += f"\n You parry the Creature attack, receiveing {damage} ({damage_parried} gets mitigated)" 
    else:
        text += f"\n The Creature strikes you for {damage} damage"
        
        
    character.current_endurance = character.current_endurance - damage
    right_info_box = update_combat_text(right_info_box, text)
    return right_info_box

def combat_loop(ui_manager,window,character,creature,left_info_box,right_info_box):
    character_turn = False
    creature_turn = False
    character_turn_number = 0
    creature_turn_number = 0

    while character.current_endurance>0 and creature.endurance>0:
        # Increase both character and creature's initial initiative
        character.initial_initiative += character.initiative
        creature.initial_initiative += creature.initiative

        # Check if the character or creature has reached or exceeded 100 initiative
        if character.initial_initiative >= 100:
            character_turn = True
            character.initial_initiative -= 100
        if creature.initial_initiative >= 100:
            creature_turn = True
            creature.initial_initiative -= 100

        # Handle the character's turn
        if character_turn:
            character_turn_number += 1
            character_action,chosen_weapon = wait_for_player_action(ui_manager,window,character,creature)  # Function to wait for player to press a button
            left_info_box = process_character_action(character_action,chosen_weapon, character, creature,left_info_box,right_info_box,character_turn_number)
            character_turn = False  # Reset the flag after the character's turn is processed

        # Handle the creature's turn
        if creature_turn:
            #creature_action = decide_creature_action(creature)  #function to decide the creature's action
            creature_turn_number += 1
            right_info_box = process_creature_action(None, character, creature,left_info_box,right_info_box,creature_turn_number)
            creature_turn = False  # Reset the flag after the creature's turn is processed
        
        window.blit(left_info_box, (0, 60))
        window.blit(right_info_box, (800*2/3, 60))
        display_combat_character(ui_manager,window,character,(20,450))

        # Check for end of combat (e.g., one of the participants' health reaches 0)
        if character.current_endurance <= 0 or creature.endurance <= 0:
            break

        # Optionally, wait for a short moment before the next loop iteration
        pygame.time.delay(100)

    # loot,cambiar slide, rewards, etc
    return

def init_combat_ui(window):
    # Get the size of the window surface
    # Create and return surfaces for left and right info boxes
    left_box_surface = pygame.Surface((800 // 3, 390), pygame.SRCALPHA)
    right_box_surface = pygame.Surface((800 // 3, 390), pygame.SRCALPHA)
    
    # Fill surfaces with a translucent color
    left_box_surface.fill((0, 0, 0, 128))  # semi-transparent black
    right_box_surface.fill((0, 0, 0, 128))
    
    return left_box_surface, right_box_surface


def display_combat_character(ui_manager,window,character,position,font_path ="UglyQua.ttf" ):
    info_texts = [
        f"Endurance: {character.current_endurance}/{character.endurance}",
        f"Head: {character.body_parts['Head'].current_hp}/{character.body_parts['Head'].max_hp}  Torso: {character.body_parts['Torso'].current_hp}/{character.body_parts['Torso'].max_hp}",
        f"L. Arm: {character.body_parts['Left Arm'].current_hp}/{character.body_parts['Left Arm'].max_hp}  R. Arm: {character.body_parts['Right Arm'].current_hp}/{character.body_parts['Right Arm'].max_hp}  Legs: {character.body_parts['Legs'].current_hp}/{character.body_parts['Legs'].max_hp}"
    ]
    font = pygame.font.Font(font_path, 17)
    # Calculate the position and size for the info box
    info_box_height = len(info_texts) * (font.get_height() + 5) + 20
    info_box_width = 300  # Adjust the width as needed
    info_box_rect = pygame.Rect(position, (info_box_width, info_box_height))

    # Draw the info box background
    pygame.draw.rect(window, (0, 0, 0, 0), info_box_rect)

    # Set the starting Y position for the first line of text
    text_pos_y = position[1] + 5

    # Iterate over each info text line
    for info_text in info_texts:
        # Determine the color based on the character's status
        text_color = (128, 128, 128)  # Default color grey
        if "Endurance" in info_text:
            font = pygame.font.Font(font_path, 30)
            text_surface = font.render(info_text, True, text_color)
    
            # Draw the text on the window
            window.blit(text_surface, (position[0] + 5, text_pos_y))
    
            # Move down for the next line of text
            text_pos_y += font.get_height() + 5
        else:
            font = pygame.font.Font(font_path, 17)
            if "Head" in info_text and character.body_parts['Head'].current_hp < 10:  # Example condition
                text_color = (255, 0, 0)  # Red color for low health
    
            # Render the text
            text_surface = font.render(info_text, True, text_color)
    
            # Draw the text on the window
            window.blit(text_surface, (position[0] + 5, text_pos_y))
    
            # Move down for the next line of text
            text_pos_y += font.get_height() + 5
    
    font = pygame.font.Font(font_path, 30)
    character_text = f"{character.name}- Level:{character.level} {character.job}"
    text_surface = font.render(character_text, True, (128, 128, 128))
    text_width, text_height = text_surface.get_size()
    box_x, box_y = 400-(text_width/2), 410
    box_width, box_height = text_width + 2, text_height + 2
    character_box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(window, (0, 0, 0), character_box_rect)
    window.blit(text_surface, (box_x, box_y))
    
    font = pygame.font.Font(font_path, 30)
    creature_text = f"Endurance:{creature.endurance}"
    text_surface = font.render(creature_text, True, (128, 128, 128))
    text_width, text_height = text_surface.get_size()
    box_x, box_y = 10, 10
    box_width, box_height = text_width + 15, text_height + 2
    creature_box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(window, (0, 0, 0), creature_box_rect)
    window.blit(text_surface, (box_x, box_y))
    
    font = pygame.font.Font(font_path, 30)
    creature_text = f"{creature.name}"
    text_surface = font.render(creature_text, True, (128, 128, 128))
    text_width, text_height = text_surface.get_size()
    box_x, box_y = 400-(text_width/2), 50
    box_width, box_height = text_width + 2, text_height + 2
    creature_box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(window, (0, 0, 0), creature_box_rect)
    window.blit(text_surface, (box_x, box_y))
    
    
    
    border_color = (0, 0, 0,0) #no border
    pygame.draw.rect(window,border_color, info_box_rect, 2)

def combat_screen(ui_manager,window,character,creature,font_path="UglyQua.ttf"):
        
    character_info_position = (20,450)
    combat_background(ui_manager,window)
    display_combat_character(ui_manager,window,character,character_info_position)

def dodge_block_parry(attacker,defender):
    flag = None
    if random.random() > attacker.accuracy - defender._dodge:
        flag = "dodged"
    elif random.random() < defender.block:
        flag = "blocked"
    elif random.random() < defender.parry:
        flag = "parried"
    return flag
    
def update_combat_text(surface, text, clear_surface=True):
    if clear_surface:
        surface.fill((0, 0, 0, 255))
        window.blit(surface, (0, 60))
        # Clear the previous text by filling the surface with the same translucent color
        new_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        new_surface.fill((0, 0, 0, 128))
    else:
        new_surface = surface
    blit_text(new_surface, text, (10, 10), (255, 255, 255)) 
    return new_surface
    
# =============================================================================
#  TESTS   
# =============================================================================
def agility_test(character):
    return random.choice([True, False])

def strength_test(character):
    return random.choice([True, False])


# =============================================================================
# # =============================================================================
# # SLIDES
# # =============================================================================
# =============================================================================
def render_slide(window, text):
    text_lines = []  # List to hold each line of text
    words = text.split(' ')  # Split the text into words
    line = ""  # Current line being assembled
    for word in words:
        test_line = f"{line} {word}".strip()  
        # Check if this line's width exceeds a certain limit
        if font.size(test_line)[0] > 760:
            text_lines.append(line)  # Save the previous line
            line = word  # Start a new line with the current word
        else:
            line = test_line
    text_lines.append(line)  # Add the last line

    # Render and blit each line
    y_offset = 20  # Starting Y offset for text rendering
    for line in text_lines:
        line_surface = font.render(line, True, (255, 255, 255))
        window.blit(line_surface, (20, y_offset))
        y_offset += font.get_linesize()  # Move down for the next line
        
def blit_text(surface, text, pos, color):
    font = pygame.font.Font("UglyQua.ttf", 24)
    words = text.split(' ')
    space = font.size(' ')[0]
    x, y = pos
    for word in words:
        word_surface = font.render(word, True, color)
        word_width, word_height = word_surface.get_size()
        if x + word_width >= surface.get_width():
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
        surface.blit(word_surface, (x, y))
        x += word_width + space
    if x < surface.get_width():
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.        

def select_random_slide(category):   
    global current_slide
    if category in slides:
        current_slide = random.choice(slides[category])  
# =============================================================================
# # =============================================================================
# # BUTTONS
# # =============================================================================
# =============================================================================


def on_category_button_click(category):
    
    global current_slide,current_category
    
    current_category = category
    select_random_slide(category)

def on_character_button_click():
    global current_slide
    if current_slide.slide_id != "character_info":
        # Save the current slide as the previous slide of the character info slide
        character_slide = getSlidebyID("character_info")
        character_slide.previous_slide = current_slide.slide_id
        current_slide = character_slide
        update_path_buttons(current_slide, ui_manager)
    elif current_slide.previous_slide is not None:
        # Go back to the previous slide
        button_body_mind.hide()
        button_quest.hide()
        current_slide = getSlidebyID(current_slide.previous_slide)
        if button_paths_linked or button_paths_test :
            for btn in button_paths_linked + button_paths_test:
                btn.show()


def update_path_buttons(slide, ui_manager):
    
    global button_paths_linked, button_paths_ids_linked,button_paths_test, button_paths_ids_test
    if slide.is_terminal():
        button_wild.show()
    else:
        button_wild.hide()
        
    if slide.is_terminal() and city_distance >= 100:
        button_city.show()
    else:
        button_city.hide()
    
    for btn in button_paths_linked + button_paths_test:
        btn.kill()
    button_paths_linked.clear()
    button_paths_ids_linked.clear()
    button_paths_test.clear()
    button_paths_ids_test.clear()
# =============================================================================
#   linked slide
# =============================================================================
    
    if not slide.is_terminal() and slide.linked_slide_id:
    # Assuming slide.linked_slide_id is a list of slide IDs for next possible slides
        for index, slide_id in enumerate(slide.linked_slide_id):
            button_text = slide.button_text[index] if index < len(slide.button_text) else "Option"
            # Modified positioning to include a gap between buttons
            btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((100 + index * (210 + 10), 500), (200, 50)),
                text=button_text,
                manager=ui_manager
            )
            button_paths_linked.append(btn)
            button_paths_ids_linked.append(slide_id)

# =============================================================================
#   test slides
# =============================================================================
    
    test_functions = [agility_test, strength_test]  # List of test functions
    if slide.test:
        # Handle test slide button creation with specific outcomes
        for index, test_action in enumerate(slide.button_text):
            btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((100, 100 + index * 60), (200, 50)),
                text=test_action,
                manager=ui_manager
            )
            button_paths_test.append(btn)
            # Store the test function along with the index
            button_paths_ids_test.append((test_functions[index], index))
            
            
    
# =============================================================================
# LOOP
# =============================================================================

running = True
button_city.hide()


while running:
    time_delta = clock.tick(60)/1000.0
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
    
    
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
            toggle_debug_mode()
        
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_element == debug_input:
            var_name = event.text  # Get the entered text
            if var_name and var_name != "Enter var name":  # Validate the input
                try:
                    var_value = eval(var_name, globals(), locals())
                    print(f"{var_name}: {var_value}")  # Print or display the value
                except Exception as e:
                    print(f"Error: {str(e)}")

            # =============================================================================
             # terminal slide loop             
            # =============================================================================
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button_wild:
                select_random_slide("wild")
                update_path_buttons(current_slide, ui_manager) 
                city_distance += current_slide.city_advancement


            elif event.ui_element == button_city:
                select_random_slide("city")
                update_path_buttons(current_slide, ui_manager)
                city_distance = 0
            # =============================================================================
             # linked loop             
            # =============================================================================
            
            elif event.ui_element in button_paths_linked:
                index = button_paths_linked.index(event.ui_element)
                linked_slide_id = button_paths_ids_linked[index]
                current_slide = getSlidebyID(linked_slide_id)
                update_path_buttons(current_slide, ui_manager)  # Update buttons for the new slide
                city_distance += current_slide.city_advancement
            # =============================================================================
             # test loop             
            # =============================================================================
            elif event.ui_element in button_paths_test:
                index = button_paths_test.index(event.ui_element)
                test_function, action_index = button_paths_ids_test[index]
            
                # Call the test function
                test_passed = test_function(testy)
                if test_passed:
                    next_slide_id = current_slide.success_slide_id[0]  # Navigate to success slide
                else:
                    next_slide_id = current_slide.fail_slide_id[action_index]  # Navigate to specific fail slide
        
                current_slide = getSlidebyID(next_slide_id)
                
                update_path_buttons(current_slide, ui_manager)
                city_distance += current_slide.city_advancement
             # =============================================================================
             # character         
             # =============================================================================       
             
            elif event.ui_element == button_character:
                on_character_button_click()
            
            
            
            current_slide_text = current_slide.text
            update_path_buttons(current_slide, ui_manager)
            
            
            # =============================================================================
            # DEBUG         
            # =============================================================================              
    
            
    if is_debug_mode:
        var_name = debug_input.get_text()
        if var_name and var_name != "Enter var name":  # Check if input is not placeholder or empty
            try:
                # Dynamically get the value of the variable
                var_value = eval(var_name, globals(), locals())  # Use globals() and locals() for safety
                debug_text = f"{var_name}: {var_value}"
                font = pygame.font.SysFont("Arial", 24)
                debug_surf = font.render(debug_text, True, (255, 255, 255))
                window.blit(debug_surf, (10, 50))
            except Exception as e:  # Catch any error
                debug_text = f"Error: {str(e)}"
                font = pygame.font.SysFont("Arial", 24)
                debug_surf = font.render(debug_text, True, (255, 255, 255))
                window.blit(debug_surf, (10, 50))


    
# =============================================================================
# COMBAT LOOP
# =============================================================================
    # If you need to check for a linked slide or a fight
    if not current_slide.is_combat :
        if current_slide.background and current_slide.background in loaded_backgrounds:
            background_image = loaded_backgrounds[current_slide.background]
        else:
            background_image = loaded_backgrounds["default"]
        window.blit(background_image, (0, 0))
    else:
        button_wild.hide()
        button_city.hide()
        button_character.hide()
        for btn in button_paths_linked + button_paths_test:
            btn.kill()
        combat_screen(ui_manager, window,testy,creature)
        left_info_box, right_info_box = init_combat_ui(window)
        window.blit(left_info_box, (0, 60))
        window.blit(right_info_box, (2 * 800 // 3, 60))
        combat_loop(ui_manager, window, testy, creature,left_info_box,right_info_box)
    
    if current_slide.category == "character":
        display_character_info(testy)
    else:
        render_slide(window, current_slide_text)
    
    # Process UI events and update the UI elements
    ui_manager.process_events(event)
    ui_manager.update(time_delta)
    ui_manager.draw_ui(window)
    
    # Update the display
    pygame.display.update()

pygame.quit()


















