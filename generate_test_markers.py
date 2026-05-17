#!/usr/bin/env python3
"""
Generate test markers for the Marker Detection app
"""

from PIL import Image, ImageDraw
import os

def create_test_markers():
    """Create correct and incorrect test markers"""
    
    # Create directories
    os.makedirs("test-images/correct-markers", exist_ok=True)
    os.makedirs("test-images/incorrect-markers", exist_ok=True)
    
    # Correct marker with dog drawing
    create_dog_marker("test-images/correct-markers/marker_dog_0deg.png", rotation=0)
    create_dog_marker("test-images/correct-markers/marker_dog_90deg.png", rotation=90)
    create_dog_marker("test-images/correct-markers/marker_dog_180deg.png", rotation=180)
    create_dog_marker("test-images/correct-markers/marker_dog_270deg.png", rotation=270)
    
    # Correct marker with cat drawing
    create_cat_marker("test-images/correct-markers/marker_cat_0deg.png", rotation=0)
    
    # Correct marker with bird drawing
    create_bird_marker("test-images/correct-markers/marker_bird_0deg.png", rotation=0)
    
    # Incorrect markers
    create_incorrect_no_corner("test-images/incorrect-markers/marker_no_corner.png")
    create_incorrect_red_x("test-images/incorrect-markers/marker_red_x.png")
    create_incorrect_plain_white("test-images/incorrect-markers/marker_white.png")
    
    print("All test markers created!")

def create_base_marker(animal_func, filename, rotation=0):
    """Create a marker with animal drawing and optional rotation"""
    img = Image.new('RGB', (300, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Outer black border (8px thick)
    border_width = 8
    draw.rectangle([0, 0, 299, 299], outline='black', width=border_width)
    
    # Inner reference (light gray, thin)
    inner_start = border_width
    inner_end = 300 - border_width
    draw.rectangle([inner_start, inner_start, inner_end, inner_end], 
                   outline='lightgray', width=1)
    
    # Orientation marker (20x20 black square at top-left of inner area)
    corner_offset = 20
    corner_size = 20
    corner_start = border_width + corner_offset
    corner_end = corner_start + corner_size
    draw.rectangle([corner_start, corner_start, corner_end, corner_end], 
                   fill='black', outline='black')
    
    # Draw animal content
    animal_func(draw)
    
    # Apply rotation if needed
    if rotation != 0:
        img = img.rotate(rotation, expand=False, fillcolor='white')
    
    img.save(filename)
    print(f"Created: {filename}")

def draw_dog(draw):
    """Draw simple dog face centered at 150,140"""
    # Head circle
    draw.ellipse([100, 80, 200, 180], outline='black', width=2)
    
    # Eyes
    draw.ellipse([120, 100, 135, 115], fill='black')
    draw.ellipse([165, 100, 180, 115], fill='black')
    
    # Nose
    draw.ellipse([140, 130, 160, 150], fill='black')
    
    # Mouth
    draw.line([150, 150, 150, 165], fill='black', width=2)
    
    # Ears
    draw.ellipse([85, 60, 105, 100], fill='black')
    draw.ellipse([195, 60, 215, 100], fill='black')

def draw_cat(draw):
    """Draw simple cat face"""
    # Head circle
    draw.ellipse([100, 80, 200, 180], outline='black', width=2)
    
    # Eyes
    draw.ellipse([120, 105, 135, 120], fill='black')
    draw.ellipse([165, 105, 180, 120], fill='black')
    
    # Nose
    draw.polygon([(150, 135), (145, 145), (155, 145)], fill='black')
    
    # Mouth
    draw.line([150, 145, 145, 155], fill='black', width=2)
    draw.line([150, 145, 155, 155], fill='black', width=2)
    
    # Pointy ears
    draw.polygon([(85, 50), (75, 80), (95, 75)], fill='black')
    draw.polygon([(215, 50), (225, 80), (205, 75)], fill='black')

def draw_bird(draw):
    """Draw simple bird"""
    # Body
    draw.ellipse([110, 100, 190, 160], outline='black', width=2)
    
    # Head
    draw.ellipse([165, 80, 200, 115], outline='black', width=2)
    
    # Eye
    draw.ellipse([180, 90, 190, 100], fill='black')
    
    # Beak
    draw.polygon([(200, 95), (220, 90), (200, 100)], fill='black')
    
    # Wing
    draw.arc([110, 100, 190, 160], 0, 180, fill='black', width=2)
    
    # Tail
    draw.polygon([(110, 130), (80, 120), (85, 150)], outline='black', width=2)

def create_dog_marker(filename, rotation=0):
    """Create correct dog marker with optional rotation"""
    create_base_marker(draw_dog, filename, rotation)

def create_cat_marker(filename, rotation=0):
    """Create correct cat marker with optional rotation"""
    create_base_marker(draw_cat, filename, rotation)

def create_bird_marker(filename, rotation=0):
    """Create correct bird marker with optional rotation"""
    create_base_marker(draw_bird, filename, rotation)

def create_incorrect_no_corner(filename):
    """Create incorrect marker without corner square"""
    img = Image.new('RGB', (300, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Outer black border (8px thick)
    border_width = 8
    draw.rectangle([0, 0, 299, 299], outline='black', width=border_width)
    
    # NO corner square - this is the difference
    # Draw some content instead
    draw.ellipse([100, 80, 200, 180], outline='black', width=2)
    draw.ellipse([120, 100, 135, 115], fill='black')
    draw.ellipse([165, 100, 180, 115], fill='black')
    
    img.save(filename)
    print(f"Created: {filename}")

def create_incorrect_red_x(filename):
    """Create incorrect marker with red X (should be rejected)"""
    img = Image.new('RGB', (300, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Outer black border (8px thick)
    border_width = 8
    draw.rectangle([0, 0, 299, 299], outline='black', width=border_width)
    
    # Orientation marker (20x20 black square at top-left)
    corner_offset = 20
    corner_size = 20
    corner_start = border_width + corner_offset
    corner_end = corner_start + corner_size
    draw.rectangle([corner_start, corner_start, corner_end, corner_end], 
                   fill='black', outline='black')
    
    # Draw RED X in center - this should cause rejection based on center intensity
    # Red line from top-left to bottom-right
    draw.line([80, 80, 220, 220], fill='red', width=8)
    # Red line from top-right to bottom-left
    draw.line([220, 80, 80, 220], fill='red', width=8)
    
    img.save(filename)
    print(f"Created: {filename}")

def create_incorrect_plain_white(filename):
    """Create incorrect marker that's mostly white (should be rejected)"""
    img = Image.new('RGB', (300, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Outer black border (8px thick)
    border_width = 8
    draw.rectangle([0, 0, 299, 299], outline='black', width=border_width)
    
    # Orientation marker (20x20 black square at top-left)
    corner_offset = 20
    corner_size = 20
    corner_start = border_width + corner_offset
    corner_end = corner_start + corner_size
    draw.rectangle([corner_start, corner_start, corner_end, corner_end], 
                   fill='black', outline='black')
    
    # Rest is just white - no content
    # This will have high center mean value and be rejected
    
    img.save(filename)
    print(f"Created: {filename}")

if __name__ == "__main__":
    create_test_markers()
