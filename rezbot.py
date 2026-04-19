import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def build_aisle_page(cat_name, sub_df, filename):
    path = os.path.join(BASE_PATH, filename)
    
    # 1. The Aisle Header
    aisle_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://googleapis.com" rel="stylesheet">
    <meta charset="UTF-8">
    <title>{cat_name} | Bulldog of the Pines</title>
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://bulldogofthepines.com{filename}" />
    <style>
        body {{ font-family: sans-serif; background: #f4f4f4; color: #333; margin: 0; padding: 0; }}
        #product-container {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; padding: 20px; }}
        .product {{ background: white; border: 1px solid #ddd; padding: 20px; border-radius: 8px; text-align: center; }}
        img {{ max-width: 100%; height: auto; border-radius: 4px; margin: 10px 0; }}
        .price {{ font-weight: bold; color: #b12704; font-size: 1.2rem; }}
    </style>
</head>
<body>
    <!-- The Bulldog Banner -->
    <div class="banner" style="width: 100%; height: 300px; background-image: url('banner.jpg'); background-position: center; background-size: 100% 100%; background-repeat: no-repeat;"></div>
    <div style="padding: 20px;"><a href="inventory-mirror.html" style="color: #021F00; font-weight: bold; text-decoration: none;">← Back to All Categories</a></div>
    <h1 style="margin-left: 20px; color: #021F00; font-family: 'Ultra', serif; font-size: 2.5em;">{cat_name}</h1>
    <div id="product-container">"""

    # 2. The Product Logic (The DNA)
    for index, row in sub_df.iterrows():
        item_id = str(row.get('id', row.get('ItemID', 'N/A')))
        title = str(row.get('title', row.get('Title', 'N/A'))).replace('"', "'")
        image = str(row.get('image_link', row.get('Image', '')))
        price_clean = str(row.get('price', '0.00')).replace(' USD', '').replace('$', '').strip()
        human_condition = str(row.get('raw_condition', row.get('condition', 'Used')))
        ebay_url = "https://ebay.com/itm/" + item_id

        aisle_html += f"""
        <div class="product">
            <a href="{ebay_url}" target="_blank" style="text-decoration:none; color:inherit;">
                <h3>{title}</h3>
            </a>
            
            <!-- THE FIX: Wrap the image in the eBay link -->
            <a href="{ebay_url}" target="_blank">
                <img src="{image}" alt="{title}" style="max-width: 150px;">
            </a>
            
            <p class="price">${price_clean}</p>
            <p>Condition: {human_condition}</p>
            <a href="{ebay_url}" target="_blank" style="color: #0066c0; text-decoration: none; font-weight: bold;">View on eBay</a>
        </div>"""

    aisle_html += "</div></body></html>"

    # 3. The Resurrection (Overwrite the old file)
    with open(path, "w", encoding="utf-8") as f:
        f.write(aisle_html)
