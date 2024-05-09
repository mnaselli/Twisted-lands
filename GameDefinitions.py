# -*- coding: utf-8 -*-
from Classes import Item,Weapon,Slide
import pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

items = {
    "armor": [
        Item("Boots of Swiftness","armor",stat_modifiers=[("agility", 1)])
    ],
    "weapon": [
        Weapon("Shortsword","weapon","blade","arming sword","medium",min_damage = 5,max_damage = 10),     
        Weapon("Axe","weapon","ax","war axe","heavy",min_damage = 5,max_damage = 14),
        Weapon("Quarterstaff","weapon","defense","quarterstaff","light",min_damage = 3,max_damage = 8) 
    ],
    "consumable": [
        Item("potion","consumable")
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
        Slide("Champion’sFeast","Taverna Bapth","tavern",background="city"),
        Slide("GuidingStar","Taverna Savaz","tavern",background="city"),
        Slide("TheEnchantedFountain","Taverna Phaos","tavern",background="city"),
        Slide("LapOfLuxury","Taverna Jaros","tavern",background="city"),
        Slide("TheFellSpot","Taverna Dargab","tavern",background="city")
    ],
    "shop": [
        Slide("Divineprovidence","shop Saklas","shop",background="city"),
        Slide("ScalpelSteel","shop Iyao","shop",background="city"),
        Slide("Hero’sArsenal","shop Bapth","shop",background="city"),
        Slide("AscendedTreasures","shop Savaz","shop",background="city"),
        Slide("Wizard'sVault","shop Phaos","shop",background="city"),
        Slide("GildedGuild","shop Jaros","shop",background="city"),
        Slide("CuriousCollections","shop Dargab","shop",background="city")
        ],
    "sp_ed": [
        Slide("Temple","Temple Saklas","sp_ed",background="city"),
        Slide("Hospital","Hospital Iyao","sp_ed",background="city"),
        Slide("GreatForge","Forge Bapth","sp_ed",background="city"),
        Slide("Observatory","Observatory Savaz","sp_ed",background="city"),
        Slide("MageTower","Mage Tower Phaos","sp_ed",background="city"),
        Slide("Bank","Bank Jaros","sp_ed",background="city"),
        Slide("ShadowCircle","Shadow Circle Dargab","sp_ed",background="city")
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

sound_effects = {
    
    "soundcategoryaxe":[pygame.mixer.Sound('sounds/Combat/AxeHit1.mp3'),
                      pygame.mixer.Sound('sounds/Combat/AxeHit2.mp3')
                     ],
    "soundcategorystaff":[pygame.mixer.Sound('sounds/Combat/StaffHit1.mp3'),
                      pygame.mixer.Sound('sounds/Combat/StaffHit2.mp3')
                     ],
    "soundcategoryblunt":[pygame.mixer.Sound('sounds/Combat/BluntHit1.mp3'),
                      pygame.mixer.Sound('sounds/Combat/BluntHit2.mp3')
                     ],
    "soundcategoryblock":[pygame.mixer.Sound('sounds/Combat/BlockMelee1.mp3'),
                      pygame.mixer.Sound('sounds/Combat/BlockMelee2.mp3')
                     ],
    'AxeHit1': pygame.mixer.Sound('sounds/Combat/AxeHit1.mp3'),
    'AxeHit2': pygame.mixer.Sound('sounds/Combat/AxeHit2.mp3'),
    'BladeHit1': pygame.mixer.Sound('sounds/Combat/BladeHit1.mp3'),
    'BlockMelee1': pygame.mixer.Sound('sounds/Combat/BlockMelee1.mp3'),
    'BlockMelee2': pygame.mixer.Sound('sounds/Combat/BlockMelee2.mp3'),
    'BluntHit1': pygame.mixer.Sound('sounds/Combat/BluntHit1.mp3'),
    'BluntHit2': pygame.mixer.Sound('sounds/Combat/BluntHit2.mp3'),
    'ThrustHit1': pygame.mixer.Sound('sounds/Combat/ThrustHit1.mp3'),
    'StaffHit1': pygame.mixer.Sound('sounds/Combat/StaffHit1.mp3'),
    'StaffHit2': pygame.mixer.Sound('sounds/Combat/StaffHit2.mp3'),
    'UnarmedHit1': pygame.mixer.Sound('sounds/Combat/UnarmedHit1.mp3'),
    'RangedHit1': pygame.mixer.Sound('sounds/Combat/RangedHit1.mp3'),
    'MissMelee1': pygame.mixer.Sound('sounds/Combat/MissMelee1.mp3'),
    'MissRanged1': pygame.mixer.Sound('sounds/Combat/MissRanged1.mp3'),
    'ParryMelee1': pygame.mixer.Sound('sounds/Combat/ParryMelee1.mp3')
    
}  