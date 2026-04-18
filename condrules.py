# condrules.py
# The "Brain" of Russet's 100% Feedback Standards

def map_condition(ebay_condition):
    """Maps eBay condition to GMC's Sacred Three."""
    if 'New' in ebay_condition and 'Other' not in ebay_condition and 'Open box' not in ebay_condition:
        return 'new'
    elif 'Refurbished' in ebay_condition:
        return 'refurbished'
    else:
        return 'used'

def apply_price_floor(price, min_margin=1.15):
    """Ensures we never 'Chomp' a price below our profit margin."""
    return float(price) * min_margin