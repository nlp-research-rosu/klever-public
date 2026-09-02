requires "verification-base.k"

module VERIFICATION
  imports VERIFICATION-BASE

  // Operational bridge justified over this exact match domain by
  // LOOP-CONNECTION.binary-loop-exact in connection-spec.k.
  rule <k>
         #while(
           Compare(Name("value"), CmpOp(">", Int(1))),
           Assign(
             Name("digits"),
             BinOp(
               "+",
               Call(
                 Name("chr"),
                 BinOp("+", Int(48), BinOp("%", Name("value"), Int(2)))),
               Name("digits")))
           Assign(Name("value"), BinOp("//", Name("value"), Int(2))))
         => .K
         ...
       </k>
       <env> 1 </env>
       <scopes>
         -1 |-> BUILTINS:Scope
         0 |-> scope(MODULE:Map, parent(-1))
         1 |-> scope(
           "n" |-> NI:Int
           "m" |-> MI:Int
           "value" |-> (V:Int => 1)
           "digits" |-> (str(A:IntSeq) => str(loopDigits(V, A))),
           parent(0))
       </scopes>
    requires V >Int 0
      andBool allBits(A)
      andBool BUILTINS ==K builtinsScope
      andBool notBool ("chr" in_keys(MODULE))
    [priority(40)]

  // Derived summary properties established by the same bridge-free theorem.
  rule bitWeight(loopDigits(V, A)) +Int bitValue(loopDigits(V, A))
    => V *Int bitWeight(A) +Int bitValue(A)
    requires V >Int 0 andBool allBits(A)
    [simplification]
  rule 1 *Int bitWeight(loopDigits(V, A)) +Int bitValue(loopDigits(V, A))
    => V *Int bitWeight(A) +Int bitValue(A)
    requires V >Int 0 andBool allBits(A)
    [simplification]

  rule allBits(loopDigits(V, A)) => true
    requires V >Int 0 andBool allBits(A)
    [simplification]
endmodule
