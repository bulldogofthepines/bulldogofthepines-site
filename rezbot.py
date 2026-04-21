import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def build_aisle_page(cat_name, sub_df, filename):
    path = os.path.join(BASE_PATH, filename)
    
    # NEW: Create the drawer for individual item pages to keep the repo clean
    items_dir = os.path.join(BASE_PATH, 'items')
    if not os.path.exists(items_dir):
        os.makedirs(items_dir)

    # 1. The Aisle Header (Remains the same)
    aisle_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://googleapis.com" rel="stylesheet">
    <meta charset="UTF-8">
    <title>{cat_name} | Bulldog of the Pines</title>
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://bulldogofthepines.com/{filename}" />
    <style>
        body {{ font-family: sans-serif; background: #f4f4f4; color: #333; margin: 0; padding: 0; }}
        #product-container {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; padding: 20px; }}
        .product {{ background: white; border: 1px solid #ddd; padding: 20px; border-radius: 8px; text-align: center; }}
        img {{ max-width: 100%; height: auto; border-radius: 4px; margin: 10px 0; }}
        .price {{ font-weight: bold; color: #b12704; font-size: 1.2rem; }}
        .search-wrapper {{ padding: 0 20px; margin-top: 20px; }}
        #searchInput {{ width: 100%; max-width: 500px; padding: 12px; border-radius: 25px; border: 2px solid #021F00; font-size: 16px; outline: none; }}
    </style>
    <script>
        function filterProducts() {{
            let input = document.getElementById('searchInput').value.toLowerCase();
            let products = document.getElementsByClassName('product');
            for (let i = 0; i < products.length; i++) {{
                let title = products[i].getElementsByTagName('h3')[0].innerText.toLowerCase();
                if (title.includes(input)) {{ products[i].style.display = ""; }}
                else {{ products[i].style.display = "none"; }}
            }}
        }}
    </script>
</head>
<body>
    <div class="banner" style="width: 100%; height: 300px; background-image: url('banner.jpg'); background-position: center; background-size: 100% 100%; background-repeat: no-repeat;"></div>
    <div style="padding: 20px;"><a href="inventory-mirror.html" style="color: #021F00; font-weight: bold; text-decoration: none;">← Back to All Categories</a></div>
    <div class="search-wrapper">
        <input type="text" id="searchInput" onkeyup="filterProducts()" placeholder="Search {cat_name}...">
    </div>
    <h1 style="margin-left: 20px; color: #021F00; font-family: 'Ultra', serif; font-size: 2.5em;">{cat_name}</h1>
    <div id="product-container">"""

    # 2. The Product Logic
    # Inside the rezbot.py product loop:
    for index, row in sub_df.iterrows():
        # FIRST: Capture all the raw data from the row
        item_id = str(row.get('id', row.get('ItemID', '')))
        title = str(row.get('title', row.get('Title', ''))).replace('"', "'")
        image = str(row.get('image_link', row.get('Image', '')))
        price_val = str(row.get('price', '0.00')).replace(' USD', '').replace('$', '').strip()
        gmc_condition = str(row.get('condition', 'used')).lower()
        
        # SECOND: Define the human condition BEFORE using it in the description
        human_condition = str(row.get('raw_condition', row.get('condition', 'Used')))
        
        # THIRD: Now build the strings that use those variables
        ebay_url = f"https://ebay.com{item_id}"
        full_desc = f"Quality item from Bulldog of the Pines: {title}. eBay Condition: {human_condition}"

        # --- THE PERMANENT FLOOR SIDE MISSION ---

        # 1. ADD THIS LINE: Build the identical twin string to match ChOmpBot
        full_desc = f"Quality item from Bulldog of the Pines: {title}. eBay Condition: {human_condition}"
        
        # Generate a tiny static landing page for Google (and direct user redirect)
        item_page_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <meta http-equiv="refresh" content="0; url=https://ebay.com/{item_id}">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": "{title}",
      "image": "{image}",
      "description": "{full_desc}",
      "sku": "{item_id}",
      "brand": {{ "@type": "Brand", "name": "Bulldog of the Pines" }},
      "offers": {{
        "@type": "Offer",
        "url": "https://ebay.com/{item_id}",
        "priceCurrency": "USD",
        "price": "{price_val}",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/{'NewCondition' if gmc_condition == 'new' else 'UsedCondition'}""
      }}
    }}
    </script>
</head>
<body>Redirecting to eBay... <a href="{ebay_url}">Click here</a></body>
</html>"""
        
        # Write the tiny file to /items/[item_id].html
        with open(os.path.join(items_dir, f"{item_id}.html"), "w", encoding="utf-8") as f:
            f.write(item_page_html)
        # --- END SIDE MISSION ---

        # The Aisle Display (Keep your original grid layout)
        aisle_html += f"""
        <div class="product">
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

    aisle_html += "</div></body></html>"

    with open(path, "w", encoding="utf-8") as f:
        f.write(aisle_html)
