requires "verification.k"

module VERIFIED-LEMMA
  imports VERIFICATION

  // This is the N=0 instance of the inductive claim proved in LOOP-SPEC.
  rule <k>
         loop(
           Compare(Name("i"),
             CmpOp("<=", Call(Name("len"), Name("string")))),
           Expr(Call(Attribute(Name("result"), "append"),
             Subscript(Name("string"),
               Slice(NoBound, Name("i"), NoBound))))
           Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
         ~> exec(Return(Name("result")))
         ~> restoreEnv(OLD)
         => listVal(allPrefixes(S))
       </k>
       <env>
         bind("string", strVal(S),
           bind("result", listVal(vnil),
             bind("i", intVal(1), emptyEnv)))
         => OLD
       </env>
    requires 0 <=Int lengthString(S)
    [priority(30)]
endmodule
