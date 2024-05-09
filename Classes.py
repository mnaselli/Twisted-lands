# -*- coding: utf-8 -*-
"""
Created on Thu May  9 16:40:55 2024

@author: Matts
"""
import random
import copy

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

        @property
        def armor(self):
                return self.armor
    
    @property
    def dodge(self):
        if self.owner:
            return self.owner.dodge + self.dodge_offset
        return self.dodge_offset
    

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


# =============================================================================
# =============================================================================
# # Spells
# =============================================================================
# =============================================================================

class Spell:
    def __init__(self, name, effects, uses_remaining, cooldown,targeted = True,required_weapon_family = False):
        self.name = name
        self.effects = effects  # This is a list of functions
        self.uses_remaining = uses_remaining 
        self.max_uses = uses_remaining  # to reset uses after resting
        self.cooldown = cooldown
        self.cooldown_timer = 0  # Tracks cooldown status
        self.targeted = targeted
        self.required_weapon_family = required_weapon_family
        
    def cast(self,character,creature,target, *args, **kwargs):
        if self.uses_remaining > 0 and self.cooldown_timer == 0:
            
            spell_level_modifier = random.randint(8, 12) * character.spell_rating
            spell_level = self.determine_spell_level(spell_level_modifier)
            kwargs['spell_level'] = spell_level
            kwargs["target"] = target
            kwargs["character"] = character
            #kwargs["creature"] = creature
            text = ""
            spell_text= ""
            for effect in self.effects:
                spell_text=effect(*args, **kwargs)  # Execute each effect function
                text = text + spell_text
            self.uses_remaining -= 1
            self.cooldown_timer = self.cooldown  # Reset cooldown timer
            return text
        
    def use_skill(self,character,creature,target, *args, **kwargs):
        if self.uses_remaining > 0 and self.cooldown_timer == 0:
            
            skill_level_modifier = random.randint(8, 12) * character.skill_rating
            skill_level = self.determine_spell_level(skill_level_modifier)
            kwargs['spell_level'] = skill_level
            kwargs["target"] = target
            kwargs["character"] = character
            #kwargs["creature"] = creature
            text = ""
            spell_text= ""
            for effect in self.effects:
                spell_text=effect(*args, **kwargs)  # Execute each effect function
                text = text + spell_text
            self.uses_remaining -= 1
            self.cooldown_timer = self.cooldown  # Reset cooldown timer
            return text
    
    def determine_spell_level(self, modifier):
        if modifier > 180:
            return 5
        elif modifier > 150:
            return 4
        elif modifier > 130:
            return 3
        elif modifier > 100:
            return 2
        elif modifier > 0:
            return 1
        return 0        
    
    
    def reduce_cooldown(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1            
            
    def reset_uses(self):
        self.uses_per_rest = self.max_uses            
                   
# =============================================================================
# =============================================================================
# # Creature actions
# =============================================================================
# =============================================================================

class CreatureAction:
    def __init__(self, name, effects, cooldown,targeted = True,priority = 1, required_parts=None):
        self.name = name
        self.effects = effects  # This is a list of functions
        self.cooldown = cooldown
        self.cooldown_timer = 0  # Tracks cooldown status
        self.targeted = targeted
        self.priority = priority
        self.required_parts = required_parts or []

    def cast(self,character,creature,target, *args, **kwargs):
        if self.cooldown_timer == 0:           
            kwargs["target"] = target
            kwargs["creature"] = creature
            text = ""
            spell_text= ""
            for effect in self.effects:
                spell_text=effect(*args, **kwargs)  # Execute each effect function
                text = text + spell_text
            self.cooldown_timer = self.cooldown  # Reset cooldown timer
            return text
        
    def reduce_cooldown(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1        
    
    def is_usable(self, creature):

        if self.cooldown_timer > 0:
             return False  # The action is on cooldown

        for parts_tuple in self.required_parts:
            all_destroyed = True
            for part in parts_tuple:
                if part in creature.body_parts:
                    if creature.body_parts[part].current_hp > 0:
                        all_destroyed = False
                        break
                else:
                    all_destroyed = False
                    break
            if all_destroyed:
                return False  # All parts in this tuple are destroyed, hence action is not usable
        return True
    
    
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
        self._dodge = 0.05
        self.crit_chance = 0.15
        self.carry_weight_base = 50
        self.armor = 1
        self._spell_rating_base = 1
        self._ritual_rating_base = 1
        self._skill_rating_base = 1
        self.block = 0.1
        self.parry = 0.1
        self.perks = []
        self.spells_known = []
        self.available_spells = []
        self.available_skills = []
        self.rituals_known = []
        self.conditions = set()
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
        self.initiative = 40
        self.initial_initiative = 0
        self.inventory = []
        self.equipped_weapon = None
        self.available_weapons = []
        self.equipped_armor = None
        

        @property
        def armor(self):
            return self.armor
        
        @property
        def dodge(self):
            return self._dodge
        
        @dodge.setter
        def dodge(self, value):
            self._dodge = value


        def take_damage(self, body_part_name, damage):
            if body_part_name in self.body_parts:
                self.body_parts[body_part_name].take_damage(damage)
                self.body_parts[body_part_name].update_conditions()


        
        
    def copy_for_combat(self):
        """Create a deep copy of the character for combat purposes."""
        return copy.deepcopy(self)
        
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
        return self._dodge + 0.01 * self.agility

    @property
    def carry_weight(self):
        return self._carry_weight_base + self.strength * 5

    @property
    def spell_rating(self):
        return self._spell_rating_base + 1 * self.lore

    @property
    def ritual_rating(self):
        return self._ritual_rating_base + 1 * self.faith
    
    @property
    def skill_rating(self):
        return self._skill_rating_base + 1 * max(self.strength,self.agility)
    
    def get_all_body_parts(self):
        return list(self.body_parts.values())

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
            

    def get_attack_modifier(self, weapon):

        if weapon.weight_type == "heavy":
            return self.strength
        elif weapon.weight_type == "medium":
            return max(self.strength, self.agility)
        elif weapon.weight_type == "light":
            return self.agility

        return 0
    def get_attack_damage(self, chosen_weapon):
        if chosen_weapon:
            # Calculate damage using the found weapon's damage range and character's stats
            return random.randint(chosen_weapon.min_damage, chosen_weapon.max_damage) + self.get_attack_modifier(chosen_weapon)
        else:
            # Optionally handle the case where no weapon is found
            return 1 + max(self.strength,self.agility)  # Default damage or consider raising an exception
        
        
    def check_vital_parts(self):
        """Check if any vital body part has 0 HP, indicating a critical condition."""
        for part in self.body_parts.values():
            if part.is_vital and part.current_hp <= 0:
                return True  # Return True if any vital part is destroyed
        return False  # Return False if all vital parts are still intact    
        
        
    def get_other_body_parts(self, target_part_name):
        # Return a list of all body parts except the one specified by target_part_name
        return [part for name, part in self.body_parts.items() if name != target_part_name]
    
    def reduce_all_cds(self):
        for spell in self.available_spells + self.available_skills:
            spell.reduce_cooldown()
    
    def reduce_allbutchosen_cds(self,chosen_spell):
        for spell in self.available_spells + self.available_skills:
            if spell.name != chosen_spell:
                spell.reduce_cooldown()

    def has_spells_available(self):
        # Check if any spells are available to cast
        for spell in self.available_spells:
            if spell.cooldown_timer == 0 and spell.uses_remaining > 0:
                return True
        return False
    
    def has_skills_available_total(self):
        for skill in self.available_skills:
            if skill.cooldown_timer == 0 and skill.uses_remaining > 0:
                return True
        return False
    
    def has_skills_available(self,weapon_family):
        # Check if any spells are available to cast
        for skill in self.available_skills:
            if skill.cooldown_timer == 0 and skill.uses_remaining > 0 and skill.required_weapon_family == weapon_family:
                return True
        return False

    def filter_weapons_by_skills(self):
        # Gather all required weapon families from skills
        required_families = {skill.required_weapon_family for skill in self.available_skills}

        # Filter weapons where their family is needed by at least one skill
        filtered_weapons = [weapon for weapon in self.available_weapons if weapon.weapon_family in required_families]

        return filtered_weapons

# =============================================================================
# =============================================================================
# # Creature
# =============================================================================
# =============================================================================

class Creature:
    def __init__(self,name):
        self.name = name
        self.endurance = 35
        self.current_endurance = 35
        self.accuracy = 0.75
        self._dodge = 0.05
        self.crit_chance = 0.30
        self.armor = 4
        self._spell_rating_base = 1
        self.block = 0
        self.parry = 0
        self.perks = []
        self.spells_known = []
        self.inventory = []
        self.conditions = set()
        self.initiative = 40
        self.initial_initiative = 0
        self.body_parts = {
            'Torso': BodyPart('Torso', 35, 5, is_vital=True),
            'Left Arm': BodyPart('Left Arm', 15,3,dodge_offset=0.05),
            'Right Arm': BodyPart('Right Arm', 15, 3,dodge_offset=0.05),
            'Head': BodyPart('Head', 30, 4, is_vital=True,dodge_offset=0.1),
            'Legs': BodyPart('Legs', 10, 4,dodge_offset=0.05),
            "Tail": BodyPart('Tail', 20, 4,dodge_offset=0.05)
        }
        for part in self.body_parts.values():
            part.owner = self
        self.available_actions = []

    @property
    def dodge(self):
        return self._dodge
    
    def check_vital_parts(self):
        """Check if any vital body part has 0 HP, indicating a critical condition."""
        for part in self.body_parts.values():
            if part.is_vital and part.current_hp <= 0:
                return True  # Return True if any vital part is destroyed
        return False  # Return False if all vital parts are still intact
    
    def get_other_body_parts(self, target_part_name):
        # Return a list of all body parts except the one specified by target_part_name
        return [part for name, part in self.body_parts.items() if name != target_part_name]
    
    def get_all_body_parts(self):
        return list(self.body_parts.values())

    def reduce_allbutchosen_cds(self,chosen_action):
        for action in self.available_actions:
            if action.name != chosen_action.name:
                action.reduce_cooldown()




# =============================================================================
# =============================================================================
# # ITEMS
# =============================================================================
# =============================================================================

class Item:
    def __init__(self, name, item_type,stat_modifiers=None, special_abilities=None):#,weight_type = None, min_damage=None,max_damage=None, stat_modifiers=None, special_abilities=None):
        self.name = name
        self.item_type = item_type
        self.stat_modifiers = stat_modifiers if stat_modifiers else []
        self.special_abilities = special_abilities if special_abilities else []

class Weapon(Item):
    def __init__(self, name,item_type,weapon_family,weapon_type,weight_type,thmin_damage = 0,thmax_damage = 0,crit_chance = 0,armor = 0,negblock_parry = 1,crit_damage = 0,arpen = 0,initiative = 0,accuracy = 0,parry_block = 0, min_damage=0,max_damage=0, stat_modifiers=None, special_abilities=None):
        super().__init__(name, item_type, stat_modifiers, special_abilities)
        self.weight_type = weight_type
        self.weapon_family = weapon_family
        self.weapon_type = weapon_type
        self.min_damage = min_damage
        self.thmin_damage = thmin_damage
        self.thmax_damage = thmax_damage
        self.max_damage = max_damage
        self.parry_block = parry_block
        self.accuracy = accuracy
        self.initiative = initiative
        self.arpen = arpen
        self.crit_damage = crit_damage
        self.crit_chance = crit_chance
        self.armor = armor
        self.negblock_parry = negblock_parry