# condrules.py
# The "Brain" of Russet's 100% Feedback Standards

def map_condition(ebay_condition):
    """Maps eBay condition to GMC's Sacred Three while preserving raw text."""
    raw_text = str(ebay_condition)
    low_text = raw_text.lower()
    
    # --- BOT LOGIC (Keep GMC Happy) ---
    # This is your original logic, just simplified to catch 'new' safely
    if 'new' in low_text and 'other' not in low_text and 'open box' not in low_text:
        gmc_label = 'new'
    elif 'refurbished' in low_text:
        gmc_label = 'refurbished'
    else:
        gmc_label = 'used'
        
    # --- THE BUNDLE ---
    return {
        "gmc": gmc_label,
        "human": raw_text
    }

def apply_price_floor(price, min_margin=1.15):
    """Ensures we never 'Chomp' a price below our profit margin."""
    return float(price) * min_margin
