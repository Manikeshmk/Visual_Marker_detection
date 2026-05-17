# Custom Marker Generation Guide

This guide explains how to create, generate, and test custom markers for the Marker Detection application.

## Marker Design Specifications

### Physical Specifications

```
┌─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
│  Outer Black Border (8px)    │
│  ┌───────────────────────┐  │
│  │ Inner White Area      │  │
│  │ 240×240 px            │  │
│  │  ┌─────────┐          │  │
│  │  │  20×20  │          │  │
│  │  │  Black  │  Animal  │  │
│  │  │ Square  │  Drawing │  │
│  │  │ (0,0)   │          │  │
│  │  └─────────┘          │  │
│  │                       │  │
│  └───────────────────────┘  │
└─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘

Final Output: 300×300 px
Aspect Ratio: 1:1 (Square)
```

### Technical Specifications

| Component               | Size       | Color              | Purpose                   |
| ----------------------- | ---------- | ------------------ | ------------------------- |
| Outer Border            | 8px thick  | #000000 (Black)    | Marker boundary detection |
| Inner White Area        | 240×240 px | #FFFFFF (White)    | Background for content    |
| Orientation Square      | 20×20 px   | #000000 (Black)    | Rotation detection        |
| Content Area            | Variable   | Black lines/shapes | Visual differentiation    |
| Clearance Around Corner | 20px       | -                  | Protection zone           |

### Color Values (Hex)

```
Black: #000000 (RGB: 0, 0, 0)
White: #FFFFFF (RGB: 255, 255, 255)
Content: Use high-contrast blacks/grays
```

## Method 1: Python PIL Generation

### Installation

```bash
pip install Pillow
```

### Generate Marker Script

```python
#!/usr/bin/env python3
"""
Generate custom markers with animal drawings
"""
from PIL import Image, ImageDraw
import os

def generate_marker(animal_type: str, output_dir: str = "markers"):
    """
    Generate a 300x300px marker with specified animal drawing

    Args:
        animal_type: 'dog', 'cat', 'bird', 'fish'
        output_dir: Directory to save marker
    """
    os.makedirs(output_dir, exist_ok=True)

    # Create image
    img = Image.new('RGB', (300, 300), color='white')
    draw = ImageDraw.Draw(img)

    # Draw outer black border (8px thick)
    border_width = 8
    draw.rectangle([0, 0, 299, 299], outline='black', width=border_width)

    # Draw inner white area boundary (visual reference)
    inner_start = border_width
    inner_end = 300 - border_width
    draw.rectangle([inner_start, inner_start, inner_end, inner_end],
                   outline='lightgray', width=1)

    # Draw orientation marker (20x20 black square at top-left)
    corner_offset = 20  # 20px from edge
    corner_size = 20
    corner_start = border_width + corner_offset
    corner_end = corner_start + corner_size
    draw.rectangle([corner_start, corner_start, corner_end, corner_end],
                   fill='black', outline='black')

    # Draw animal-specific content
    if animal_type == 'dog':
        draw_dog(draw)
    elif animal_type == 'cat':
        draw_cat(draw)
    elif animal_type == 'bird':
        draw_bird(draw)
    elif animal_type == 'fish':
        draw_fish(draw)

    # Save
    output_path = os.path.join(output_dir, f"marker_{animal_type}.png")
    img.save(output_path)
    print(f"Saved: {output_path}")
    return img

def draw_dog(draw):
    """Draw simple dog face"""
    # Head circle
    draw.ellipse([100, 80, 200, 180], outline='black', width=2)

    # Eyes
    draw.ellipse([120, 100, 135, 115], fill='black')
    draw.ellipse([165, 100, 180, 115], fill='black')

    # Nose
    draw.ellipse([140, 130, 160, 150], fill='black')

    # Mouth
    draw.line([150, 150, 150, 170], fill='black', width=2)

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

def draw_fish(draw):
    """Draw simple fish"""
    # Body (ellipse)
    draw.ellipse([90, 100, 210, 180], outline='black', width=2)

    # Eye
    draw.ellipse([150, 115, 165, 130], fill='black')

    # Mouth
    draw.arc([200, 100, 230, 140], 0, 180, fill='black', width=2)

    # Tail
    draw.polygon([(90, 130), (50, 110), (50, 150)], fill='black')

    # Fin
    draw.polygon([(150, 100), (160, 70), (140, 100)], fill='black')

# Generate all marker types
if __name__ == "__main__":
    for animal in ['dog', 'cat', 'bird', 'fish']:
        generate_marker(animal)
    print("All markers generated!")
```

### Generate All Rotations

```python
import cv2
import numpy as np

def generate_rotations(marker_path: str, output_dir: str = "rotations"):
    """Generate 0°, 90°, 180°, 270° rotations of marker"""
    os.makedirs(output_dir, exist_ok=True)

    img = cv2.imread(marker_path)
    base_name = os.path.splitext(os.path.basename(marker_path))[0]

    rotations = {
        0: img,
        90: cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE),
        180: cv2.rotate(img, cv2.ROTATE_180),
        270: cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    }

    for angle, rotated in rotations.items():
        output_path = os.path.join(output_dir, f"{base_name}_{angle}deg.png")
        cv2.imwrite(output_path, rotated)
        print(f"Saved: {output_path}")

# Usage
generate_rotations("markers/marker_dog.png")
```

## Method 2: SVG Generation

### SVG Template

Create `marker_template.svg`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg width="300" height="300" xmlns="http://www.w3.org/2000/svg">
  <!-- White background -->
  <rect width="300" height="300" fill="white"/>

  <!-- Outer black border (8px) -->
  <rect x="0" y="0" width="300" height="300" fill="none" stroke="black" stroke-width="8"/>

  <!-- Inner white area boundary (for reference) -->
  <rect x="8" y="8" width="284" height="284" fill="none" stroke="lightgray" stroke-width="1"/>

  <!-- Orientation marker (20x20 black square at top-left) -->
  <rect x="28" y="28" width="20" height="20" fill="black"/>

  <!-- Animal drawing (example: simple dog face) -->
  <g id="dog-content">
    <!-- Head circle -->
    <circle cx="150" cy="130" r="50" fill="none" stroke="black" stroke-width="2"/>

    <!-- Eyes -->
    <circle cx="130" cy="110" r="7" fill="black"/>
    <circle cx="170" cy="110" r="7" fill="black"/>

    <!-- Nose -->
    <circle cx="150" cy="140" r="8" fill="black"/>

    <!-- Mouth -->
    <line x1="150" y1="150" x2="150" y2="165" stroke="black" stroke-width="2"/>

    <!-- Ears -->
    <circle cx="100" cy="85" r="15" fill="black"/>
    <circle cx="200" cy="85" r="15" fill="black"/>
  </g>
</svg>
```

### Convert SVG to PNG

```bash
# Using ImageMagick
convert -density 150 marker_template.svg -background white marker_dog.png

# Using Inkscape
inkscape marker_template.svg --export-filename=marker_dog.png --export-dpi=150
```

## Method 3: Online Marker Generator

A simple web-based tool can be created:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Marker Generator</title>
  </head>
  <body>
    <h1>Custom Marker Generator</h1>
    <canvas id="canvas" width="300" height="300"></canvas>
    <button onclick="generateMarker()">Generate</button>
    <button onclick="downloadMarker()">Download PNG</button>

    <script>
      const canvas = document.getElementById('canvas');
      const ctx = canvas.getContext('2d');

      function generateMarker() {
        // White background
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, 300, 300);

        // Outer black border
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 8;
        ctx.strokeRect(4, 4, 292, 292);

        // Orientation square (top-left)
        ctx.fillStyle = 'black';
        ctx.fillRect(28, 28, 20, 20);

        // Sample animal (dog face)
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 2;

        // Head
        ctx.beginPath();
        ctx.arc(150, 130, 50, 0, Math.PI * 2);
        ctx.stroke();

        // Eyes
        ctx.fillRect(120, 100, 10, 10);
        ctx.fillRect(170, 100, 10, 10);

        // Nose
        ctx.beginPath();
        ctx.arc(150, 140, 8, 0, Math.PI * 2);
        ctx.fill();

        // Mouth
        ctx.beginPath();
        ctx.moveTo(150, 150);
        ctx.lineTo(150, 165);
        ctx.stroke();
      }

      function downloadMarker() {
        const link = document.createElement('a');
        link.href = canvas.toDataURL('image/png');
        link.download = 'marker.png';
        link.click();
      }
    </script>
  </body>
</html>
```

## Testing Your Custom Markers

### Test Suite

Create test images in these orientations:

```
test-images/
├── marker_0deg.png      (Original)
├── marker_90deg.png     (Rotated 90° clockwise)
├── marker_180deg.png    (Upside down)
├── marker_270deg.png    (Rotated 270° clockwise / 90° counter-clockwise)
└── marker_perspective.png (Tilted at 30-45° angle)
```

### Validation Checklist

- [ ] **Black Border**: Pure black, 8px thick, sharp edges
- [ ] **Inner White**: Pure white, 240×240 px area
- [ ] **Corner Square**: 20×20 px black, 20px from edges
- [ ] **Content Contrast**: Black lines on white, high contrast
- [ ] **Sharpness**: No anti-aliasing artifacts on borders
- [ ] **Color Accuracy**: Use #000000 and #FFFFFF exactly
- [ ] **File Format**: PNG with no compression artifacts
- [ ] **Resolution**: 300×300 px minimum

### Quick Test

```bash
# Run the app with test markers
adb push test-images/marker_0deg.png /sdcard/Pictures/

# View marker properties
python3 -c "
from PIL import Image
import numpy as np

img = Image.open('marker_0deg.png')
arr = np.array(img)

print(f'Size: {img.size}')
print(f'Mode: {img.mode}')
print(f'Unique colors: {len(np.unique(arr.reshape(-1, 3), axis=0))}')
print(f'Border pixels: {arr[0, 0]}')  # Should be [0, 0, 0]
print(f'Inner pixels: {arr[50, 50]}')  # Should be [255, 255, 255]
"
```

## Marker Variations

You can create marker variations for different scenarios:

### Variant 1: Simple Outline

```python
def create_outline_marker():
    """Minimal marker - just border and corner square"""
    img = Image.new('RGB', (300, 300), 'white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 299, 299], outline='black', width=8)
    draw.rectangle([28, 28, 48, 48], fill='black')
    return img
```

### Variant 2: QR-Like Pattern

```python
def create_pattern_marker():
    """Marker with grid pattern instead of image"""
    img = Image.new('RGB', (300, 300), 'white')
    draw = ImageDraw.Draw(img)
    # Border
    draw.rectangle([0, 0, 299, 299], outline='black', width=8)
    # Corner marker
    draw.rectangle([28, 28, 48, 48], fill='black')
    # Grid pattern
    for i in range(50, 250, 30):
        draw.line([50, i, 250, i], fill='black', width=1)
        draw.line([i, 50, i, 250], fill='black', width=1)
    return img
```

### Variant 3: Text Marker

```python
from PIL import ImageFont

def create_text_marker(text: str):
    """Marker with text identifier"""
    img = Image.new('RGB', (300, 300), 'white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 299, 299], outline='black', width=8)
    draw.rectangle([28, 28, 48, 48], fill='black')

    font = ImageFont.load_default()
    draw.text((120, 140), text, fill='black', font=font)
    return img
```

## Performance Notes

### PNG Encoding

- Use PNG format for lossless compression
- File size typically 2-5 KB per marker
- No quality loss compared to raw image

### Image Dimensions

- 300×300 px recommended for balance between detection accuracy and processing speed
- Minimum 200×200 px to detect 20×20 corner square
- Maximum 500×500 px may slow detection

### Color Accuracy

- Ensure exact #000000 black and #FFFFFF white
- Avoid gray values or anti-aliasing
- Use binary image processing for best results

## Distribution

Save generated markers in:

```
MarkerDetector/
├── test-images/
│   ├── correct-markers/
│   │   ├── marker_dog_0deg.png
│   │   ├── marker_dog_90deg.png
│   │   ├── marker_dog_180deg.png
│   │   └── marker_dog_270deg.png
│   └── incorrect-markers/
│       ├── red_x.png
│       ├── plain_white.png
│       └── no_corner_square.png
```

These can be:

1. Printed for physical testing
2. Displayed on secondary devices
3. Used in app documentation
4. Shared with QA teams

---

For questions or issues with marker generation, refer to the main `README.md` or `Approach.md`.
