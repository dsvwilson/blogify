import requests

# fetch the current TLDs from the IANA website, remove the comment at the top of the page, save in a set, append a "." to each element, and convert the text to lowercase.

tlds_data = requests.get("https://data.iana.org/TLD/tlds-alpha-by-domain.txt")
tlds = []

for tld in tlds_data.text.splitlines():
    if not tld.startswith("#"):
        tlds.append("." + tld.lower())