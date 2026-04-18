import pandas as pd
import os
import chompbot_fetch  # This links GhoBot to your sweep script

# 1. Setup the Home Base
BASE_PATH = r'C:\Users\durge\OneDrive\Desktop\BoMaMeMo'
latest_csv = os.path.join(BASE_PATH, "latest_inventory.csv")
output_html = os.path.join(BASE_PATH, "inventory-mirror.html")

def generate_ghost_mirror():
    # --- STEP 1: AUTO-RUN THE SWEEP ---
    print("🔄 GhoBot is signaling ChOmpBot to start the sweep...")
    chompbot_fetch.get_full_inventory() 
    print("✅ Sweep successful. Now building the Mirror...")

    # --- STEP 2: BUILD THE HTML ---
    if not os.path.exists(latest_csv):
        print("❌ Error: latest_inventory.csv not found.")
        return

    df = pd.read_csv(latest_csv)
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bulldog Inventory Mirror</title>
    <meta name="robots" content="noindex">
</head>
<body>
    <h1>Bulldog of the Pines - Live Inventory Mirror</h1>
    <div id="product-container">"""

    for index, row in df.iterrows():
        item_id = str(row.get('id', row.get('ItemID', 'N/A')))
        title = str(row.get('title', row.get('Title', 'N/A'))).replace('"', "'") 
        image = str(row.get('image_link', row.get('Image', '')))
        price = str(row.get('price', '0.00')).replace(' USD', '')
        
        # --- THE LITERAL SLASH FIX (Added /itm/) ---
        # Force the literal string with all slashes included
        ebay_url = "https://www.ebay.com/itm/" + str(item_id)
        
        # Schema URLs need the / at the end
        availability_url = "https://schema.org"
        condition_url = "https://schema.org" if row.get('condition') == 'new' else "https://schema.org"
        
        product_div = f"""
        <div class="product" style="border-bottom: 1px solid #eee; padding: 10px;">
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
                "price": "{price}",
                "availability": "{availability_url}",
                "itemCondition": "{condition_url}"
              }}
            }}
            </script>
            <h3>{title}</h3>
            <img src="{image}" style="max-width: 150px; display: block; margin: 10px 0;">
            <p>Price: {price} USD</p>
            <a href="{ebay_url}" target="_blank">View Item {item_id} on eBay</a>
        </div>"""
        html_content += product_div

    # Close the container and add the redirect script
    html_content += """
    </div>
    <script>
        const urlParams = new URLSearchParams(window.location.search);
        const itemId = urlParams.get('id');
        if (itemId) {
            // Literal string concatenation to prevent mushing
            window.location.href = "https://www.ebay.com/itm/" + itemId;
        }
    </script>
</body>
</html>"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ GhoBot Success! Mirror created at: {output_html}")

if __name__ == "__main__":
    generate_ghost_mirror()