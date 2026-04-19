import pandas as pd

# The Visual Mapping in catpro.py
cat_images = {
    "Business & Industrial": "Industrial.JPG",
    "Clothing, Shoes & Accessories": "Clothing.jpg",
    "eBay Motors": "Auto_Parts.JPG",
    "Toys & Hobbies": "Toys_Hobbies.jpg",
    "Home & Garden": "Home_Garden.jpg",
    "Other": "Other.JPG"
}

def group_inventory_by_cat(df):
    # Your target buckets
    target_cats = [
        "Business & Industrial", 
        "Clothing, Shoes & Accessories", 
        "eBay Motors", 
        "Toys & Hobbies", 
        "Home & Garden"
    ]
    
    # Extract the top-level category from 'CategoryName'
    # Uses .str.split(':').str[0] to handle the whole column at once
    df['TopCat'] = df['CategoryName'].fillna('Other').str.split(':').str[0].str.strip()
    
    # Map anything not in your list to 'Other'
    df.loc[~df['TopCat'].isin(target_cats), 'TopCat'] = 'Other'
    
    # Split into a dictionary of dataframes { 'CategoryName': sub_df }
    grouped = {cat: df[df['TopCat'] == cat] for cat in target_cats + ["Other"]}
    
    return grouped
