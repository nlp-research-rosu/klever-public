requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // Mathematical result: ASCII codes for "0 1 ... N".  Defining the
  // contract independently of the program keeps the final claim readable.
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

  // Normalize the range guard to the decreasing distance used by the
  // invariant; this is the integer identity I < I + D iff D > 0.
  rule inRange(I:Int, I +Int D:Int, 1) => D >Int 0 [simplification]
  rule I:Int <Int I +Int D:Int => D >Int 0 [simplification]
  rule seqConcat(sequenceCodes(X:Int -Int 1),
                 iCons(32, strToCodes(Int2String(X))))
    => sequenceCodes(X)
    requires X >=Int 1
    [simplification]

  // These macros are exactly the translated function body and loop body in
  // solution.mpy.  They let the invariant and its proved summary share one
  // syntactic definition.
  syntax Stmts ::= "sequenceLoopBody" [macro]
  rule sequenceLoopBody
    => Assign(Name("result"),
         BinOp("+", Name("result"),
           BinOp("+", Str(" "), Call(Name("str"), Name("i")))))

  syntax Stmts ::= "sequenceBody" [macro]
  rule sequenceBody
    => Expr(Str("Return the decimal integers from 0 through n, separated by spaces."))
       If(Compare(Name("n"), CmpOp("<", Int(0))), Return(Str("")), .Stmts)
       Assign(Name("result"), Str("0"))
       Assign(Name("i"), Int(1))
       For(Name("i"), Call(Name("range"), Int(1), BinOp("+", Name("n"), Int(1))),
           sequenceLoopBody)
       Return(Name("result"))
endmodule

// This module adds the loop summary only after LOOP-SPEC has proved the same
// reachability formula against VERIFICATION-BASE.  FULL-SPEC then composes the
// proved invariant with ordinary function-call semantics.
module VERIFICATION
  imports VERIFICATION-BASE

  // Corollary of LOOP-SPEC at I = 1, composed with the body’s deterministic
  // initialization.  Keeping #endcall lets the reference return/pop rules
  // perform ordinary frame restoration.
  rule <k> sequenceBody ~> #endcall
        => Return(str(sequenceCodes(N))) ~> #endcall </k>
       <env> 1 </env>
       <scopes>
         ... 1 |-> scope("n" |-> N:Int, parent(0)) ...
       </scopes>
    requires N >=Int 0
    [priority(40)]
endmodule
