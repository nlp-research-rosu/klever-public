The first inventory-generation diagnostic incorrectly treated indented rule
guards beginning with `requires` as top-level declarations. The generated TSV
was immediately overwritten after the parser was corrected. The authoritative
generation is `05-rule-inventory-generation.log`; its 705 rule and 233 syntax
counts are independently reconciled in `05-rule-inventory-validation.log`.
