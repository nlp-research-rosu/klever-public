requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical result for the unprocessed suffix when the current nesting
  // depth is D.  The implementation's else branch treats every non-"<"
  // character as a close bracket; on the prompt's domain those are exactly
  // the ">" characters.
  syntax Bool ::= bracketResult(IntSeq, Int) [function, total]

  rule bracketResult(.IntSeq, 0) => true [simplification]
  rule bracketResult(.IntSeq, D:Int) => false
       requires D >Int 0
       [simplification]
  rule bracketResult(.IntSeq, D:Int) => false
       requires D <Int 0
       [simplification]

  rule bracketResult(iCons(60, REST:IntSeq), 0)
    => bracketResult(REST, 1)
       [simplification]
  rule bracketResult(iCons(C:Int, _REST:IntSeq), 0) => false
       requires notBool (C ==Int 60)
       [simplification]

  rule bracketResult(iCons(60, REST:IntSeq), D:Int)
    => bracketResult(REST, D +Int 1)
       requires D >Int 0
  rule bracketResult(iCons(C:Int, REST:IntSeq), D:Int)
    => bracketResult(REST, D -Int 1)
       requires notBool (C ==Int 60) andBool D >Int 0
  rule bracketResult(iCons(_C:Int, _REST:IntSeq), D:Int) => false
       requires D <Int 0
       [simplification]

  // Proof-only derived macro steps for this program's two return forms.
  // The Haskell prover otherwise leaves evaluated Bool values in the strict
  // Return freezer.  Each rule is the composition of the reference literal /
  // lookup / comparison rules with MPY-FUNCTIONS' Return rule.
  rule <k> Return(Bool(B:Bool)) ~> _ => #pop </k>
       <ret> noRet => retV(B) </ret>
       [priority(40)]

  rule <k>
         Return(Compare(Name("depth"), CmpOp("==", Int(0)))) ~> _
       =>
         #pop
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           "brackets" |-> _BRACKETS:Val
           "depth" |-> D:Int
           "bracket" |-> _BRACKET:Val,
           _PARENT:Parent) ...
       </scopes>
       <ret> noRet => retV(D ==Int 0) </ret>
       [priority(40)]

  rule <k>
         If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
            THEN:Stmts, ELSE:Stmts)
       =>
         #branch(true, THEN, ELSE)
       ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           "brackets" |-> _BRACKETS:Val
           "depth" |-> _D:Int
           "bracket" |-> str(iCons(C:Int, .IntSeq)),
           _PARENT:Parent) ...
       </scopes>
       requires C ==Int 60
       [priority(40)]

  rule <k>
         If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
            THEN:Stmts, ELSE:Stmts)
       =>
         #branch(false, THEN, ELSE)
       ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           "brackets" |-> _BRACKETS:Val
           "depth" |-> _D:Int
           "bracket" |-> str(iCons(C:Int, .IntSeq)),
           _PARENT:Parent) ...
       </scopes>
       requires C =/=Int 60
       [priority(40)]

  rule <k>
         AugAssign(Name("depth"), "+", Int(1)) => .K
       ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           "brackets" |-> _BRACKETS:Val
           "depth" |-> (D:Int => D +Int 1)
           "bracket" |-> _BRACKET:Val,
           _PARENT:Parent) ...
       </scopes>
       [priority(40)]

  rule <k>
         AugAssign(Name("depth"), "-", Int(1)) => .K
       ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           "brackets" |-> _BRACKETS:Val
           "depth" |-> (D:Int => D -Int 1)
           "bracket" |-> _BRACKET:Val,
           _PARENT:Parent) ...
       </scopes>
       [priority(40)]

  rule <k>
         If(Compare(Name("depth"), CmpOp("<", Int(0))),
            THEN:Stmts, ELSE:Stmts)
       =>
         #branch(true, THEN, ELSE)
       ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           "brackets" |-> _BRACKETS:Val
           "depth" |-> D:Int
           "bracket" |-> _BRACKET:Val,
           _PARENT:Parent) ...
       </scopes>
       requires D <Int 0
       [priority(40)]

  rule <k>
         If(Compare(Name("depth"), CmpOp("<", Int(0))),
            THEN:Stmts, ELSE:Stmts)
       =>
         #branch(false, THEN, ELSE)
       ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           "brackets" |-> _BRACKETS:Val
           "depth" |-> D:Int
           "bracket" |-> _BRACKET:Val,
           _PARENT:Parent) ...
       </scopes>
       requires D >=Int 0
       [priority(40)]

  // Normal form of MPY-FUNCTIONS' #pop rule when the callee location is known
  // fresh in the rest of the scope map.  This removes the symbolic
  // `MAP [ L <- undef ]` update that the backend intentionally does not
  // normalize on its own.
  rule <k> #pop => V ~> CONT </k>
       <ret> retV(V:Val) => noRet </ret>
       <stack>
         ListItem(frame(CONT:K, CALLER:Int, SAVED:Int)) REST:List => REST
       </stack>
       <env> L:Int => CALLER </env>
       <scopes> (L |-> _FRAME:Scope SC:Map) => SC </scopes>
       <scopeLoc> _ => SAVED </scopeLoc>
       requires notBool L in_keys(SC)
       [priority(40)]
endmodule
