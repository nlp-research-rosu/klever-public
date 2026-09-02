sed -n '1,320p' /reference/tools/k_rule_inventory.py
printf '\nLEMMA DISCOVERY CONTRACT\n'
sed -n '1,360p' /reference/tools/lemma_discovery_contract.py
printf '\nKLEAN PREFLIGHT SIGNATURES\n'
rg -n '^(def |class |GENERATION|ALLOWED|STATUS|TARGET|OBLIGATION)' /reference/tools/klean_preflight.py
sed -n '1,420p' /reference/tools/klean_preflight.py
