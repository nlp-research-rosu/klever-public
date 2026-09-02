#!/usr/bin/env python3
"""Generate small K specs whose program term comes from an actual .mpy file."""

import argparse
import re
from pathlib import Path


def identity_spec(program: str) -> str:
    return f'''requires "verification.k"

module IDENTITY-SPEC
  imports VERIFICATION

  claim [translated-program-identity]:
    <k> #loadAll({program}) => .K </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map => "even_odd_count" |-> evenOddClosure, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
'''


def mutant_spec(program: str) -> str:
    return f'''requires "verification-with-lemma.k"

module BODY-MUTATION-SPEC
  imports VERIFICATION-WITH-LEMMA

  claim [mutated-body-rejected]:
    <k> #loadAll({program})
         ~> Call(Name("even_odd_count"), Int(2))
         => tuple(vCons(1, vCons(0, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map => ?M:Map, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("identity", "mutant"))
    parser.add_argument("program")
    args = parser.parse_args()
    program = Path(args.program).read_text(encoding="utf-8").strip()
    # The standalone .mpy parser accepts a blank list argument. When embedded
    # in a K rule, spell the empty statement-list unit explicitly.
    program = re.sub(r",\s*\)", ", .Stmts)", program)
    print(identity_spec(program) if args.mode == "identity" else mutant_spec(program))


if __name__ == "__main__":
    main()
