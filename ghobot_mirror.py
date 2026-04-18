<title>Bulldog Inventory Mirror</title>
    <meta name="robots" content="noindex">
    <link rel="canonical" href="https://ebay.com" />
    <style>
        body { font-family: sans-serif; background: #f4f4f4; color: #333; padding: 20px; }
        #product-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
        .product { background: white; border: 1px solid #ddd; padding: 20px; border-radius: 8px; text-align: center; }
        img { max-width: 100%; height: auto; border-radius: 4px; margin: 10px 0; }
        h3 { font-size: 1.1rem; height: 3.3em; overflow: hidden; }
        .price { font-weight: bold; color: #b12704; font-size: 1.2rem; }
    </style>
</head>
<body>
    <h1>Bulldog of the Pines - Live Inventory Mirror</h1>
@@ -36,21 +44,27 @@ def generate_ghost_mirror():
        item_id = str(row.get('id', row.get('ItemID', 'N/A')))
        title = str(row.get('title', row.get('Title', 'N/A'))).replace('"', "'") 
        image = str(row.get('image_link', row.get('Image', '')))
        price = str(row.get('price', '0.00')).replace(' USD', '')

        # --- THE LITERAL SLASH FIX (Added /itm/) ---
        # Force the literal string with all slashes included
        ebay_url = "https://www.ebay.com/itm/" + str(item_id)
        # Clean price for the bot (numbers only)
        price_clean = str(row.get('price', '0.00')).replace(' USD', '').replace('$', '').strip()

        # Schema URLs need the / at the end
        availability_url = "https://schema.org"
        condition_url = "https://schema.org" if row.get('condition') == 'new' else "https://schema.org"
        # Condition logic
        cond_raw = str(row.get('condition', 'used')).lower()
        display_condition = "New" if "new" in cond_raw else "Used"
        
        # eBay URL
        ebay_url = "https://www.ebay.com/itm/" + item_id
        
        # Correct Schema URLs for GMC
        schema_context = "https://schema.org"
        availability_url = "https://schema.orgInStock"
        condition_url = f"https://schema.org{'NewCondition' if display_condition == 'New' else 'UsedCondition'}"

        product_div = f"""
        <div class="product" style="border-bottom: 1px solid #eee; padding: 10px;">
        <div class="product">
            <script type="application/ld+json">
            {{
              "@context": "https://schema.org",
              "@context": "{schema_context}",
              "@type": "Product",
              "name": "{title}",
              "image": "{image}",
@@ -60,16 +74,19 @@ def generate_ghost_mirror():
                "@type": "Offer",
                "url": "{ebay_url}",
                "priceCurrency": "USD",
                "price": "{price}",
                "price": "{price_clean}",
                "availability": "{availability_url}",
                "itemCondition": "{condition_url}"
              }}
            }}
            </script>
            <h3>{title}</h3>
            <img src="{image}" style="max-width: 150px; display: block; margin: 10px 0;">
            <p>Price: {price} USD</p>
            <a href="{ebay_url}" target="_blank">View Item {item_id} on eBay</a>
            <a href="{ebay_url}" target="_blank">
                <img src="{image}" alt="{title}">
            </a>
            <p class="price">${price_clean}</p>
            <p>Condition: {display_condition}</p>
            <a href="{ebay_url}" target="_blank" style="color: #0066c0; text-decoration: none; font-weight: bold;">View Item on eBay</a>
        </div>"""
        html_content += product_div

@@ -80,7 +97,6 @@ def generate_ghost_mirror():
        const urlParams = new URLSearchParams(window.location.search);
        const itemId = urlParams.get('id');
        if (itemId) {
            // Literal string concatenation to prevent mushing
            window.location.href = "https://www.ebay.com/itm/" + itemId;
        }
    </script>
@@ -94,3 +110,6 @@ def generate_ghost_mirror():

if __name__ == "__main__":
    generate_ghost_mirror()
