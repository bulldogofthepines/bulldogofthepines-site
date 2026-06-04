# datagristle.py
# The "Meat Grinder" - Separates Raw eBay Truth from GMC Sacred Three

def process_condition(raw_text):
    """
    Takes 'New other (see details)' and creates a bundle:
    1. 'gmc': Simplified (new, used, refurbished) for Google compliance.
    2. 'human': The full, original eBay text for your Mirror page.
    """
    raw = str(raw_text)
    low = raw.lower()
    
    # 1. Logic for GMC (The Robot)
    # This ensures Google always gets one of its approved keywords
    if 'new' in low:
        gmc_label = 'new'
    elif 'refurbished' in low or 'remanufactured' in low:
        gmc_label = 'refurbished'
    else:
        gmc_label = 'used'
        
    # 2. Return the "Bundle"
    return {
        "gmc": gmc_label,
        "human": raw
    }