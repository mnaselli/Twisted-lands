# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 23:38:49 2024

@author: Matts 
"""
import pygame
import pygame_gui
import random
import json
import math
from Classes import BodyPart,Spell,Character,Creature,CreatureAction
from GameDefinitions import slides,items,backgrounds_paths,sound_effects
#import Creature_randomizer
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




# =============================================================================
# GAME DEF
# =============================================================================
def getSlidebyID(slide_id):
    for category in slides.values():
        for slide in category:  
            if slide.slide_id == slide_id:  
                return slide  
            
def increase_speed(character):
    character.agility += 1 
def heal(character):
    character.health += 10
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
base_creatures = []
last_weapon_used = None





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

# =============================================================================
# =============================================================================
# # creature effects
# =============================================================================
# =============================================================================

def calc_modifier_creature(character,creature,extra = 0):
     modifier = 1 - extra
     if creature.iscursed:
        modifier - 0.2         
     return modifier

def creature_tail_attack(target,creature,min_damage = 5,max_damage = 10, multiplier = 1):
    damage = random.randint(min_damage, max_damage)
    flag = dodge_block_parry(creature,target)
    text = ""
    if flag == "dodged":
        damage = 0
        text += f"	The {creature.name} attacks your {target.name} with its tail, but you manage to dodge!"
    elif flag == "blocked":
        damage_blocked = int(0.5*damage)
        damage = damage*0.5
        damage = int(damage-target.armor)
        if last_weapon_used:
            damage -=- last_weapon_used.armor
        text += f"	You block the {creature.name} tail's attack to your {target.name}, receiveing {damage} ({damage_blocked} damage mitigated)(reduced {target.armor} damage by your armor)"
    elif flag == "parried":
        damage_parried = int(damage*0.25)
        damage = damage*0.75
        damage = int(damage-target.armor)
        if last_weapon_used:
            damage -=- last_weapon_used.armor
        text += f"	You parry the {creature.name} tail's attack to your {target.name}, receiveing {damage} ({damage_parried} gets mitigated)(reduced {target.armor} damage by your armor) "
    else:
        damage = int(damage-target.armor)
        if last_weapon_used:
            damage -=- last_weapon_used.armor
        text += f"	The {creature.name} strikes your {target.name} with its tail for {damage} damage(reduced {target.armor} damage by your armor)"
        
        
    target.current_hp -= damage
    target.owner.current_endurance -= damage
    return text
    
def creature_claw_attack(target,creature,min_damage = 2,max_damage = 5, multiplier = 1):
    damage = damage = random.randint(min_damage, max_damage)
    flag = dodge_block_parry(creature,target)
    text = ""
    if flag == "dodged":
        damage = 0
        text += f"	The {creature.name} attacks your {target.name} with its claw, but you manage to dodge!"
    elif flag == "blocked":
        damage_blocked = int(0.5*damage)
        damage = damage*0.5
        damage = int(damage-target.armor)
        if last_weapon_used:
            damage -=- last_weapon_used.armor
        text += f"	You block the {creature.name} claw's attack to your {target.name}, receiveing {damage} ({damage_blocked} damage mitigated)(reduced {target.armor} damage by your armor)"
    elif flag == "parried":
        damage_parried = int(damage*0.25)
        damage = damage*0.75
        #damage = calc_modifier_creature(target,creature,extra = 0.25)
        damage = int(damage-target.armor)
        if last_weapon_used:
            damage -=- last_weapon_used.armor
        text += f"	You parry the {creature.name} claw's attack to your {target.name}, receiveing {damage} ({damage_parried} gets mitigated)(reduced {target.armor} damage by your armor)" 
    else:
        damage = int(damage-target.armor)
        if last_weapon_used:
            damage -=- last_weapon_used.armor
        text += f"	The {creature.name} strikes your {target.name} with its claw for {damage} damage(reduced {target.armor} damage by your armor) "
          
    target.current_hp = target.current_hp - damage
    target.owner.current_endurance -= damage
    return text


def creature_swipe(target,creature,min_damage = 2,max_damage = 5, multiplier = 1):
    damage = damage = random.randint(min_damage, max_damage)
    #flag = dodge_block_parry(target, creature)
    text = ""
    text += f"	The {creature.name} swipes at you with its claws for {damage} damage"
    for body_part in target.get_all_body_parts():
        body_part.current_hp -= damage
    target.current_endurance -= damage
    return text

# =============================================================================
# =============================================================================
# # spell effects
# =============================================================================
# =============================================================================

def spell_fireball(target,character,spell_level,multiplier = 1):
    damage = 0
    text = ""
    match spell_level:
        case 1:
            damage = random.randint(4, 6)
            target.current_hp -= damage
            target.owner.current_endurance -= damage
            text = f"	Your fireball deals {damage} damage to {target.owner.name} {target.name}"
        case 2:
            damage = random.randint(6, 8)
            target.current_hp -= damage
            target.owner.current_endurance -= damage
            text = f"	Your fireball deals {damage} damage to {target.owner.name} {target.name}"
        case 3:
            damage = random.randint(12, 16)
            target.current_hp -= damage
            target.owner.current_endurance -= damage
            aoe_damage = math.ceil(damage/10)
            text = f"	Your fireball deals {damage} damage to {target.owner.name} {target.name}"
            if random.random() < 0.3:
                
                for body_part in target.owner.get_other_body_parts(target.name):
                    body_part.current_hp -= aoe_damage
                text = text + f"	and {aoe_damage} damage to all other body parts"
        case 4:
            damage = random.randint(16, 20)
            target.current_hp -= damage
            target.owner.current_endurance -= damage
            aoe_damage = math.ceil(damage/10)
            text = f"	Your fireball deals {damage} damage to {target.owner.name} {target.name}"
            if random.random() < 0.4:
                
                for body_part in target.owner.get_other_body_parts(target.name):
                    body_part.current_hp -= aoe_damage 
                text = text + f"	and {aoe_damage} damage to all other body parts"
        case 5:
            damage = random.randint(22, 30)
            target.current_hp -= damage
            target.owner.current_endurance -= damage
            aoe_damage = math.ceil(damage/10)
            text = f"	Your fireball deals {damage} damage to {target.owner.name} {target.name}"
            if random.random() < 0.5:
                
                for body_part in target.owner.get_other_body_parts(target.name):
                    body_part.current_hp -= aoe_damage
                text = text + f" and {aoe_damage} damage to all other body parts"                     
        case 0:
            damage = 1
            target.current_hp -= damage
            target.owner.current_endurance -= damage
            text = f"	Your fireball deals {damage} damage to {target.owner.name} {target.name}"
    
    return text


def spell_fissure(target,character,spell_level,multiplier = 1):
    damage = 0
    text = ""
    match spell_level:
        case 1:
            damage = random.randint(3, 4)
            damage = damage * multiplier
            text = f"	Your fissure deals {damage} damage to {target.name} body parts"
            for body_part in target.get_all_body_parts():
                body_part.current_hp -= damage
            target.current_endurance -= damage
            
        case 2:
            damage = random.randint(4, 5)
            damage = damage * multiplier
            text = f"	Your fissure deals {damage} damage to {target.name} body parts"
            for body_part in target.get_all_body_parts():
                body_part.current_hp -= damage
            target.current_endurance -= damage
        case 3:
            damage = random.randint(6, 8)
            damage = damage * multiplier
            text = f"	Your fissure deals {damage} damage to {target.name} body parts"
            for body_part in target.get_all_body_parts():
                body_part.current_hp -= damage
            
            target.current_endurance -= damage
            if random.random() < 0.2:
                target.conditions.add(("burn",3,character.level))
                text = text + " and burns them"
        case 4:
            damage = random.randint(8, 10)
            damage = damage * multiplier
            text = f"	Your fissure deals {damage} damage to {target.name} body parts"
            for body_part in target.get_all_body_parts():
                body_part.current_hp -= damage
            target.current_endurance -= damage
            if random.random() < 0.3:
                target.conditions.add(("burn",3,character.level))
                text = text + " and burns them"
        case 5:
            damage = random.randint(11, 15)
            damage = damage * multiplier
            text = f"	Your fissure deals {damage} damage to {target.name} body parts"
            for body_part in target.get_all_body_parts():
                body_part.current_hp -= damage
            target.current_endurance -= damage
            if random.random() < 0.4:
                target.conditions.add(("burn",3,character.level))
                text = text + " and burns them"                    
        case 0:
            damage = 1
            damage = damage * multiplier
            text = f"	Your fissure deals {damage} damage to {target.name} body parts"
            for body_part in target.get_all_body_parts():
                body_part.current_hp -= damage
            target.owner.current_endurance -= damage
    
    return text
    
# =============================================================================
# =============================================================================
# # SKILLS 
# =============================================================================
# =============================================================================

def skill_wallop(target,character,spell_level,multiplier = 1):
    damage = character.get_attack_damage(last_weapon_used)
    text = ""
    match spell_level:
        case 1:
            damage = math.ceil(damage * 0.6)
            target.current_hp -= damage
            target.owner.current_endurance -= damage
            text = f"	Your wallop deals {damage} damage to {target.owner.name} {target.name}"
            if random.random() < 0.5:
                text += "and blind them"
                target.owner.conditions.add(("blind",1))

        case 2:
            damage = math.ceil(damage * 0.7)
            target.current_hp -= damage
            target.owner.current_endurance -= damage
            text = f"	Your wallop deals {damage} damage to {target.owner.name} {target.name}"
            if random.random() < 0.5:
                text += "and blind them"
                target.owner.conditions.add(("blind",1))
        case 3:
            damage = math.ceil(damage * 0.8)
            target.current_hp -= damage
            target.owner.current_endurance -= damage
            text = f"	Your wallop deals {damage} damage to {target.owner.name} {target.name}"
            if random.random() < 0.65:
                text += "and blind them"
                target.owner.conditions.add(("blind",1))
        case 4:
            damage = math.ceil(damage * 0.9)
            target.current_hp -= damage
            target.owner.current_endurance -= damage
            text = f"	Your wallop deals {damage} damage to {target.owner.name} {target.name}"
            if random.random() < 0.65:
                text += "and blind them"
                target.owner.conditions.add(("blind",1))
        case 5:
            target.current_hp -= damage
            target.owner.current_endurance -= damage
            text = f"	Your wallop deals {damage} damage to {target.owner.name} {target.name}"
            if random.random() < 0.65:
                text += "and blind them"
                target.owner.conditions.add(("blind",1))               
        case 0:
            damage = 1
            target.current_hp -= damage
            text = f"	Your wallop deals {damage} damage to {target.owner.name} {target.name}"
            if random.random() < 0.5:
                text += "and blind them"
                target.owner.conditions.add(("blind",1))

    return text




# =============================================================================
# =============================================================================
# # others
# =============================================================================
# =============================================================================

def create_item(name):
    # Iterate through each category in the items dictionary
    for category in items.values():
        # Look for the item by name
        for item in category:
            if item.name == name:
                if item.item_type == "weapon":
                    return item
                # Found the item, create a new instance and return it
                return item#Item(item.name, item.item_type,item.weight_type, item.min_damage, item.max_damage, item.stat_modifiers, item.special_abilities)
    # If item not found, return None or raise an error
    return None



def play_random_sound(category):
    if category in sound_effects:
        sound_to_play = random.choice(sound_effects[category])
        sound_to_play.play()


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

def create_hybrid_creature():
    creature_parts = ['front_legs', 'back_legs', 'torso', 'head', 'tail', 'wings']
    hybrid_creature = {}
    
    for part in creature_parts:
        selected_creature = random.choice(list(base_creatures.keys()))
        hybrid_creature[part] = base_creatures[selected_creature].get(part, 'None')
    
    return hybrid_creature

def clean_combat_buttons():
    global button_paths_combat, button_paths_ids_combat
    for btn in button_paths_combat:
        btn.kill()
    button_paths_combat.clear()
    button_paths_ids_combat.clear()
    bg_middle = pygame.transform.scale(loaded_backgrounds["default"], (800/3, 390))
    window.blit(bg_middle, (800/3, 60))
    

def choose_weapon(ui_manager,window,character,filtered_weapons = None):
    global button_paths_combat, button_paths_ids_combat
    clock = pygame.time.Clock()  # Ensure you have a clock to manage updates

    if button_paths_combat:
        clean_combat_buttons()
    
    if filtered_weapons:
        for index, weapon in enumerate(filtered_weapons):
            btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((300, 100 + index * 60), (200, 50)),
                text=weapon.name,
                manager=ui_manager    
            )
            button_paths_combat.append(btn)
            button_paths_ids_combat.append((weapon, index))
    elif filtered_weapons != []:        
        for index, weapon in enumerate(character.available_weapons):
            btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((300, 100 + index * 60), (200, 50)),
                text=weapon.name,
                manager=ui_manager    
            )
            button_paths_combat.append(btn)
            button_paths_ids_combat.append((weapon, index))

    weapon_chosen = None
    while weapon_chosen is None:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for i, button in enumerate(button_paths_combat):
                    if event.ui_element == button:
                        weapon_chosen,index = button_paths_ids_combat[i]  # Retrieve the BodyPart instance
                        clean_combat_buttons()
                        break

            ui_manager.process_events(event)
        
        ui_manager.update(time_delta)
        ui_manager.draw_ui(window)
        pygame.display.update()

    # Clean up buttons after choice
    clean_combat_buttons()
    return weapon_chosen


def choose_spell(ui_manager,window,character):
    global button_paths_combat, button_paths_ids_combat
    clock = pygame.time.Clock()  # Ensure you have a clock to manage updates

    if button_paths_combat:
        clean_combat_buttons()
        
        
    filtered_spells = [spell for spell in character.available_spells if spell.uses_remaining > 0 and spell.cooldown_timer == 0]
    for index, spell in enumerate(filtered_spells):
        btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 100 + index * 60), (200, 50)),
            text=spell.name,
            manager=ui_manager    
        )
        button_paths_combat.append(btn)
        button_paths_ids_combat.append((spell.name, index))

    chosen_spell = None
    while chosen_spell is None:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for i, button in enumerate(button_paths_combat):
                    if event.ui_element == button:
                        chosen_spell,index = button_paths_ids_combat[i]  # Retrieve the BodyPart instance
                        clean_combat_buttons()
                        break

            ui_manager.process_events(event)
        
        ui_manager.update(time_delta)
        ui_manager.draw_ui(window)
        pygame.display.update()

    # Clean up buttons after choice
    clean_combat_buttons()
    return chosen_spell

def choose_skill(ui_manager,window,character):
    global button_paths_combat, button_paths_ids_combat,last_weapon_used
    clock = pygame.time.Clock()  # Ensure you have a clock to manage updates

    if button_paths_combat:
        clean_combat_buttons()
    
    filtered_weapons = character.filter_weapons_by_skills()
    
    chosen_weapon = choose_weapon(ui_manager,window,character,filtered_weapons)
        
    filtered_skills = [skill for skill in character.available_skills if skill.uses_remaining > 0 and skill.cooldown_timer == 0 and skill.required_weapon_family == chosen_weapon.weapon_family]
    for index, skill in enumerate(filtered_skills):
        btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 100 + index * 60), (200, 50)),
            text=skill.name,
            manager=ui_manager    
        )
        button_paths_combat.append(btn)
        button_paths_ids_combat.append((skill.name, index))

    chosen_skill = None
    while chosen_skill is None:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for i, button in enumerate(button_paths_combat):
                    if event.ui_element == button:
                        chosen_skill,index = button_paths_ids_combat[i]  # Retrieve the BodyPart instance
                        clean_combat_buttons()
                        break

            ui_manager.process_events(event)
        
        ui_manager.update(time_delta)
        ui_manager.draw_ui(window)
        pygame.display.update()
    
    last_weapon_used = chosen_weapon
    # Clean up buttons after choice
    clean_combat_buttons()
    return chosen_skill

def body_part_targeting(ui_manager,window,target):
    global button_paths_combat, button_paths_ids_combat
    clock = pygame.time.Clock()
    if button_paths_combat:
        clean_combat_buttons()
    
    for index, (name, bodypart) in enumerate(target.body_parts.items()):
        if bodypart.current_hp > 0:
            btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((300, 100 + index * 60), (200, 50)),
                text=name,  # Use the key or bodypart.name depending on your setup
                manager=ui_manager    
        )
        button_paths_combat.append(btn)
        button_paths_ids_combat.append(bodypart)  # Store the actual BodyPart instance
    
    bodypart_chosen = None
    while bodypart_chosen is None:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for i, button in enumerate(button_paths_combat):
                    if event.ui_element == button:
                        bodypart_chosen = button_paths_ids_combat[i]  # Retrieve the BodyPart instance
                        clean_combat_buttons()
                        break

            ui_manager.process_events(event)
        
        ui_manager.update(time_delta)
        ui_manager.draw_ui(window)
        pygame.display.update()

    # Clean up buttons after choice
    clean_combat_buttons()
    return bodypart_chosen
   
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
    chosen_weapon_spell = None
    if not character.has_spells_available():
        button_Spell.disable()
    if not character.has_skills_available_total():
        button_Skill.disable()
        
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
                    chosen_weapon_spell = choose_weapon(ui_manager,window,character)                    
                    action = 'attack'
                
                if event.ui_element == button_Spell:
                    if character.has_spells_available():    
                        action = "spell"
                        chosen_weapon_spell = choose_spell(ui_manager, window, character)
                        
                if event.ui_element == button_Skill:
                    if character.has_spells_available():    
                        action = "skill"
                        chosen_weapon_spell = choose_skill(ui_manager, window, character)
            # Pass the event to the UIManager
            ui_manager.process_events(event)

        # Update the UI manager and draw the UI
        ui_manager.update(time_delta)  # time_delta is the time since the last loop
        ui_manager.draw_ui(window)  # window_surface is your main display surface

        # Update the display
        pygame.display.update()

        clock.tick(60)
    
    button_Spell.enable()
    button_Skill.enable()
    return action,chosen_weapon_spell

def resolve_character_conditions(character):
    text = ""
    updated_conditions = set()
    for conditions in character.conditions:
        name,turns, *extras = conditions
        if name == "bleed":
            character.current_endurance -= extras[0] if extras else 0
            text += f"You bleed for {extras[0]} damage"
        if name == "poison":
            character.current_endurance -= extras[0] if extras else 0
            text += f"The poison deals {extras[0]} damage"
        if name == "burn":
            character.current_endurance -= extras[0] if extras else 0
            text += f"You burn for {extras[0]} damage"
        if turns > 1:
            updated_condition = (name, turns - 1) + tuple(extras)
            updated_conditions.add(updated_condition)
        elif turns == 1:
            text += f"{name} condition has ended"
    character.conditions = updated_conditions
    return text

def resolve_creature_conditions(creature):
    text = ""
    updated_conditions = set()
    for conditions in creature.conditions:
        name,turns, *extras = conditions
        if name == "bleed":
            creature.current_endurance -= extras[0] if extras else 0
            text += f"{creature.name} bleeds for {extras[0]} damage"
        if name == "poison":
            creature.current_endurance -= extras[0] if extras else 0
            text += f"The poison deals {extras[0]} damage"
        if name == "burn":
            creature.current_endurance -= extras[0] if extras else 0
            #if "fan the flames" in character.perks:
                
            text += f"The {creature.name} burn for {extras[0]} damage"
        if turns > 1:
            updated_condition = (name, turns - 1) + tuple(extras)
            updated_conditions.add(updated_condition)
        elif turns == 1:
            text += f"{name} condition has ended"
    creature.conditions = updated_conditions
    return text

def process_character_action(ui_manager,window,character_action,chosen_weapon_spell,character,creture,left_info_box,right_info_box,character_turn_number):
    text = f"Turn {character_turn_number}                " 
    match character_action:
        case "attack":
            
            damage = basic_attack(character, creature,chosen_weapon_spell)
            bodypart = body_part_targeting(ui_manager, window, creature)
            flag = dodge_block_parry(character, bodypart)
            if flag == "dodged":
                damage = 0
                text += f"\n Your attack at {bodypart.name} misses the {creature.name}, dealing no damage!"
                sound_effects['MissMelee1'].play()
            elif flag == "blocked":
                damage_blocked = 0.5* chosen_weapon_spell.negblock_parry
                damage = int(damage*0.5)
                damage = max(damage - bodypart.armor,0)
                text += f"\n Your attack at {bodypart.name} was blocked, dealing {damage}! ({damage_blocked} damage lost)({bodypart.armor} reduced by armor)"
                play_random_sound("soundcategoryaxe")
            elif flag == "parried":
                damage_parried = int(damage*0.25)
                damage = int(damage*0.75)
                damage = max(damage - bodypart.armor,0)
                text += f"\n Your attack at {bodypart.name} was parried, dealing {damage}! ({damage_parried} damage lost)({bodypart.armor} reduced by armor)" 
            else:
                damage = max(damage - bodypart.armor,0)
                text += f"\n Your {chosen_weapon_spell.name} hits the {creature.name}'s {bodypart.name} for {damage} damage ({bodypart.armor} reduced by armor)"
               # if chosen_weapon == "Axe":
                #    sound_effects["soundcategoryaxe"].play()
               # elif chosen_weapon == "Quarterstaff":
                #    sound_effects["soundcategorystaff"].play()
                if chosen_weapon_spell == "Axe":
                    play_random_sound("soundcategoryaxe")
                elif chosen_weapon_spell == "Quarterstaff":
                    play_random_sound("soundcategorystaff")
            
            creature.current_endurance -= max(damage,0)
            bodypart.current_hp -= damage
            #left_info_box = update_combat_text(left_info_box, text)
            character.reduce_all_cds()
            
        case "spell":
            chosen_spell = next((spell for spell in character.available_spells if spell.name == chosen_weapon_spell), None)
            target = creature
            if chosen_spell.targeted:
                target = body_part_targeting(ui_manager, window, creature)
            spell_text = chosen_spell.cast(character,creature,target)
            text = text + spell_text
            #left_info_box = update_combat_text(left_info_box, text)  
            character.reduce_allbutchosen_cds(chosen_weapon_spell)
        case "skill":
            chosen_skill =  next((spell for spell in character.available_skills if spell.name == chosen_weapon_spell), None)
            target = creature
            if chosen_skill.targeted:
                target = body_part_targeting(ui_manager, window, creature)
            skill_text = chosen_skill.use_skill(character,creature,target)
            text = text + skill_text
            #left_info_box = update_combat_text(left_info_box, text)  
            character.reduce_allbutchosen_cds(chosen_weapon_spell)
    
    
    condition_text = resolve_character_conditions(character)
    text += condition_text        
    left_info_box = update_combat_text(left_info_box, text)        
    return left_info_box

def creature_auto_target(character):
    available_targets = [part for part_name, part in character.body_parts.items() if part.current_hp > 0]
    chosen_target = random.choices(available_targets,k=1)[0]
    return chosen_target

def choose_creature_action(creature):
    
    available_actions = [action for action in creature.available_actions if action.is_usable(creature)]   
    weights = [action.priority for action in available_actions]
    
    chosen_action = random.choices(available_actions, weights=weights, k=1)[0]
    
    return chosen_action



            
def process_creature_action(creature_action,character,creature,left_info_box,right_info_box,creature_turn_number):
    text = f"Turn {creature_turn_number}                "
    chosen_action = choose_creature_action(creature)
    target = character
    if chosen_action.targeted:
        target =creature_auto_target(character)
    action_text = chosen_action.cast(character,creature,target)
    creature.reduce_allbutchosen_cds(chosen_action)
    condition_text = resolve_creature_conditions(creature)
    text = text + action_text + condition_text
    
    right_info_box = update_combat_text(right_info_box, text)
    return right_info_box

def combat_loop(ui_manager,window,character,creature,left_info_box,right_info_box):
    global last_weapon_used
    character_turn = False
    creature_turn = False
    character_turn_number = 0
    creature_turn_number = 0
    last_weapon_used = None

    while character.current_endurance>0 and creature.current_endurance>0 and not creature.check_vital_parts() and not character.check_vital_parts():
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
            last_weapon_used = None
            character_turn_number += 1
            character_action,chosen_weapon_spell = wait_for_player_action(ui_manager,window,character,creature)# Function to wait for player to press a button
            if character_action == "attack":
                last_weapon_used = chosen_weapon_spell #next((item for item in character.available_weapons if item.name == chosen_weapon_spell), None)
            left_info_box = process_character_action(ui_manager,window,character_action,chosen_weapon_spell, character, creature,left_info_box,right_info_box,character_turn_number)
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
        if character.current_endurance <= 0 or creature.check_vital_parts() or character.check_vital_parts() or creature.endurance <= 0:
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
        f"L. Arm: {character.body_parts['Left Arm'].current_hp}/{character.body_parts['Left Arm'].max_hp}  R. Arm: {character.body_parts['Right Arm'].current_hp}/{character.body_parts['Right Arm'].max_hp}",
        f"Legs: {character.body_parts['Legs'].current_hp}/{character.body_parts['Legs'].max_hp}"
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
    creature_text = f"Endurance:{creature.current_endurance}"
    for part in creature.body_parts.values():
        if part.current_hp <= 0:
            creature_text += f"  {part.name} DESTROYED"  # Return True if any vital part is destroyed
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
    if random.random() > attacker.accuracy - defender.dodge:
        flag = "dodged"
    else:
        if isinstance(defender, Character):
            if random.random() < defender.block:
                flag = "blocked"
            elif random.random() < defender.parry:
                flag = "parried"
        elif isinstance(defender,BodyPart):
            if random.random() < defender.owner.block:
                flag = "blocked"
            elif random.random() < defender.owner.parry:
                flag = "parried"            
        
    return flag
    
def update_combat_text(surface, text, clear_surface=True):
    if clear_surface:
        surface.fill((0, 0, 0, 255))
        window.blit(surface, (0, 60))
        # Clear the previous text by filling the surface with the same translucent color
        new_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        new_surface.fill((0, 0, 0, 255))
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
# TEST CHARACTER
# =============================================================================

running = True
button_city.hide()

testy = Character("Testycle","Test character",1,1,1,1)



shortsword = create_item("Shortsword")
axe = create_item("Axe")
quarterstaff = create_item("Quarterstaff")
testy.available_weapons.append(shortsword)
testy.available_weapons.append(axe)
testy.available_weapons.append(quarterstaff)

fireball = Spell("Fireball", [spell_fireball], 5, 1)
fissure = Spell("Fissure",[spell_fissure],5,1,targeted= False)
wallop = Spell("Wallop",[skill_wallop],5,1,required_weapon_family = "defense")
character_window_reference = None
current_slide_text = current_slide.text
testy.available_spells.append(fireball)
testy.available_spells.append(fissure)
testy.available_skills.append(wallop)
creature = Creature("Giant Rat Scorpion")
creature_tail_attack = CreatureAction("Tail_Attack",[creature_tail_attack],2,priority = 2, required_parts=[("Tail",)])
creature_swipe = CreatureAction("Swipe",[creature_swipe],2,priority = 3, required_parts=[("Right Arm","Left Arm")],targeted = False)
creature_claw_attack = CreatureAction("Claw_Attack",[creature_claw_attack],0)
creature.available_actions.append(creature_tail_attack)
creature.available_actions.append(creature_swipe)
creature.available_actions.append(creature_claw_attack)



# =============================================================================
# LOOP
# =============================================================================
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


















