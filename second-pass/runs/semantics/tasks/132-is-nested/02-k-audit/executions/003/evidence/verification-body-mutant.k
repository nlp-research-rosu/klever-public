requires "reference-semantics/semantics.k"

module IS-NESTED-VERIFICATION
  imports MPY

  // The translated implementation, factored only to keep the claims readable.
  syntax Stmts ::= "scanBody" [function]
  rule scanBody
    => If(Compare(Call(Name("ord"), Name("char")),
                 CmpOp("==", Int(93))),
         If(Compare(Name("state"), CmpOp("<", Int(2))),
            AugAssign(Name("state"), "+", Int(1))
            .Stmts,
            .Stmts)
         .Stmts,
         If(Compare(Name("state"), CmpOp(">", Int(1))),
            If(Compare(Name("state"), CmpOp("<", Int(4))),
               AugAssign(Name("state"), "+", Int(1))
               .Stmts,
               .Stmts)
            .Stmts,
            .Stmts)
         .Stmts)
       .Stmts

  syntax Stmts ::= "isNestedBody" [function]
  rule isNestedBody
    => Assign(Name("state"), Int(0))
       Assign(Name("char"), Str(""))
       For(Name("char"), Name("string"), scanBody)
       Return(Compare(Name("state"), CmpOp("==", Int(4))))
       .Stmts

  syntax Val ::= "isNestedClosure" [function]
  rule isNestedClosure
    => closureVal(("string", .ParamNames), isNestedBody, 0)

  // All and only inputs admitted by the prompt: finite strings of '[' and ']'.
  syntax BSeq ::= "bNil" | bOpen(BSeq) | bClose(BSeq)

  // bCodes is a symbolic IntSeq encoding.  Its iterator observations are
  // exactly those of the corresponding native 91/93 code sequence.
  syntax IntSeq ::= bCodes(BSeq)
  rule <k> #iterNext(str(bCodes(bNil))) => #iterDone ... </k>
  rule <k> #iterNext(str(bCodes(bOpen(BS))))
        => #iterYield(str(iCons(91, .IntSeq)), str(bCodes(BS))) ... </k>
  rule <k> #iterNext(str(bCodes(bClose(BS))))
        => #iterYield(str(iCons(93, .IntSeq)), str(bCodes(BS))) ... </k>

  // Independent reference automaton for the subsequence [ [ ] ].
  syntax Int ::= openStep(Int) [function, total]
  rule openStep(I)
    => #if I <Int 2 #then I +Int 1 #else I #fi

  syntax Int ::= closeStep(Int) [function, total]
  rule closeStep(I)
    => #if I >Int 1 andBool I <Int 4 #then I +Int 1 #else I #fi

  syntax Int ::= scanState(Int, BSeq) [function, total]
  rule scanState(I, bNil)       => I
  rule scanState(I, bOpen(BS))  => scanState(openStep(I), BS)
  rule scanState(I, bClose(BS)) => scanState(closeStep(I), BS)

  syntax Bool ::= nested(BSeq) [function, total]
  rule nested(BS) => scanState(0, BS) ==Int 4
endmodule

// This module is compiled only after IS-NESTED-LOOP-SPEC has proved the rule
// below against the base module.  It makes that established loop theorem
// available as a modular lemma for the entry-point proof.
module IS-NESTED-VERIFICATION-WITH-LOOP-LEMMA
  imports IS-NESTED-VERIFICATION

  rule [proved-scan-loop]:
    <k>
      #loop(str(bCodes(BS:BSeq)), Name("char"),
        If(Compare(Call(Name("ord"), Name("char")),
                   CmpOp("==", Int(91))),
           If(Compare(Name("state"), CmpOp("<", Int(2))),
              AugAssign(Name("state"), "+", Int(1))
              .Stmts,
              .Stmts)
           .Stmts,
           If(Compare(Name("state"), CmpOp(">", Int(1))),
              If(Compare(Name("state"), CmpOp("<", Int(4))),
                 AugAssign(Name("state"), "+", Int(1))
                 .Stmts,
                 .Stmts)
              .Stmts,
              .Stmts)
           .Stmts)
         .Stmts)
      ~> (Return(Compare(Name("state"), CmpOp("==", Int(4))))
          .Stmts):Stmts
      ~> #endcall
      => scanState(I:Int, BS) ==Int 4
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (1 |-> scope(
        "state" |-> I
        "char" |-> _CHAR:Val
        "string" |-> _INPUT:Val,
        parent(0)) => .Map)
      _REST:Map
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int I andBool I <=Int 4
    [priority(40)]
endmodule
