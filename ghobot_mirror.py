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

            .search-wrapper {{ position: relative; max-width: 600px; margin: 20px; text-align: left; }}
            #masterSearch {{ width: 100%; padding: 14px 20px; border-radius: 30px; border: 2.5px solid #021F00; font-size: 16px; outline: none; }}
            #searchResults {{ position: absolute; width: 100%; background: white; z-index: 1000; border-radius: 0 0 15px 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.15); max-height: 400px; overflow-y: auto; display: none; border: 1px solid #ddd; border-top: none; }}
            
        </style>
    </head>
    <body>
        <div class="banner"></div>
        
        <!-- START DELETE: Navigation & Page Title -->
        <div style="margin: 20px 0 0 20px;">
            <a href="index.html" style="color: #021F00; text-decoration: none; font-weight: bold; font-size: 0.9em;">← Back to Home</a>
        </div>

        <!-- THE MASTER PRODUCT SEARCH -->
        <div class="search-wrapper">
            <input type="text" id="masterSearch" placeholder="Search 500+ items instantly...">
            <div id="searchResults"></div>
        </div>
    
        <h1> Shop By Category <span class="update-tag">(updates daily)</span></h1>
        <!-- END DELETE: Navigation & Page Title -->
        """ # <--- ADD THIS HERE TO CLOSE THE STRING
    
    # Build the Visual Category Grid
    html_content += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; padding: 20px; width: 100%; box-sizing: border-box;">'
        
    # --- STEP 1: BUILD THE MAIN HUB (The Menu) ---
    html_content += '<div id="category-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 20px; width: 100%;">'

    for cat_name, sub_df in grouped_data.items():
        if not sub_df.empty:
            img_file = catpro.cat_images.get(cat_name, "Other.JPG")
            safe_name = cat_name.replace(" ", "_").replace(",", "").replace("&", "")
            aisle_filename = f"{safe_name}.html"
            
            # Link to the Aisle Page
            # Hub Link Box with Fixed Height
            html_content += f"""
            <a href="{aisle_filename}" style="text-decoration: none; color: #021F00;">
                <div style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; text-align: center; height: 250px; display: flex; flex-direction: column; justify-content: space-between; align-items: center;">
                    <img src="{img_file}" style="width: 100%; height: 160px; object-fit: contain; border-radius: 4px;">
                    <h3 style="font-family: 'Ultra', serif; font-size: 1.1em; margin: 10px 0 0 0;">{cat_name}</h3>
                </div>
            </a>"""

            # --- STEP 2: SIGNAL REZBOT TO BUILD THE AISLE ---
            # This triggers the resurrection of the individual category page
            rezbot.build_aisle_page(cat_name, sub_df, aisle_filename)

    # Lines 159-228 go here

    # Close the Hub Menu Grid and the Page
    html_content += """
    
    </div>

        <script>
            let inventory = [];
            let selectedIndex = -1;
            fetch('search_index.json')
                .then(r => r.json())
                .then(data => { 
                    inventory = data;
                    // DYNAMIC UPDATE:
                    document.getElementById('masterSearch').placeholder = `Search ${inventory.length} items instantly...`;
                });
            
            const searchInput = document.getElementById('masterSearch');
            const resultsDiv = document.getElementById('searchResults');
    
            searchInput.addEventListener('input', function(e) {
                let term = e.target.value.toLowerCase().trim();
                resultsDiv.innerHTML = '';
                selectedIndex = -1;
                if (term.length < 2) { resultsDiv.style.display = 'none'; return; }
                let matches = inventory.filter(item => item.t.toLowerCase().includes(term)).slice(0, 10);
                if (matches.length > 0) {
                    resultsDiv.style.display = 'block';
                    matches.forEach((item, index) => {
                        let div = document.createElement('div');
                        div.className = 'result-item';
                        div.style = "display: flex; align-items: center; padding: 10px; border-bottom: 1px solid #eee; cursor: pointer;";
                        div.innerHTML = `<img src="${item.i}" style="width: 40px; height: 40px; margin-right: 12px; object-fit: cover; border-radius: 4px;"> <div style="font-size: 13px; color: #333;">${item.t}</div>`;
                        div.onclick = () => window.open(item.u, '_blank');
                        resultsDiv.appendChild(div);
                    });
                } else {
                    resultsDiv.innerHTML = `<div style="padding: 15px; font-size: 13px; color: #888; font-style: italic; text-align: center; background: white;">No products matching...</div>`;
                    resultsDiv.style.display = 'block';
                }
            });
    
            searchInput.addEventListener('keydown', function(e) {
                let items = resultsDiv.getElementsByClassName('result-item');
                if (e.key === 'ArrowDown') { e.preventDefault(); selectedIndex = Math.min(selectedIndex + 1, items.length - 1); updateHighlight(items); }
                else if (e.key === 'ArrowUp') { e.preventDefault(); selectedIndex = Math.max(selectedIndex - 1, -1); updateHighlight(items); }
                else if (e.key === 'Enter') {
                    if (selectedIndex > -1 && items[selectedIndex]) { items[selectedIndex].click(); }
                    else {
                        let term = e.target.value.toLowerCase().trim();
                        let matches = inventory.filter(item => item.t.toLowerCase().includes(term));
                        if (matches.length > 0) window.open(matches[0].u, '_blank');
                    }
                    searchInput.value = ''; resultsDiv.style.display = 'none';
                }
            });
    
            function updateHighlight(items) {
                for (let i = 0; i < items.length; i++) {
                    items[i].style.background = (i === selectedIndex) ? "#e9ecef" : "white";
                    if (i === selectedIndex) items[i].scrollIntoView({ block: 'nearest' });
                }
            }
            document.addEventListener('click', (e) => { if (!e.target.closest('.search-wrapper')) { resultsDiv.style.display = 'none'; searchInput.value = ''; } });
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
