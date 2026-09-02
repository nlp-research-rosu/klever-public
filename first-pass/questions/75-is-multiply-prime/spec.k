// spec.k — is_multiply_prime on the UNIFIED semantics (src/). Trial-division while invariant + entry.
// See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module IS-MULTIPLY-PRIME-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module IS-MULTIPLY-PRIME-SPEC

requires "verification.k"

module IS-MULTIPLY-PRIME-SPEC
  imports IS-MULTIPLY-PRIME-VERIFICATION

  // ---- Loop invariant — trial-division count. From (count=C, a=AV, i=IV) the loop leaves
  // count := C + factorCount(AV, IV); a/i havoc'd. The body's If splits on `a%i==0` (divide vs.
  // increment), matching factorCount's two non-base rules. Scope: {a, count, i}.
  claim
    <k>
      #while(Compare(Name("i"), CmpOp("<=", Name("a"))),
        If(Compare(BinOp("%", Name("a"), Name("i")), CmpOp("==", Int(0))),
          Assign(Name("count"), BinOp("+", Name("count"), Int(1)))
          Assign(Name("a"), BinOp("//", Name("a"), Name("i"))),
          Assign(Name("i"), BinOp("+", Name("i"), Int(1)))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "a" <- AV:Int ] [ "count" <- C:Int ] [ "i" <- IV:Int ], P:Parent) =>
        scope(.Map [ "a" <- ?_:Val ] [ "count" <- factorCount(AV, IV, C) ] [ "i" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires IV >=Int 2 andBool AV >=Int 0
    [all-path]

  // ---- Entry — result = is_multiply_prime(A) == mulPrimeRes(A) = (factorCount(A, 2) == 3). Domain
  // A >= 0 (the documented domain is a < 100; the trial-division count is total for any A >= 0).
  claim
    <k>
      FuncDef("is_multiply_prime", Params("a"),
        Assign(Name("count"), Int(0))
        Assign(Name("i"), Int(2))
        While(Compare(Name("i"), CmpOp("<=", Name("a"))),
          If(Compare(BinOp("%", Name("a"), Name("i")), CmpOp("==", Int(0))),
            Assign(Name("count"), BinOp("+", Name("count"), Int(1)))
            Assign(Name("a"), BinOp("//", Name("a"), Name("i"))),
            Assign(Name("i"), BinOp("+", Name("i"), Int(1)))))
        Return(Compare(Name("count"), CmpOp("==", Int(3)))))
      Assign(Name("result"), Call(Name("is_multiply_prime"), A:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_multiply_prime" <- ?_:Val ] [ "result" <- mulPrimeRes(A) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A >=Int 0
    [all-path]
endmodule
