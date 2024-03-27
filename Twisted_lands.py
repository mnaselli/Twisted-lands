# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 23:38:49 2024

@author: Matts
"""
import pygame
import pygame_gui
import random
pygame.init()
pygame.font.init()
# =============================================================================
# CLASSES
# =============================================================================
class Slide:
    def __init__(self,slide_id, text_template, category, linked_slide_id=None, is_fight=False,background =None):
        self.slide_id = slide_id
        self.text = text_template
        self.text_template = text_template
        self.category = category 
        self.linked_slide_id = linked_slide_id if linked_slide_id is not None else [] 
        self.is_fight = is_fight  # Flag to indicate if it's a fight slide
        self.background = background
            

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
        Slide("wild5","You enter the grove. [/color] flowers surround you filling the air with a [/smellqual] aroma of [/smell]. The birds sing, filling you with [/emotion].","wild")
    ],
    "city": [
        Slide("city1","You arrive to the city of ......","city", background="city"),
        Slide("city2","You stand before the doors of ......","city", background="city"),
        Slide("city3","At the distance you see the great city of .........","city", background="city")
    ],
    "encounter": [
        Slide("encounter1","A strange animal approaches you menacingly.","encounter"),
        Slide("encounter2","A human like creature ambushes you, weapons at hand.","encounter"),
        Slide("encounter3","An old friend finds you, bringing news from home.","encounter")
    ],
    "chain": [
        Slide("chainGiantTree1","You approach the giant tree and as you blink it dissapears","chain",background = "woodbackground"),
        Slide("chainGiantTree2","You approach the giant tree and as you blink it dissapears22","chain",background = "woodbackground"),
        Slide("chainGiantTree3","You go around the giant tree, and the trunk seems endless","chain",background = "woodbackground")
    ]
}


text_options = {
    "[/color]": ["Purple", "Red", "Yellow", "Vibrant", "Pale"],
    "[/smellqual]": ["sweet", "strong", "delicate", "overpowering", "unpleasant"],
    "[/smell]": ["roses", "lavender", "corpses", "fresh rain", "pine"],
    "[/emotion]": ["dread", "joy", "peace", "excitement", "anxiety"],
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

button_city = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 550), (200, 50)),
                                           text='City',
                                           manager=ui_manager)

button_encounter = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 550), (200, 50)),
                                                 text='Encounter',
                                                 manager=ui_manager)

character_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (50, 30)),
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


testy = Character("Testy","wanderer",1,1,1,1)

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
        test_line = f"{line} {word}".strip()  # Try adding the next word
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
            button_encounter.hide()
        else:
            # If the slide is not part of a chain, show the category buttons and hide the "Next Slide" button.
            button_wild.show()
            button_city.show()
            button_encounter.show()


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




def update_path_buttons(slide, ui_manager):
    # Clear existing buttons
    for btn in button_paths:
        btn.kill()
    button_paths.clear()
    button_paths_ids.clear()

    # Assuming slide.linked_slide_id is a list of slide IDs for next possible slides
    for index, slide_id in enumerate(slide.linked_slide_id):

        # Modified positioning to include a gap between buttons
        btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100 + index * (210 + 10), 500), (200, 50)),  # Added a 10-pixel gap# Adjusted for a 20px gap
            text=f"Option {index + 1}",
            manager=ui_manager
        )
        button_paths.append(btn)
        button_paths_ids.append(slide_id)



# =============================================================================
# =============================================================================
# # WINDOW
# =============================================================================
# =============================================================================

def create_character_window(ui_manager, character):
    global character_window_reference
    # Window dimensions and position
    if character_window_reference is not None:
            # The window already exists, so you could either do nothing or focus the existing window
            # For example, do nothing or bring the window to front if supported
            return    
    window_rect = pygame.Rect((0, 0), (800, 600))
    character_window = pygame_gui.elements.UIWindow(rect=window_rect,
                                                   manager=ui_manager,
                                                   window_display_title= "caracter info"#,
#                                                     object_id="#character_window")
# =============================================================================
                                                    )
    character_window_reference = character_window                                               
    # Close button
# =============================================================================
#     close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((370, 2), (28, 28)),
#                                                 text='X',
#                                                 manager=ui_manager,
#                                                 container=character_window,
#                                                 tool_tip_text='Close')
# =============================================================================

    # Display character attributes
    name_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 40), (380, 50)),
                                             text=f"{character.name} - Level: {character.level}  {character.job} ",
                                             manager=ui_manager,
                                             container=character_window)
# =============================================================================
# 
#     level_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 90), (380, 50)),
#                                               text=f"Level: {character.level}",
#                                               manager=ui_manager,
#                                               container=character_window)
# 
#     health_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 140), (380, 50)),
#                                                text=f"Health: {character.job}",
#                                                manager=ui_manager,
#                                                container=character_window)





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
        
        
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == character_window_reference:
                character_window_reference = None  # Reset the reference when the window is closed
            
            
            
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element in [button_wild, button_city, button_encounter]:
                # Handles category button clicks
                category = 'wild' if event.ui_element == button_wild else ('city' if event.ui_element == button_city else 'encounter')

                on_category_button_click(category)  # Function to handle category selection

                current_slide_text = generate_dynamic_text(current_slide.text_template, text_options)
                update_buttons_for_slide(current_slide)  # Update buttons based on the new slide

            elif event.ui_element in button_paths:
                # Handles clicks on dynamically created path buttons
                index = button_paths.index(event.ui_element)  # Find the pressed button
                slide_id = button_paths_ids[index]  # Get the associated slide ID
                next_slide = get_linked_slide(slide_id)  # Retrieve the slide object
                if next_slide:
                    current_slide = next_slide  # Transition to the next slide
                    current_slide_text = generate_dynamic_text(current_slide.text_template, text_options)  # Update text
                    if current_slide.linked_slide_id:
                        update_path_buttons(current_slide, ui_manager)  # Update buttons for the next slide
                    else:
                        # Logic to handle the end of a chain
                        button_wild.show()
                        button_city.show()
                        button_encounter.show()
                        for btn in button_paths:  # Remove path buttons
                            btn.kill()
                        button_paths.clear()
                        button_paths_ids.clear()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in button_paths:
                    index = button_paths.index(event.ui_element)
                    # Handle the button click as before
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:

            
                
                if current_slide.linked_slide_id:
                    update_path_buttons(current_slide, ui_manager)            
            current_slide_text = generate_dynamic_text(current_slide.text_template, text_options)
            update_buttons_for_slide(current_slide)  # Update button visibility based on the new current slide.
         
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == character_button:
                create_character_window(ui_manager, testy)  # Assuming you have a character instance   
         
            
         
        ui_manager.process_events(event)



    # If you need to check for a linked slide or a fight
    if current_slide.background and current_slide.background in loaded_backgrounds:
        background_image = loaded_backgrounds[current_slide.background]
    else:
        background_image = loaded_backgrounds["default"]
    window.blit(background_image, (0, 0))
    
    # Now, render the slide text on top of the background
    render_slide(window, current_slide_text)
    
    # Process UI events and update the UI elements
    ui_manager.process_events(event)
    ui_manager.update(time_delta)
    ui_manager.draw_ui(window)
    
    # Update the display
    pygame.display.update()

pygame.quit()


















