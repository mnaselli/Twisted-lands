# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 23:38:49 2024

@author: Matts
"""
import pygame
import pygame_gui
import random
import json
pygame.init()
pygame.font.init()
# =============================================================================
# CLASSES
# =============================================================================
class Slide:
    def __init__(self,slide_id, text_template, category,test = None,city_advancement = None,button_text = None, spell = None,item = None, previous_slide = None, success_slide_id = None, fail_slide_id = None, linked_slide_id=None, is_fight=False,background =None):
        self.slide_id = slide_id
        self.text = text_template
        self.text_template = text_template
        self.category = category 
        self.linked_slide_id = linked_slide_id if linked_slide_id is not None else []
        self.is_fight = is_fight  # Flag to indicate if it's a fight slide
        self.background = background
        self.previous_slide = previous_slide
        self.city_advancement = city_advancement if city_advancement is not None else 10 #aca despues lo pongo en random
        self.use_spell = spell
        self.use_item = item
        self.button_text = button_text if button_text is not None else ["move forward"]
        self.test = test
        self.success_slide_id = success_slide_id
        self.fail_slide_id = fail_slide_id

    def is_terminal(self):
        return not self.linked_slide_id and not self.success_slide_id

    


class Character:
    def __init__(self,name,job,strenght,agility,lore,faith):
        self.name = name
        self.level = 1
        self.job = job
        self.strenght = strenght
        self.agility = agility
        self.lore = lore  # Category of the slide
        self.faith = faith
        
        
def getSlidebyID(slide_id):
    for category in slides.values():
        for slide in category:  
            if slide.slide_id == slide_id:  
                return slide      



# =============================================================================
# GAME DEF
# =============================================================================

slides = {
    "start": [
        Slide("0","TWISTED LANDS","start"),
    ],
    "wild": [
        #Slide("wild1","You're wandering in a dense forest. Birds are chirping.","wild"),
        #Slide("wild2","A clearing in the forest reveals a peaceful river.","wild"),
        Slide("wild3","The path leads you to the edge of a cliff with a breathtaking view.","wild"),
        Slide("wild4","A clearing in the forest reveals a giant tree.","wild", linked_slide_id=["chainGiantTree1","chainGiantTree2","chainGiantTree3"]),
        Slide("wild5","You enter the grove. [/color] flowers surround you filling the air with a [/smellqual] aroma of [/smell]. The birds sing, filling you with [/emotion].","wild"),
        Slide("wild6","You are crossing a bridge and it starts to break","wild", success_slide_id=["bridge_success"],fail_slide_id=["bridge_fail1,bridge_fail2"],button_text = ["run fast to the end","take a big jump"],test = ["agility","strength"]),
    ],
    "city": [
        Slide("city1","You arrive to the city of ......","city", background="city"),
        Slide("city2","You stand before the doors of ......","city", background="city"),
        Slide("city3","At the distance you see the great city of .........","city", background="city")
    ],
    "chain": [
        Slide("chainGiantTree1","You approach the giant tree and as you blink it dissapears","chain",background = "woodbackground"),
        Slide("chainGiantTree2","You approach the giant tree and as you blink it dissapears22","chain",background = "woodbackground"),
        Slide("chainGiantTree3","You go around the giant tree, and the trunk seems endless","chain",background = "woodbackground")
    ],
    "test": [
        Slide("bridge_success","You approach the giant tree and as you blink it dissapears","ctest"),
        Slide("bridge_fail1","You are not fast enough and fall taking X damage","test"),
        Slide("bridge_fail2","Your jump is not long enough and you fall taking X damage","test"),
    ],
    "character": [
        Slide("character_info","","character")
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

character_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((710, 10), (50, 30)),
                                                text='C',
                                                manager=ui_manager)


# =============================================================================
# GLOBALS
# =============================================================================


current_category = "start"


current_slide = getSlidebyID("0")


background_image = loaded_backgrounds.get(current_slide.background, loaded_backgrounds["default"])

button_paths = []
button_paths_ids = []  # This will store the next slide IDs corresponding to each button in button_paths


button_paths_linked = []
button_paths_ids_linked = []
button_paths_test = []
button_paths_ids_test = []

testy = Character("Testy","Test character",1,1,1,1)

character_window_reference = None
current_slide_text = current_slide.text
# =============================================================================
# FUNCIONES
# =============================================================================

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
    # This is a simplified example. Adjust according to your UI design.
    
    button_wild.hide()
    button_city.hide()
    #button_encounter.hide()
    for btn in button_paths_linked + button_paths_test:
        btn.hide()
    
    
    
    with open("boxes_config.json", "r") as file:
        boxes_config = json.load(file)["boxes"]
        
    texts= [f"{character.name}  Level: {character.level} {character.job}",
            f"ATTRIBUTES \n \n Strenght: {character.strenght} \n Agilityt: {character.agility} \n Lore: {character.lore} \n Faith: {character.faith}"]
    
    for text, box in zip(texts, boxes_config):
        draw_box_with_border(window, text, box)
    
def agility_test(character):
    # Placeholder logic for agility test
    return random.choice([True, False])

def strength_test(character):
    # Placeholder logic for strength test
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
        if font.size(test_line)[0] > 760:  # 760px wide for some margin
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
        
        

def update_buttons_for_slide(slide):
    global button_paths, button_paths_ids
    if current_slide:
        render_slide(window, current_slide.text)
        if slide.linked_slide_id:
        # If the current slide is part of a chain, show only the "Next Slide" button.
            button_wild.hide()
            button_city.hide()
            #button_encounter.hide()
        else:
            # If the slide is not part of a chain, show the category buttons and hide the "Next Slide" button.
            button_wild.show()
            button_city.show()
            #button_encounter.show()


def get_linked_slide(linked_slide_id):
    for category in slides.values():
        for slide in category:
            if slide.slide_id == linked_slide_id:
                return slide
    return None

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
    elif current_slide.previous_slide is not None:
        # Go back to the previous slide
        current_slide = getSlidebyID(current_slide.previous_slide)
        if button_paths_linked or button_paths_test :
            for btn in button_paths_linked + button_paths_test:
                btn.show()


def update_path_buttons(slide, ui_manager):
    
    global button_paths_linked, button_paths_ids_linked,button_paths_linked_test, button_paths_ids_test
    if slide.is_terminal():
        button_wild.show()
    else:
        button_wild.hide()
    
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
                relative_rect=pygame.Rect((100 + index * (210 + 10), 500), (200, 50)),  # Added a 10-pixel gap# Adjusted for a 20px gap
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



while running:
    time_delta = clock.tick(60)/1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        ui_manager.process_events(event)
            
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button_wild:
                select_random_slide("wild")  # Set the current slide to a random wild slide
                update_buttons_for_slide(current_slide)  # Update UI buttons for the new slide
                update_path_buttons(current_slide, ui_manager) 
            
            
            if event.ui_element in button_paths_linked:
                index = button_paths_linked.index(event.ui_element)
                linked_slide_id = button_paths_ids_linked[index]
                current_slide = getSlidebyID(linked_slide_id)
                update_path_buttons(current_slide, ui_manager)  # Update buttons for the new slide

            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in button_paths_test:
                    index = button_paths_test.index(event.ui_element)
                    test_function, action_index = button_paths_ids_test[index]
            
                    # Call the test function
                    test_passed = test_function(testy)  # Assuming `testy` is your character instance
            
                    if test_passed:
                        next_slide_id = current_slide.success_slide_id[0]  # Navigate to success slide
                    else:
                        next_slide_id = current_slide.fail_slide_id[action_index]  # Navigate to specific fail slide
            
                    current_slide = getSlidebyID(next_slide_id)
                    
                    update_path_buttons(current_slide, ui_manager)
            
# =============================================================================
#             if event.ui_element ==button_wild:
#                 # Handles category button clicks
#                 category = 'wild'
# 
#                 on_category_button_click(category)  # Function to handle category selection
# 
#                 #current_slide_text = generate_dynamic_text(current_slide.text_template, text_options)
#                 update_buttons_for_slide(current_slide)  # Update buttons based on the new slide
#                 update_path_buttons(current_slide, ui_manager)
# 
#             elif event.ui_element in button_paths:
#                 # Handles clicks on dynamically created path buttons
#                 index = button_paths.index(event.ui_element)  # Find the pressed button
#                 slide_id = button_paths_ids[index]  # Get the associated slide ID
#                 next_slide = get_linked_slide(slide_id)  # Retrieve the slide object
#                 if next_slide:
#                     current_slide = next_slide  # Transition to the next slide
#                     current_slide_text = generate_dynamic_text(current_slide.text_template, text_options)  # Update text
#                     if current_slide.linked_slide_id:
#                         update_path_buttons(current_slide, ui_manager)  # Update buttons for the next slide
#                     else:
#                         # Logic to handle the end of a chain
#                         button_wild.show()
#                         #button_city.show()
#                         #button_encounter.show()
#                         for btn in button_paths:  # Remove path buttons
#                             btn.kill()
#                         button_paths.clear()
#                         button_paths_ids.clear()
# =============================================================================
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == character_button:
                    on_character_button_click()
            
           
            current_slide_text = generate_dynamic_text(current_slide.text_template, text_options)
            #update_buttons_for_slide(current_slide)  # Update button visibility based on the new current slide.
         
        ui_manager.process_events(event)



    # If you need to check for a linked slide or a fight
    if current_slide.background and current_slide.background in loaded_backgrounds:
        background_image = loaded_backgrounds[current_slide.background]
    else:
        background_image = loaded_backgrounds["default"]
    window.blit(background_image, (0, 0))
    
    # Now, render the slide text on top of the background
    if current_slide.category == "character":
        # Special rendering for the character info slide
        display_character_info(testy)  # You'll define this function
    else:
        # Regular slide rendering
        render_slide(window, current_slide_text)
    
    # Process UI events and update the UI elements
    ui_manager.process_events(event)
    ui_manager.update(time_delta)
    ui_manager.draw_ui(window)
    
    # Update the display
    pygame.display.update()

pygame.quit()


















