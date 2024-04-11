# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 01:31:28 2024

@author: Matts
"""

def count_code_lines(file_path):
    code_lines = 0
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('#'):
                code_lines += 1
    return code_lines

# Example usage
file_path = 'Twisted_lands.py'
print("Number of code lines:", count_code_lines(file_path))