// spec.k — change_base on the UNIFIED semantics (src/). A numeric while building the base-B digit
// string of x (base < 10 => single-digit remainders): while invariant + entry. `str(x%base)` uses
// the single-digit str interception in verification.k. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module CHANGE-BASE-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module CHANGE-BASE-SPEC

requires "verification.k"

module CHANGE-BASE-SPEC
  imports CHANGE-BASE-VERIFICATION

  // ---- While invariant (circularity) — from (x=X, ret=str(RC)) the loop leaves
  // ret := str(baseFold(X, B, RC)). `str(x%base)` reduces to the digit char via the interception
  // (x%base = pyMod(X,B), 0 <= it < B <= 10); `str(...) + ret` concatenates (applyBin "+" on str) to
  // prepend it; `x //= base` steps x to X//B. base constant.
  claim
    <k>
      #while(Compare(Name("x"), CmpOp(">", Int(0))),
        Assign(Name("ret"), BinOp("+", Call(Name("str"), BinOp("%", Name("x"), Name("base"))), Name("ret")))
        AugAssign(Name("x"), "//", Name("base")))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "change_base" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "x" <- X:Int ] [ "base" <- B:Int ] [ "ret" <- str(RC:IntSeq) ], parent(GLB:Int)) =>
        scope(.Map [ "x" <- ?_:Val ] [ "base" <- B ] [ "ret" <- str(baseFold(X, B, RC)) ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires X >=Int 0 andBool B >=Int 2 andBool B <=Int 10
    [all-path]

  // ---- Entry claim — result = change_base(X, B) == str(baseFold(X, B, .IntSeq)), the base-B digit
  // string of X (most-significant first). Domain X >= 0, base in [2,10] (single-digit remainders).
  // X == 0 -> the while never runs -> ret stays "" (baseFold(0,B,.IntSeq) = .IntSeq).
  claim
    <k>
      FuncDef("change_base", Params("x", "base"),
        Assign(Name("ret"), Str(""))
        While(Compare(Name("x"), CmpOp(">", Int(0))),
          Assign(Name("ret"), BinOp("+", Call(Name("str"), BinOp("%", Name("x"), Name("base"))), Name("ret")))
          AugAssign(Name("x"), "//", Name("base")))
        Return(Name("ret")))
      Assign(Name("result"), Call(Name("change_base"), (X:Int, B:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "change_base" <- ?_:Val ] [ "result" <- str(baseFold(X, B, .IntSeq)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires X >=Int 0 andBool B >=Int 2 andBool B <=Int 10
    [all-path]
endmodule
