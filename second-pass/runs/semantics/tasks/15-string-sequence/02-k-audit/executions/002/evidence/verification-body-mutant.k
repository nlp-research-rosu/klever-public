requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  syntax IntSeq ::= sequenceCodes(Int) [function, injective]
  rule sequenceCodes(0) => iCons(48, .IntSeq)
  rule sequenceCodes(N:Int)
    => seqConcat(sequenceCodes(N -Int 1),
         iCons(32, strToCodes(Int2String(N))))
    [owise]
  rule sequenceCodes(N:Int)
    => seqConcat(sequenceCodes(N -Int 1),
         iCons(32, strToCodes(Int2String(N))))
    requires N >=Int 1
    [simplification]

  rule inRange(I:Int, I +Int D:Int, 1) => D >Int 0 [simplification]
  rule I:Int <Int I +Int D:Int => D >Int 0 [simplification]
  rule seqConcat(sequenceCodes(X:Int -Int 1),
                 iCons(32, strToCodes(Int2String(X))))
    => sequenceCodes(X)
    requires X >=Int 1
    [simplification]

  syntax Stmts ::= "sequenceLoopBody" [macro]
  rule sequenceLoopBody
    => Assign(Name("result"),
         BinOp("+", Name("result"),
           BinOp("+", Str(" "), Call(Name("str"), Name("i")))))

  // Material body mutation: this changes the constructor term bound into the
  // closure and executed by the claim from initial "0" to initial "WRONG".
  syntax Stmts ::= "sequenceBody" [macro]
  rule sequenceBody
    => Expr(Str("Return the decimal integers from 0 through n, separated by spaces."))
       If(Compare(Name("n"), CmpOp("<", Int(0))), Return(Str("")), .Stmts)
       Assign(Name("result"), Str("WRONG"))
       Assign(Name("i"), Int(1))
       For(Name("i"), Call(Name("range"), Int(1), BinOp("+", Name("n"), Int(1))),
           sequenceLoopBody)
       Return(Name("result"))
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // Unchanged candidate bridge: because its LHS uses the same macro, it now
  // also matches the mutated body while its result remains the original answer.
  rule <k> sequenceBody ~> #endcall
        => Return(str(sequenceCodes(N))) ~> #endcall </k>
       <env> 1 </env>
       <scopes>
         ... 1 |-> scope("n" |-> N:Int, parent(0)) ...
       </scopes>
    requires N >=Int 0
    [priority(40)]
endmodule
