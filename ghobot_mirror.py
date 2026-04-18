import pandas as pd
import os
import chompbot_fetch 

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
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bulldog Inventory Mirror</title>
    <meta name="robots" content="noindex">
    <!-- FIXED GOOGLE FONTS -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Ultra&display=swap" rel="stylesheet">
    <link rel="canonical" href="https://ebay.com" />
    <style>
        body {{ font-family: sans-serif; background: #f4f4f4; color: #333; margin: 0; padding: 0; }}
        
        .banner {{ 
            width: 100%; 
            height: 300px; 
            background-color: #cccccc; 
            background-image: url('banner.jpg');
            background-position: center;
            background-size: 100% 100%;
            background-repeat: no-repeat;
        }}

        .header-section {{ margin: 20px 0 10px 20px; }}
        
        h1 {{ 
            color: #021F00; 
            font-family: 'Ultra', serif; 
            font-size: 3.5em;
            margin: 0;
            letter-spacing: -2px; 
        }}

        .subtitle {{ 
            font-size: 1.2rem; 
            color: #666; 
            font-style: italic;
            margin-left: 5px;
        }}

        #product-container {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); 
            gap: 20px; 
            padding: 20px; 
        }}
        
        .product {{ 
            background: white; 
            border: 1px solid #ddd; 
            padding: 20px; 
            border-radius: 8px; 
            text-align: center;
            display: flex;
            flex-direction: column;
        }}

        /* FIXED TITLE OVERLAP */
        .item-title {{ 
            text-decoration: none; 
            color: #333; 
            margin-bottom: 10px;
            display: block;
            height: 4.5em; /* Gives fixed space for 3 lines of title */
            overflow: hidden;
        }}
        
        h3 {{ 
            font-size: 1.05rem; 
            margin: 0; 
            line-height: 1.3;
        }}

        .img-container {{
            height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 10px 0;
        }}

        img {{ max-width: 100%; max-height: 200px; border-radius: 4px; }}
        
        .price {{ font-weight: bold; color: #b12704; font-size: 1.2rem; margin: 10px 0; }}

        @media (max-width: 768px) {{
            h1 {{ font-size: 1.8em; letter-spacing: -1px; }}
            .banner {{ height: 35vw; }}
        }}
    </style>
</head>
<body>
    <div class="banner"></div>
    <div class="header-section">
        <h1>eBay Inventory Mirror</h1>
        <span class="subtitle">(updated daily)</span>
    </div>
    <div id="product-container">"""

    for index, row in df.iterrows():
        item_id = str(row.get('id', row.get('ItemID', 'N/A')))
        title = str(row.get('title', row.get('Title', 'N/A'))).replace('"', "'") 
        image = str(row.get('image_link', row.get('Image', '')))
        price_clean = str(row.get('price', '0.00')).replace(' USD', '').replace('$', '').strip()
        cond_raw = str(row.get('condition', 'used')).lower()
        display_condition = "New" if "new" in cond_raw else "Used"
        
        # FIXED: Added literal /itm/ and slashes
        ebay_url = "https://www.ebay.com/itm/" + item_id
        
        product_div = f"""
        <div class="product">
            <script type="application/ld+json">
            {{
              "@context": "https://schema.org",
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
                "availability": "https://schema.orgInStock",
                "itemCondition": "https://schema.org{'NewCondition' if display_condition == 'New' else 'UsedCondition'}"
              }}
            }}
            </script>
            <a href="{ebay_url}" target="_blank" class="item-title">
                <h3>{title}</h3>
            </a>
            <div class="img-container">
                <a href="{ebay_url}" target="_blank">
                    <img src="{image}" alt="{title}">
                </a>
            </div>
            <div class="info-box">
                <p class="price">${price_clean}</p>
                <p>Condition: {display_condition}</p>
                <a href="{ebay_url}" target="_blank" style="color: #0066c0; text-decoration: none; font-weight: bold;">View Item on eBay</a>
            </div>
        </div>"""
        html_content += product_div

    html_content += """
    </div>
    <script>
        window.onload = function() {
            const urlParams = new URLSearchParams(window.location.search);
            const itemId = urlParams.get('id');
            if (itemId && itemId.length > 5) {
                // FIXED: Literal redirect string
                window.location.replace("https://www.ebay.com/itm/" + itemId);
            }
        };
    </script>
</body>
</html>"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ GhoBot Success! Mirror updated at: {output_html}")

if __name__ == "__main__":
    generate_ghost_mirror()
