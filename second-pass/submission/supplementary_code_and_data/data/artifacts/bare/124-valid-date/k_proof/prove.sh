#!/usr/bin/env bash
set -euo pipefail

# Recreate the submitted constructor term with the fixed translator, then bind
# the copied solutionProgram term in verification.k to these exact bytes.
python3 py2mpy.py solution.py > solution.mpy
printf 'fb4a7d0caadab15af3f85da978c9739d8db1e71ec10e5efe2ab9d84d3b8d1b8a  solution.mpy\n' | sha256sum --check

# Compile the executable semantics and confirm that solution.mpy parses as a
# Program under the constructor grammar.
kompile semantic.k --main-module MPY --syntax-module MPY --backend haskell
kast --definition semantic-kompiled --input program --sort Program solution.mpy >/dev/null

# Concrete executions through distinct contract paths.
krun --definition semantic-kompiled -cPGM="runProgram($(tr '\n' ' ' < solution.mpy), \"valid_date\", vals(strVal(\"03-11-2000\")))" --output program
krun --definition semantic-kompiled -cPGM="runProgram($(tr '\n' ' ' < solution.mpy), \"valid_date\", vals(strVal(\"15-01-2012\")))" --output program
krun --definition semantic-kompiled -cPGM="runProgram($(tr '\n' ' ' < solution.mpy), \"valid_date\", vals(strVal(\"04-0-2040\")))" --output program
krun --definition semantic-kompiled -cPGM="runProgram($(tr '\n' ' ' < solution.mpy), \"valid_date\", vals(strVal(\"06-04-2020\")))" --output program
krun --definition semantic-kompiled -cPGM="runProgram($(tr '\n' ' ' < solution.mpy), \"valid_date\", vals(strVal(\"06/04/2020\")))" --output program
krun --definition semantic-kompiled -cPGM="runProgram($(tr '\n' ' ' < solution.mpy), \"valid_date\", vals(strVal(\"02-29-1900\")))" --output program
krun --definition semantic-kompiled -cPGM="runProgram($(tr '\n' ' ' < solution.mpy), \"valid_date\", vals(strVal(\"02-30-2020\")))" --output program

# Compile the independent contract layer and prove every claim in spec.k.
kompile verification.k --main-module VERIFICATION --syntax-module VERIFICATION --backend haskell
kprove spec.k --definition verification-kompiled --spec-module VALID-DATE-SPEC --smt-timeout 5000
