#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor term with the supplied, unmodified translator.
python3 py2mpy.py solution.py > solution.mpy

# Concrete backend and all examples from prompt.py.
kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX
krun solution.mpy -cINPUT='lbr lbr rbr rbr .BString' --definition semantic-kompiled | grep -F 'boolVal ( true )'
krun solution.mpy -cINPUT='lbr rbr rbr rbr rbr rbr rbr rbr lbr lbr lbr lbr lbr rbr .BString' --definition semantic-kompiled | grep -F 'boolVal ( false )'
krun solution.mpy -cINPUT='lbr rbr lbr rbr .BString' --definition semantic-kompiled | grep -F 'boolVal ( false )'
krun solution.mpy -cINPUT='lbr rbr .BString' --definition semantic-kompiled | grep -F 'boolVal ( false )'
krun solution.mpy -cINPUT='lbr lbr rbr lbr rbr rbr .BString' --definition semantic-kompiled | grep -F 'boolVal ( true )'
krun solution.mpy -cINPUT='lbr lbr rbr rbr lbr lbr .BString' --definition semantic-kompiled | grep -F 'boolVal ( true )'

# Symbolic backend and all five claims (four loop invariants plus the universal
# end-to-end theorem).  A successful run prints #Top and exits zero.
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled --spec-module SPEC
