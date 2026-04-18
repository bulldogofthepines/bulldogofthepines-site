# bdotpschema.py
# The Master Blueprint for all Bulldog of the Pines bots

# bdotpschema.py
COLUMNS = {
    'SKU': 'ns:SKU',
    'ItemID': 'ns:ItemID',
    'Title': 'ns:Title',
    'Price': './/ns:CurrentPrice',
    'Condition': 'ns:ConditionDisplayName',
    'Image': 'ns:PictureDetails/ns:PictureURL' 
}

# Official Schema.org URLs for GMC Compliance
# We include the trailing slash here so the bots never "mush" them
GMC_MAP = {
    'context': 'https://schema.org/',
    'in_stock': 'https://schema.org',
    'out_of_stock': 'https://schema.org',
    'condition_used': 'https://schema.org',
    'condition_new': 'https://schema.org'
}
