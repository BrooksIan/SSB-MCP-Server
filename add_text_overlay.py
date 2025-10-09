#!/usr/bin/env python3
"""
Script to add "SSB MCP SERVER" text overlay to SSB_Home.png image.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def add_text_overlay(input_path, output_path, text="SSB MCP SERVER"):
    """Add text overlay to an image."""
    try:
        # Open the image
        img = Image.open(input_path)
        draw = ImageDraw.Draw(img)
        
        # Get image dimensions
        width, height = img.size
        
        # Calculate text size and position
        # Try to use a large font, fallback to default if not available
        try:
            # Try to use a large font
            font_size = min(width, height) // 15  # Scale font with image size
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
        except:
            try:
                # Fallback to default font
                font = ImageFont.load_default()
            except:
                font = None
        
        # Get text bounding box
        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            # Rough estimate if no font available
            text_width = len(text) * 10
            text_height = 20
        
        # Calculate position (center of image)
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Create a semi-transparent background box
        padding = 20
        box_coords = [
            x - padding, 
            y - padding, 
            x + text_width + padding, 
            y + text_height + padding
        ]
        
        # Draw background box with transparency
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(box_coords, fill=(0, 0, 0, 128))  # Semi-transparent black
        
        # Blend overlay with original image
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Draw the text
        draw.text((x, y), text, fill=(255, 255, 255), font=font)  # White text
        
        # Save the modified image
        img.save(output_path)
        print(f"✅ Successfully added text overlay to {output_path}")
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")

def main():
    """Main function."""
    input_file = "images/SSB_Home.png"
    output_file = "images/SSB_Home_with_text.png"
    
    if not os.path.exists(input_file):
        print(f"❌ Input file {input_file} not found")
        return
    
    print(f"🖼️  Adding 'SSB MCP SERVER' text overlay to {input_file}")
    add_text_overlay(input_file, output_file)
    
    if os.path.exists(output_file):
        print(f"📁 Modified image saved as: {output_file}")
        print("💡 You can now use this image in your README.md")

if __name__ == "__main__":
    main()
