import pandas as pd
import os
import chompbot_fetch 
import catpro  # Logic for the Bulldog Buckets
import rezbot

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
latest_csv = os.path.join(BASE_PATH, "latest_inventory.csv")
output_html = os.path.join(BASE_PATH, "inventory-mirror.html")

def generate_ghost_mirror():
    print("🔄 GhoBot is signaling ChOmpBot to start the sweep...")
    chompbot_fetch.get_full_inventory() 
    print("✅ Sweep successful. Now building the Mirror...")

    if not os.path.exists(latest_csv):
        print("❌ Error: latest_inventory.csv not found.")
        return

    df = pd.read_csv(latest_csv)
    # ... after loading the df ...
    grouped_data = catpro.group_inventory_by_cat(df)
    
    html_content = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Available Items</title>
        <meta name="robots" content="index, follow">
        
        <!-- START DELETE: Font & Canonical Section -->
        <link rel="preconnect" href="https://googleapis.com">
        <link rel="preconnect" href="https://gstatic.com" crossorigin>
        <link href="https://googleapis.com/css2?family=Ultra&display=swap" rel="stylesheet">
        <link rel="canonical" href="https://bulldogofthepines.com/inventory-mirror.html" />
        <!-- END DELETE: Font & Canonical Section -->
    
        <style>
            body {{ font-family: sans-serif; background: #f4f4f4; color: #333; margin: 0; padding: 0; }}
            
            .banner {{ 
                width: 100%; 
                height: 300px; 
                background-image: url('banner.jpg');
                background-position: center;
                background-size: 100% 100%;
                background-repeat: no-repeat;
            }}
    
            /* START DELETE: Bulldog Title Styling */
            h1 {{ 
                color: #021F00; 
                font-family: 'Ultra', serif; 
                font-size: 3.5em;
                margin: 20px 0 5px 20px; 
                letter-spacing: -2px; 
            }}
    
            .update-tag {{
                font-family: sans-serif;
                font-size: 0.2em; 
                font-style: italic;
                color: #666;
                letter-spacing: 0px;
                vertical-align: middle;
                margin-left: 12px;
            }}
            /* END DELETE: Bulldog Title Styling */
    
            #product-container {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); 
                gap: 20px; 
                padding: 20px; 
            }}
            
            .product {{ background: white; border: 1px solid #ddd; padding: 20px; border-radius: 8px; text-align: center; }}
            img {{ max-width: 100%; height: auto; border-radius: 4px; margin: 10px 0; }}
            .price {{ font-weight: bold; color: #b12704; font-size: 1.2rem; }}
    
            @media (max-width: 768px) {{
                h1 {{ font-size: 1.8em; letter-spacing: -1px; }}
                .banner {{ height: 35vw; }}
            }}
        </style>
    </head>
    <body>
        <div class="banner"></div>
        
        <!-- START DELETE: Navigation & Page Title -->
        <div style="margin: 20px 0 0 20px;">
            <a href="index.html" style="color: #021F00; text-decoration: none; font-weight: bold; font-size: 0.9em;">← Back to Home</a>
        </div>
    
        <h1> Shop By Category <span class="update-tag">(updates daily)</span></h1>
        <!-- END DELETE: Navigation & Page Title -->
        """ # <--- ADD THIS HERE TO CLOSE THE STRING
    
    # Build the Visual Category Grid
    html_content += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; padding: 20px; width: 100%; box-sizing: border-box;">'
        
    # --- STEP 1: BUILD THE MAIN HUB (The Menu) ---
    html_content += "<h1>Shop by Category</h1>"
    html_content += '<div id="category-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 20px;">'

    for cat_name, sub_df in grouped_data.items():
        if not sub_df.empty:
            img_file = catpro.cat_images.get(cat_name, "Other.JPG")
            safe_name = cat_name.replace(" ", "_").replace(",", "").replace("&", "")
            aisle_filename = f"{safe_name}.html"
            
            # Link to the Aisle Page
            html_content += f"""
            <a href="{aisle_filename}" style="text-decoration: none; color: #021F00;">
                <div style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; text-align: center;">
                    <img src="{img_file}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 4px;">
                    <h3>{cat_name}</h3>
                </div>
            </a>"""

            # --- STEP 2: SIGNAL REZBOT TO BUILD THE AISLE ---
            # This triggers the resurrection of the individual category page
            rezbot.build_aisle_page(cat_name, sub_df, aisle_filename)

    # Lines 159-228 go here

    # Close the Hub Menu Grid and the Page
    html_content += """
    </div>
    </body>
    </html>"""

    try:
        if os.path.exists(output_html):
            os.remove(output_html) 
            
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"✅ OVERWRITE SUCCESS: {output_html}")
    except Exception as e:
        print(f"❌ LOCK ERROR: {e}")

if __name__ == "__main__":
    generate_ghost_mirror()
