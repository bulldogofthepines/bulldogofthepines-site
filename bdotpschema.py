# bdotpschema.py
# The Master Blueprint for all Bulldog of the Pines bots

# bdotpschema.py
COLUMNS = {
    'SKU': 'ns:SKU',
    'ItemID': 'ns:ItemID',
    'Title': 'ns:Title',
    'Price': './/ns:CurrentPrice',
    'Condition': 'ns:ConditionDisplayName',
    # ADD THIS LINE:
    'Image': 'ns:PictureDetails/ns:PictureURL' 
}

# GMC Requirements for the "Sacred Three" Mapping
GMC_CONDITIONS = {
    'new': 'new',
    'refurbished': 'refurbished',
    'used': 'used'
}