requires "verification.k"

module GCD-SPEC
  imports GCD-VERIFICATION

  // The submitted loop body implements one Euclidean transition under the
  // unmodified reference rules.  This is the inductive step behind the
  // symbolic loop summary in verification.k.
  claim
    <k> GcdLoopBody => .K </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(("a" |-> A:Int
                   "b" |-> B:Int), P:Parent)
      => SC
         L |-> scope(("a" |-> B
                      "b" |-> pyMod(A, B)), P)
    </scopes>
    <heap> .Map </heap>
    requires A >=Int 0 andBool B >Int 0
    [label(euclid-step)]

  // For arbitrary signed integer arguments, the submitted function returns
  // the mathematical gcd of their absolute values.  gcdSpec denotes the
  // standard Euclidean recurrence and is kept opaque to avoid divergent
  // symbolic expansion.
  claim
    <k>
      #loadAll(Module(GcdDef .Stmts))
      ~> Call(Name("greatest_common_divisor"),
              (A0:Int, B0:Int, .Exprs))
      => gcdSpec(absInt(A0), absInt(B0))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope("greatest_common_divisor" |-> GcdClosure,
                   parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <stack> .List </stack>
    <ret> noRet </ret>
    [label(program-correct)]

  // Prompt examples reduce gcdSpec through its concrete Euclidean equations;
  // together with the separate MPY-KRUN run, they guard the abstraction and
  // implementation/specification linkage at exact values.
  claim
    <k>
      #loadAll(Module(GcdDef .Stmts))
      ~> Call(Name("greatest_common_divisor"), (3, 5, .Exprs))
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope("greatest_common_divisor" |-> GcdClosure,
                   parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <stack> .List </stack>
    <ret> noRet </ret>
    [label(example-3-5)]

  claim
    <k>
      #loadAll(Module(GcdDef .Stmts))
      ~> Call(Name("greatest_common_divisor"), (25, 15, .Exprs))
      => 5
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope("greatest_common_divisor" |-> GcdClosure,
                   parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <stack> .List </stack>
    <ret> noRet </ret>
    [label(example-25-15)]
endmodule
