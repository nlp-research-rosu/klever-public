// spec.k — max_fill on the UNIFIED semantics (src/). Outer loop over the grid rows, each adding the
// per-row integer-ceil. Fully symbolic grid (list of symbolic list rows, allList) + symbolic cap.
// See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module MAX-FILL-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module MAX-FILL-SPEC

requires "verification.k"

module MAX-FILL-SPEC
  imports MAX-FILL-VERIFICATION

  // ---- Outer-loop invariant (circularity) — over the grid rows GRIDVS from total = ACC the loop
  // leaves total := fillFrom(ACC, GRIDVS, CAP). Each row is a symbolic list (allList); sum(row) is
  // sumVS(rowProj(row)).
  claim
    <k>
      #loop(list(GRIDVS:ValSeq), Name("arr"),
        Assign(Name("total"),
          BinOp("+", Name("total"),
            BinOp("//",
              BinOp("-", BinOp("+", Call(Name("sum"), Name("arr")), Name("capacity")), Int(1)),
              Name("capacity")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "max_fill" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "grid" <- GV:Val ] [ "capacity" <- CAP:Int ] [ "total" <- ACC:Int ] [ "arr" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "grid" <- GV ] [ "capacity" <- CAP ] [ "total" <- fillFrom(ACC, GRIDVS, CAP) ] [ "arr" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allList(GRIDVS) andBool CAP >=Int 1
    [all-path]

  // ---- Entry claim — result = max_fill(list(GRIDVS), CAP) == fillFrom(0, GRIDVS, CAP).
  claim
    <k>
      FuncDef("max_fill", Params("grid", "capacity"),
        Assign(Name("total"), Int(0))
        For(Name("arr"), Name("grid"),
          Assign(Name("total"),
            BinOp("+", Name("total"),
              BinOp("//",
                BinOp("-", BinOp("+", Call(Name("sum"), Name("arr")), Name("capacity")), Int(1)),
                Name("capacity")))))
        Return(Name("total")))
      Assign(Name("result"), Call(Name("max_fill"), list(GRIDVS:ValSeq), CAP:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "max_fill" <- ?_:Val ] [ "result" <- fillFrom(0, GRIDVS, CAP) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allList(GRIDVS) andBool CAP >=Int 1
    [all-path]
endmodule
