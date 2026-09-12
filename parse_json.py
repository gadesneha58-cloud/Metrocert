import json
import re

json_data = """
{
  "mpe_reference": {
    "standard": "OIML R76",
    "note": "n = load / e (verification scale interval). Apply mpe at whichever load band the test point falls in.",
    "initial_verification": [
      { "n_min": 0,    "n_max": 500,   "mpe_in_e": 0.5 },
      { "n_min": 500,  "n_max": 2000,  "mpe_in_e": 1.0 },
      { "n_min": 2000, "n_max": 10000, "mpe_in_e": 1.5 }
    ],
    "in_service_verification": [
      { "n_min": 0,    "n_max": 500,   "mpe_in_e": 1.0 },
      { "n_min": 500,  "n_max": 2000,  "mpe_in_e": 2.0 },
      { "n_min": 2000, "n_max": 10000, "mpe_in_e": 3.0 }
    ]
  },
  "models": [
    { "manufacturer": "Mettler Toledo", "model": "XPR205", "category": "Analytical Balance", "max": "220 g", "min": "10 mg", "e": "0.01 mg", "d": "0.01 mg", "class": "I" },
    { "manufacturer": "Mettler Toledo", "model": "XSR204", "category": "Analytical Balance", "max": "220 g", "min": "10 mg", "e": "0.1 mg", "d": "0.1 mg", "class": "I" },
    { "manufacturer": "Mettler Toledo", "model": "ME204", "category": "Analytical Balance", "max": "220 g", "min": "10 mg", "e": "0.1 mg", "d": "0.1 mg", "class": "I" },
    { "manufacturer": "Mettler Toledo", "model": "BC60", "category": "Bench/Shipping Scale", "max": "150 lb", "min": "0.2 lb", "e": "0.05 lb", "d": "0.05 lb", "class": "III" },
    { "manufacturer": "Mettler Toledo", "model": "JL602-GE/A", "category": "Jewellery Scale", "max": "610 g", "min": "0.2 g", "e": "0.01 g", "d": "0.01 g", "class": "II" },
    { "manufacturer": "Mettler Toledo", "model": "JL6001GE/A", "category": "Jewellery/Precision Scale", "max": "6200 g", "min": "2 g", "e": "0.1 g", "d": "0.1 g", "class": "II" },
    { "manufacturer": "Mettler Toledo", "model": "IND231", "category": "Platform Scale (indicator+platform)", "max": "1500 kg", "min": "10 kg", "e": "0.5 kg", "d": "0.5 kg", "class": "III" },
    { "manufacturer": "Ohaus", "model": "Explorer EX12001", "category": "Precision Balance", "max": "12000 g", "min": "1 g", "e": "0.1 g", "d": "0.1 g", "class": "II" },
    { "manufacturer": "Ohaus", "model": "Explorer EX35001", "category": "Precision Balance", "max": "35000 g", "min": "5 g", "e": "0.1 g", "d": "0.1 g", "class": "III" },
    { "manufacturer": "Ohaus", "model": "Adventurer AX8201/E", "category": "Precision Balance (NTEP)", "max": "8200 g", "min": "5 g", "e": "0.1 g", "d": "0.1 g", "class": "III" },
    { "manufacturer": "Ohaus", "model": "Pioneer PX2202", "category": "Precision Balance", "max": "2200 g", "min": "0.5 g", "e": "0.01 g", "d": "0.01 g", "class": "II" },
    { "manufacturer": "Ohaus", "model": "Scout SJX1502N/E", "category": "Precision Balance (NTEP)", "max": "1500 g", "min": "0.5 g", "e": "0.01 g", "d": "0.01 g", "class": "II" },
    { "manufacturer": "Ohaus", "model": "Scout SJX6201N/E", "category": "Precision Balance (NTEP)", "max": "6200 g", "min": "10 g", "e": "1 g", "d": "1 g", "class": "III" },
    { "manufacturer": "Ohaus", "model": "Voyager Pro CX", "category": "Precision Balance", "max": "8200 g", "min": "1 g", "e": "0.01 g", "d": "0.01 g", "class": "I" },
    { "manufacturer": "Sartorius", "model": "Practum 224-1S", "category": "Analytical Balance", "max": "220 g", "min": "10 mg", "e": "0.1 mg", "d": "0.1 mg", "class": "I" },
    { "manufacturer": "Sartorius", "model": "Secura 225D-1S", "category": "Analytical Balance", "max": "220 g", "min": "1 mg", "e": "0.01 mg", "d": "0.01 mg", "class": "I" },
    { "manufacturer": "Sartorius", "model": "Cubis II MSA225S", "category": "Analytical Balance", "max": "220 g", "min": "1 mg", "e": "0.01 mg", "d": "0.01 mg", "class": "I" },
    { "manufacturer": "Sartorius", "model": "Entris II BCE224i", "category": "Analytical Balance", "max": "220 g", "min": "10 mg", "e": "0.1 mg", "d": "0.1 mg", "class": "I" },
    { "manufacturer": "Kern", "model": "ABJ 220-4M", "category": "Analytical Balance", "max": "220 g", "min": "10 mg", "e": "0.1 mg", "d": "0.1 mg", "class": "I" },
    { "manufacturer": "Kern", "model": "EW 6000-1M", "category": "Precision Balance", "max": "6000 g", "min": "1 g", "e": "0.1 g", "d": "0.1 g", "class": "II" },
    { "manufacturer": "A&D Company", "model": "GX-6100", "category": "Precision Balance", "max": "6100 g", "min": "1 g", "e": "0.01 g", "d": "0.01 g", "class": "II" },
    { "manufacturer": "A&D Company", "model": "FX-300i", "category": "Precision Balance", "max": "320 g", "min": "0.1 g", "e": "1 mg", "d": "1 mg", "class": "I" },
    { "manufacturer": "Radwag", "model": "AS 220.R2", "category": "Analytical Balance", "max": "220 g", "min": "10 mg", "e": "0.1 mg", "d": "0.1 mg", "class": "I" },
    { "manufacturer": "GemOro", "model": "Platinum PRO1601", "category": "Jewellery Scale", "max": "1600 g", "min": "0.1 g", "e": "0.1 g", "d": "0.1 g", "class": "N/A (non-verified)" },
    { "manufacturer": "GemOro", "model": "Platinum XP500", "category": "Jewellery Scale", "max": "500 g", "min": "0.05 g", "e": "0.01 g", "d": "0.01 g", "class": "N/A (non-verified)" },
    { "manufacturer": "Essae", "model": "DJ-320", "category": "Jewellery Scale", "max": "320/620/1000 g", "min": "0.5 g", "e": "0.001 g", "d": "0.001 g", "class": "II" },
    { "manufacturer": "American Weigh Scales", "model": "AWS-100", "category": "Jewellery Scale", "max": "100 g", "min": "0.1 g", "e": "0.01 g", "d": "0.01 g", "class": "N/A (non-verified)" },
    { "manufacturer": "CAS Corp", "model": "SW-1", "category": "Jewellery Scale", "max": "200 g", "min": "0.5 g", "e": "0.01 g", "d": "0.01 g", "class": "II" },
    { "manufacturer": "Essae", "model": "DS-215HD", "category": "Retail Counter Scale", "max": "30/60/100 kg", "min": "40 g", "e": "5 g", "d": "5 g", "class": "III" },
    { "manufacturer": "Essae", "model": "DS-215SS", "category": "Retail Counter Scale", "max": "100 kg", "min": "40 g", "e": "5 g", "d": "5 g", "class": "III" },
    { "manufacturer": "Essae", "model": "DS-75", "category": "Retail Counter Scale", "max": "30 kg", "min": "20 g", "e": "5 g", "d": "5 g", "class": "III" },
    { "manufacturer": "Essae", "model": "DS-252PR", "category": "Retail Label-Printing Scale", "max": "30 kg", "min": "20 g", "e": "2/5 g", "d": "2/5 g", "class": "III" },
    { "manufacturer": "CAS Corp", "model": "AP-1", "category": "Retail Counter Scale", "max": "15/30 kg", "min": "20 g", "e": "2/5 g", "d": "2/5 g", "class": "III" },
    { "manufacturer": "CAS Corp", "model": "ER Plus", "category": "Retail Counter Scale", "max": "6/15/30 kg", "min": "10 g", "e": "1/2 g", "d": "1/2 g", "class": "III" },
    { "manufacturer": "Avery Berkel", "model": "FX50/FX120", "category": "Retail Counter Scale", "max": "6/30 kg", "min": "10 g", "e": "1/2 g", "d": "1/2 g", "class": "III" },
    { "manufacturer": "Contech", "model": "CS-500", "category": "Retail Counter Scale", "max": "30 kg", "min": "20 g", "e": "5 g", "d": "5 g", "class": "III" },
    { "manufacturer": "Salter Brecknell", "model": "6710U", "category": "Retail Counter Scale", "max": "30 lb", "min": "0.1 lb", "e": "0.01 lb", "d": "0.01 lb", "class": "III" },
    { "manufacturer": "Essae", "model": "DX-415N", "category": "Platform/Floor Scale", "max": "up to 5000 kg", "min": "20 kg", "e": "1000 g", "d": "1000 g", "class": "IIII" },
    { "manufacturer": "Essae", "model": "DX-852", "category": "Bench Scale", "max": "6 kg", "min": "4 g", "e": "0.2 g", "d": "0.2 g", "class": "III" },
    { "manufacturer": "Essae", "model": "DX-215", "category": "Platform Scale", "max": "100-1000 kg", "min": "1 kg", "e": "50-200 g", "d": "50-200 g", "class": "IIII" },
    { "manufacturer": "Adam Equipment", "model": "CPWplus 200", "category": "Platform Scale", "max": "200 kg", "min": "0.2 kg", "e": "0.1 kg", "d": "0.1 kg", "class": "III" },
    { "manufacturer": "Adam Equipment", "model": "GBK 60a", "category": "Bench Scale", "max": "60 kg", "min": "0.04 kg", "e": "0.01 kg", "d": "0.01 kg", "class": "III" },
    { "manufacturer": "Avery Weigh-Tronix", "model": "ZM303", "category": "Platform Scale", "max": "up to 1000 kg", "min": "4 kg", "e": "0.2 kg", "d": "0.2 kg", "class": "III" },
    { "manufacturer": "Avery Weigh-Tronix", "model": "PS Series", "category": "Floor Scale", "max": "up to 3000 kg", "min": "20 kg", "e": "0.5-1 kg", "d": "0.5-1 kg", "class": "IIII" },
    { "manufacturer": "Rice Lake", "model": "RL1250", "category": "Floor Scale", "max": "up to 5000 lb", "min": "40 lb", "e": "1 lb", "d": "1 lb", "class": "III" },
    { "manufacturer": "Avery Weigh-Tronix", "model": "LS1000", "category": "Crane Scale", "max": "up to 10000 kg", "min": "40 kg", "e": "2-5 kg", "d": "2-5 kg", "class": "IIII" },
    { "manufacturer": "Essae", "model": "Weighbridge (pit-type)", "category": "Weighbridge", "max": "20000-100000 kg", "min": "400 kg", "e": "10-20 kg", "d": "10-20 kg", "class": "IIII" },
    { "manufacturer": "Rice Lake", "model": "SURVIVOR OTR", "category": "Weighbridge", "max": "up to 80000 kg", "min": "800 kg", "e": "20 kg", "d": "20 kg", "class": "IIII" },
    { "manufacturer": "Gallagher", "model": "W210", "category": "Livestock Scale", "max": "up to 2000 kg", "min": "20 kg", "e": "0.5-1 kg", "d": "0.5-1 kg", "class": "IIII" },
    { "manufacturer": "Mettler Toledo", "model": "PS Series", "category": "Postal/Shipping Scale", "max": "up to 300 kg", "min": "2 kg", "e": "0.1-1 kg", "d": "0.1-1 kg", "class": "III" }
  ]
}
"""

data = json.loads(json_data)

def parse_val(s):
    # returns value (in base unit g or kg depending on what it is, actually let's just return the numeric value and unit)
    # let's try to normalize everything to kg or g?
    # No, keep the unit that max is in.
    pass

items = []
for d in data['models']:
    # parse max
    max_s = d['max'].replace('up to ', '')
    # handle 30/60/100 -> pick highest
    max_val_str = max_s.split(' ')[0].split('-')[-1].split('/')[-1]
    max_unit = max_s.split(' ')[1]
    max_val = float(max_val_str)
    
    def to_base(val_str, unit, base_unit):
        val = float(val_str)
        if base_unit == unit: return val
        if base_unit == 'g' and unit == 'mg': return val / 1000.0
        if base_unit == 'g' and unit == 'kg': return val * 1000.0
        if base_unit == 'kg' and unit == 'g': return val / 1000.0
        if base_unit == 'kg' and unit == 'mg': return val / 1000000.0
        if base_unit == 'mg' and unit == 'g': return val * 1000.0
        return val # fallback (lb to lb)

    # min
    min_s = d['min'].split(' ')
    min_val_str = min_s[0].split('-')[-1].split('/')[-1]
    min_val = to_base(min_val_str, min_s[1], max_unit)
    
    # e
    e_s = d['e'].split(' ')
    e_val_str = e_s[0].split('-')[-1].split('/')[-1]
    e_val = to_base(e_val_str, e_s[1], max_unit)
    
    # d_s
    d_s = d['d'].split(' ')
    d_val_str = d_s[0].split('-')[-1].split('/')[-1]
    d_val = to_base(d_val_str, d_s[1], max_unit)
    
    items.append(f'InstrumentCatalogItem("{d["manufacturer"]}", "{d["model"]}", "{d["category"]}", "{d["class"]}", {max_val}, {min_val}, "{max_unit}", {e_val}, {d_val})')

kotlin_code = "val seedData = listOf(\n    " + ",\n    ".join(items) + "\n)"

# now inject this into MetroCertViewModel.kt
with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'r') as f:
    content = f.read()

import re
# Find fetchOrSeedCatalog
start = content.find("val seedData = listOf(")
end = content.find(")", start) + 1
if start != -1:
    content = content[:start] + kotlin_code + content[end:]
else:
    print("Could not find seedData list")

with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'w') as f:
    f.write(content)
