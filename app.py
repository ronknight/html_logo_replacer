from bs4 import BeautifulSoup
import re

# Base URL pointing to the image directory in the GitHub repository
base_url = "https://raw.githubusercontent.com/ronknight/Logo-Image-Repository-with-Flask/refs/heads/main/static/images/"

# Custom mappings for character names with non-standard filenames
image_name_exceptions = {
    "Mickey Mouse & Friends": "mickey-mouse-and-friends-logo.png",
    "Disney Princess": "disney-princess-logo.png",
    "Justice League": "justice-league-logo.png",
    "Toy Story": "toy-story-logo.png",
    "Spider-Man": "spider-man-logo.png",
    "DC Comics": "dc-comics-logo.png",
    "Hello Kitty": "hello-kitty-logo.png",
    # Add more mappings as needed
}

def generate_image_url(character_name):
    # Use custom mapping if available
    if character_name in image_name_exceptions:
        image_name = image_name_exceptions[character_name]
    else:
        # Convert character name to lowercase, replace spaces with hyphens, and add '-logo.png' suffix
        image_name = re.sub(r'\s+', '-', character_name.strip().lower()) + "-logo.png"
    return f"{base_url}{image_name}"

def replace_text_with_images(input_file, output_file):
    # Read the input HTML file
    with open(input_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Target only the "Popular Licensed Characters" section
    popular_section = soup.find("div", class_="popular-characters")
    
    # Find all character links in the popular section to replace with image logos
    if popular_section:
        for a_tag in popular_section.find_all("a"):
            character_name = a_tag.text.strip()
            
            # Generate image URL based on character name
            image_url = generate_image_url(character_name)
            
            # Create a new `div` to wrap the image and text overlay
            wrapper_div = soup.new_tag("div", style="position: relative; display: inline-block; width: 150px; height: 150px; text-align: center;")
            
            # Create the `img` tag with the generated URL and SEO-friendly `alt` text
            img_tag = soup.new_tag("img", src=image_url, alt=f"WHOLESALE {character_name} Logo")
            img_tag["style"] = "width: 150px; height: 150px; object-fit: contain;"

            # Create the overlay div for the "Wholesale" label
            overlay_div = soup.new_tag("div", style="position: absolute; bottom: 0; background: rgba(0, 0, 0, 0.5); color: white; width: 100%; text-align: center; font-weight: bold; padding: 5px;")
            overlay_div.string = "Wholesale"

            # Append the `img` and overlay div to the wrapper div
            wrapper_div.append(img_tag)
            wrapper_div.append(overlay_div)

            # Clear any existing text or attributes in the `a` tag and add the wrapper div
            a_tag.clear()  # Clear existing text and attributes
            a_tag.append(wrapper_div)  # Insert `wrapper_div` inside the `a` tag

    # Write the modified HTML to output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(str(soup))

# Run the function to update input.html and save as output.html
replace_text_with_images("input.html", "output.html")
