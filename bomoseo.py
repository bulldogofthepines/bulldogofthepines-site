# bdotpseo.py
# Cleans and optimizes titles for Google and eBay SEO

def clean_title(title):
    """Strips non-standard characters and fixes spacing."""
    clean = "".join([c if ord(c) < 128 else " " for c in title])
    return " ".join(clean.split())