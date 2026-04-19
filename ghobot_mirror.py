import pandas as pd
import os
import chompbot_fetch 
import catpro  # Logic for the Bulldog Buckets

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
    
        <h1>Available Items <span class="update-tag">(updates daily)</span></h1>
        <!-- END DELETE: Navigation & Page Title -->
        """ # <--- ADD THIS HERE TO CLOSE THE STRING
    
    # Build the Visual Category Grid
    html_content += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; padding: 20px;">'
        
    # --- STEP 1: BUILD THE MAIN HUB (The Menu) ---
    hub_html = "<h1>Shop by Category</h1>"
    hub_html += '<div id="category-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 20px;">'

    for cat_name, sub_df in grouped_data.items():
        if not sub_df.empty:
            # Match your GitHub image titles
            img_file = catpro.cat_images.get(cat_name, "Other.JPG")
            # Create a clean filename for the aisle page
            safe_name = cat_name.replace(" ", "_").replace(",", "").replace("&", "")
            aisle_filename = f"{safe_name}.html"
            
            # Add to the Hub Menu
            hub_html += f"""
            <a href="{aisle_filename}" style="text-decoration: none; color: #021F00;">
                <div style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; text-align: center;">
                    <img src="{img_file}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 4px;">
                    <h3>{cat_name}</h3>
                    <p>{len(sub_df)} Items Available</p>
                </div>
            </a>"""

            # --- STEP 2: BUILD THE INDIVIDUAL AISLE PAGE ---
            # This wipes the old file and creates the new one with current items
            build_aisle_page(cat_name, sub_df, aisle_filename)

    hub_html += '</div>'

    # NEXT: Open the product container (Notice the += and NO f(plus 3 quotes) template reset)
    html_content += '<div id="product-container">'

    # START: The Item Loop
    for cat_name, sub_df in grouped_data.items():
        if not sub_df.empty:
            # 1. Add the Category Header (With the ID for the Jump Link)
            safe_id = cat_name.replace(" ", "").replace(",", "").replace("&", "")
            # 2. Inject that ID into the header div
            html_content += f'<div id="{safe_id}" class="category-header" style="grid-column: 1/-1; background: #021F00; color: white; padding: 15px; margin: 20px 0; border-radius: 8px; font-family: Ultra, serif;">{cat_name}</div>'
            
            for index, row in sub_df.iterrows():
                # 1. Define all data variables FIRST
                item_id = str(row.get('id', row.get('ItemID', 'N/A')))
                title = str(row.get('title', row.get('Title', 'N/A'))).replace('"', "'")
                image = str(row.get('image_link', row.get('Image', '')))
                price_clean = str(row.get('price', '0.00')).replace(' USD', '').replace('$', '').strip()
                human_condition = str(row.get('raw_condition', row.get('condition', 'Used')))
                is_new = "new" in human_condition.lower()
                display_condition = "New" if is_new else "Used"
                ebay_url = "https://www.ebay.com/itm/" + item_id
                schema_context = "https://schema.org/"
                availability_url = "https://schema.org/InStock"
                condition_url = f"https://schema.org/{'NewCondition' if display_condition == 'New' else 'UsedCondition'}"

                # 2. Build the product HTML string SECOND
                product_div = f"""
                <div class="product">
                    <script type="application/ld+json">
                        {{
                        "@context": "{schema_context}",
                        "@type": "Product",
                        "name": "{title}",
                        "image": "{image}",
                        "description": "{row.get('description', 'Quality Part')}",
                        "sku": "{row.get('SKU', 'N/A')}",
                        "offers": {{
                            "@type": "Offer",
                            "url": "{ebay_url}",
                            "priceCurrency": "USD",
                            "price": "{price_clean}",
                            "availability": "{availability_url}",
                            "itemCondition": "{condition_url}"
                            }}
                        }}
                    </script>
                    <a href="{ebay_url}" target="_blank" style="text-decoration:none; color:inherit;">
                    <h3>{title}</h3>
                    </a>
                    <a href="{ebay_url}" target="_blank">
                        <img src="{image}" alt="{title}" style="max-width: 150px;">
                    </a>
                    <p class="price">${price_clean}</p>
                    <p>Condition: {human_condition}</p>
                    <a href="{ebay_url}" target="_blank" style="color: #0066c0; text-decoration: none; font-weight: bold;">View on eBay</a>
                </div>"""

                # 3. Add to the page content LAST
                html_content += product_div

            # --- EXIT BOTH LOOPS HERE ---
            html_content += "</div>" # This closes the #product-container grid once.

        html_content += """ 
        <script>
            const urlParams = new URLSearchParams(window.location.search);
            const itemId = urlParams.get('id');
            if (itemId) {
                window.location.href = "https://www.ebay.com/itm/" + itemId;
            }
        </script>
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
