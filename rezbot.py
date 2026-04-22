import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# SAFETY CHECK: Load the template once at the start so we don't open/close it 500 times.
template_path = os.path.join(BASE_PATH, 'item_template.html')

if not os.path.exists(template_path):
    print("CRITICAL ERROR: item_template.html not found in root directory!")
    landing_template = "<html><body>Template Missing - Check Rezbot setup</body></html>"
else:
    with open(template_path, 'r', encoding='utf-8') as t:
        landing_template = t.read()

def build_aisle_page(cat_name, sub_df, filename):
    path = os.path.join(BASE_PATH, filename)
    
    # Create the drawer for individual item pages
    items_dir = os.path.join(BASE_PATH, 'items')
    if not os.path.exists(items_dir):
        os.makedirs(items_dir)

    # 1. The Aisle Header (Kept exactly as original)
    aisle_html = f"""<!DOCTYPE html> <html lang="en"> <head> <link href="https://googleapis.com" rel="stylesheet"> <meta charset="UTF-8"> <title>{cat_name} | Bulldog of the Pines</title> <meta name="robots" content="index, follow"> <link rel="canonical" href="https://bulldogofthepines.com/{filename}" /> <style> body {{ font-family: sans-serif; background: #f4f4f4; color: #333; margin: 0; padding: 0; }} #product-container {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; padding: 20px; }} .product {{ background: white; border: 1px solid #ddd; padding: 20px; border-radius: 8px; text-align: center; }} img {{ max-width: 100%; height: auto; border-radius: 4px; margin: 10px 0; }} .price {{ font-weight: bold; color: #b12704; font-size: 1.2rem; }} .search-wrapper {{ padding: 0 20px; margin-top: 20px; }} #searchInput {{ width: 100%; max-width: 500px; padding: 12px; border-radius: 25px; border: 2px solid #021F00; font-size: 16px; outline: none; }} </style> <script> function filterProducts() {{ let input = document.getElementById('searchInput').value.toLowerCase(); let products = document.getElementsByClassName('product'); for (let i = 0; i < products.length; i++) {{ let title = products[i].getElementsByTagName('h3')[0].innerText.toLowerCase(); if (title.includes(input)) {{ products[i].style.display = ""; }} else {{ products[i].style.display = "none"; }} }} }} </script> </head> <body> <div class="banner" style="width: 100%; height: 300px; background-image: url('banner.jpg'); background-position: center; background-size: 100% 100%; background-repeat: no-repeat;"></div> <div style="padding: 20px;"><a href="inventory-mirror.html" style="color: #021F00; font-weight: bold; text-decoration: none;">← Back to All Categories</a></div> <div class="search-wrapper"> <input type="text" id="searchInput" onkeyup="filterProducts()" placeholder="Search {cat_name}..."> </div> <h1 style="margin-left: 20px; color: #021F00; font-family: 'Ultra', serif; font-size: 2.5em;">{cat_name}</h1> <div id="product-container">"""

    # 2. The Product Logic
    for index, row in sub_df.iterrows():
        # Capture raw data
        item_id = str(row.get('id', row.get('ItemID', '')))
        title = str(row.get('title', row.get('Title', ''))).replace('"', "'")
        image = str(row.get('image_link', row.get('Image', '')))
        price_clean = str(row.get('price', '0.00')).replace(' USD', '').replace('$', '').strip()
        gmc_condition = str(row.get('condition', 'used')).lower()
        human_condition = str(row.get('raw_condition', row.get('condition', 'Used')))
        
        ebay_url = f"https://www.ebay.com/itm/{item_id}"
        full_desc = f"Quality item from Bulldog of the Pines: {title}. eBay Condition: {human_condition}"

        # --- THE NEW "HARD LANDING" SIDE MISSION ---
        # Replace the meta-refresh string with the template-swap logic
        item_page_html = landing_template.replace('{{title}}', title) \
                                         .replace('{{image}}', image) \
                                         .replace('{{price}}', price_clean) \
                                         .replace('{{description}}', full_desc) \
                                         .replace('{{item_id}}', item_id) \
                                         .replace('{{ebay_url}}', ebay_url) \
                                         .replace('{{human_condition}}', human_condition) \
                                         .replace('{{condition_url}}', 'https://schema.org' if gmc_condition == 'new' else 'https://schema.org')

        # Write the individual item landing page
        with open(os.path.join(items_dir, f"{item_id}.html"), "w", encoding="utf-8") as f:
            f.write(item_page_html)
        # --- END SIDE MISSION ---

        # 3. The Aisle Display (Kept exactly as original)
        aisle_html += f""" <div class="product"> <a href="{ebay_url}" target="_blank" style="text-decoration:none; color:inherit;"> <h3>{title}</h3> </a> <a href="{ebay_url}" target="_blank"> <img src="{image}" alt="{title}" style="max-width: 150px;"> </a> <p class="price">${price_clean}</p> <p>Condition: {human_condition}</p> <a href="{ebay_url}" target="_blank" style="color: #0066c0; text-decoration: none; font-weight: bold;">View on eBay</a> </div>"""

    # Close the Aisle Page and Save
    aisle_html += "</div></body></html>"
    with open(path, "w", encoding="utf-8") as f:
        f.write(aisle_html)

    with open(path, "w", encoding="utf-8") as f:
        f.write(aisle_html)
