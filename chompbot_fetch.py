import requests
import pandas as pd
import xml.etree.ElementTree as ET
import time
import bdotptoken as keys
import bdotpschema as schema
import condrules as rules
import bomoseo as seo
import os
import json
from datetime import datetime

# 1. Setup the Home Base (OneDrive Desktop)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BACKUP_FOLDER = os.path.join(BASE_PATH, 'inventory_backups')

# 2. Create the folder if it's missing
if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)

# 3. Setup the timestamp
STAMP = datetime.now().strftime("%Y-%m-%d_%H-%M")

def get_full_inventory():
    url = "https://api.ebay.com/ws/api.dll"
    all_items = []
    page_number = 1
    
    print("🚀 ChOmpBot is starting the modular stealth sweep...")

    while True:
        headers = {
            "X-EBAY-API-SITEID": "0",
            "X-EBAY-API-COMPATIBILITY-LEVEL": "1085",
            "X-EBAY-API-CALL-NAME": "GetSellerList",
            "X-EBAY-API-APP-NAME": keys.APP_ID,
            "X-EBAY-API-DEV-NAME": keys.DEV_ID,
            "X-EBAY-API-CERT-NAME": keys.CERT_ID,
            "Content-Type": "text/xml",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36",
        }

        # --- HIGH DETAIL REQUEST ---
        body = f"""<?xml version="1.0" encoding="utf-8"?>
<GetSellerListRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RequesterCredentials><eBayAuthToken>{keys.TOKEN.strip()}</eBayAuthToken></RequesterCredentials>
    <EndTimeFrom>{time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}</EndTimeFrom>
    <EndTimeTo>{time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 120*24*3600))}</EndTimeTo>
    <Pagination>
        <EntriesPerPage>200</EntriesPerPage>
        <PageNumber>{page_number}</PageNumber>
    </Pagination>
    <DetailLevel>ReturnAll</DetailLevel>
    <GranularityLevel>Fine</GranularityLevel>
</GetSellerListRequest>"""

        response = requests.post(url, data=body.encode('utf-8'), headers=headers)
        
        if "<?xml" in response.text or "<GetSellerListResponse" in response.text:
            root = ET.fromstring(response.content)
            namespace = {'ns': 'urn:ebay:apis:eBLBaseComponents'}
            items = root.findall('.//ns:Item', namespace)
            if not items: break

            for item in items:
                item_id = str(item.findtext(schema.COLUMNS['ItemID'], namespaces=namespace)).strip()
                
                # 1. Grab the raw text from eBay (e.g., "New other (see details)")
                raw_ebay_condition = item.findtext(schema.COLUMNS['Condition'], default='Used', namespaces=namespace)
                
                # 2. Get the "Bundle" from your upgraded condrules.py
                cond_bundle = rules.map_condition(raw_ebay_condition) 
                
                clean_title = seo.clean_title(item.findtext(schema.COLUMNS['Title'], namespaces=namespace))

                # Pull the Category Name from the eBay XML
                category_name = item.findtext(schema.COLUMNS['CategoryName'], default='Other', namespaces=namespace)

                all_items.append({
                    'SKU': item.findtext(schema.COLUMNS['SKU'], default='N/A', namespaces=namespace),
                    'id': item_id,
                    'title': clean_title,
                    'CategoryName': category_name,  # <--- ADD THIS LINE for Cats
                    'description': f"Quality part from Bulldog of the Pines. eBay Condition: {raw_ebay_condition}",
                    'link': f"https://bulldogofthepines.com{item_id}",
                    'image_link': item.findtext(schema.COLUMNS['Image'], default="https://bulldogofthepines.com", namespaces=namespace),
                    'price': f"{item.findtext(schema.COLUMNS['Price'], namespaces=namespace)} USD",
                    'availability': 'in_stock',
                    # --- THE DOUBLE-TRACK SPLIT ---
                    'condition': cond_bundle['gmc'],     # 'new', 'used', or 'refurbished' for Google
                    'raw_condition': cond_bundle['human'] # The full eBay text for your Mirror
                })

            print(f"Bagged {len(all_items)} items...")
            total_pages = int(root.findtext('.//ns:TotalNumberOfPages', default='1', namespaces=namespace))
            if page_number >= total_pages: break
            page_number += 1
            time.sleep(1) 
        else:
            print("❌ Connection blocked by HTML wall.")
            break

    if all_items:
        df_master = pd.DataFrame(all_items)
        
        # Save files
        df_master.to_csv(os.path.join(BACKUP_FOLDER, f"bulldog_inventory_{STAMP}.csv"), index=False)
        df_master.to_csv(os.path.join(BASE_PATH, "latest_inventory.csv"), index=False)
        
        # GMC specific upload file (only needs the bot-friendly 'condition' column)
        google_cols = ['id', 'title', 'description', 'link', 'image_link', 'price', 'availability', 'condition']
        df_google = df_master[google_cols]
        df_google.to_csv(os.path.join(BACKUP_FOLDER, f"GMC_Upload_{STAMP}.csv"), index=False)

        # Build the lightweight Search Index for the Dropdown UI
        search_data = []
        for item in all_items:
            search_data.append({
                "t": item['title'],
                "i": item['image_link'],
                "u": f"https://ebay.com{item['id']}"
            })

        with open(os.path.join(BASE_PATH, "search_index.json"), "w", encoding="utf-8") as f:
            json.dump(search_data, f)
        
        print(f"✅ MISSION COMPLETE! Files in: {BASE_PATH}")
    else:
        print("🤷 No data found.")

if __name__ == "__main__":
    get_full_inventory()

if __name__ == "__main__":
    get_full_inventory()
