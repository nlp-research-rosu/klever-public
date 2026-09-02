requires "verification.k"

module UNIQUE-DIGITS-SPEC
  imports UNIQUE-DIGITS-VERIFICATION

  // ---- Inner digit-while invariant (co-inductive circularity): folds
  // is_odd to oddAcc(N, B); the heap is untouched.
  claim
    <k>
      #while(Compare(Name("n"), CmpOp(">", Int(0))),
        If(Compare(
          BinOp("%", BinOp("%", Name("n"), Int(10)), Int(2)),
          CmpOp("==", Int(0))),
          Assign(Name("is_odd"), Bool(false)),
          .Stmts)
        Assign(Name("n"), BinOp("//", Name("n"), Int(10))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "unique_digits" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "x" <- XV:Val ] [ "odd_digit_elements" <- ref(AR:Int) ]
                    [ "i" <- IV:Val ] [ "n" <- NV:Val ] [ "is_odd" <- B:Bool ], parent(0)) =>
         scope(.Map [ "x" <- XV ] [ "odd_digit_elements" <- ref(AR) ]
                    [ "i" <- IV ] [ "n" <- ?_:Val ]
                    [ "is_odd" <- (oddI(projectIntTotal(NV), B) ==Int 1) ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isInt(NV)
    [all-path]

  // ---- Outer element-loop invariant, variant B: i/n/is_odd bound. Fixed-ref
  // append (heap rest untouched -- nothing in the body allocates).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        Assign(Name("n"), Name("i"))
        Assign(Name("is_odd"), Bool(true))
        While(Compare(Name("n"), CmpOp(">", Int(0))),
          If(Compare(
            BinOp("%", BinOp("%", Name("n"), Int(10)), Int(2)),
            CmpOp("==", Int(0))),
            Assign(Name("is_odd"), Bool(false)),
            .Stmts)
          Assign(Name("n"), BinOp("//", Name("n"), Int(10))))
        If(Name("is_odd"),
          Expr(
            Call(
              Attribute(Name("odd_digit_elements"), "append"),
              Name("i"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "unique_digits" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "x" <- XV:Val ] [ "odd_digit_elements" <- ref(AR:Int) ]
                    [ "i" <- _:Val ] [ "n" <- _:Val ] [ "is_odd" <- _:Val ], parent(0)) =>
         scope(.Map [ "x" <- XV ] [ "odd_digit_elements" <- ref(AR) ]
                    [ "i" <- ?_:Val ] [ "n" <- ?_:Val ] [ "is_odd" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (AR |-> list(ACC:ValSeq)) HREST:Map
        => (AR |-> list(filterOdd2(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]

  // ---- Variant A: pre-first-iteration (i/n/is_odd unbound).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        Assign(Name("n"), Name("i"))
        Assign(Name("is_odd"), Bool(true))
        While(Compare(Name("n"), CmpOp(">", Int(0))),
          If(Compare(
            BinOp("%", BinOp("%", Name("n"), Int(10)), Int(2)),
            CmpOp("==", Int(0))),
            Assign(Name("is_odd"), Bool(false)),
            .Stmts)
          Assign(Name("n"), BinOp("//", Name("n"), Int(10))))
        If(Name("is_odd"),
          Expr(
            Call(
              Attribute(Name("odd_digit_elements"), "append"),
              Name("i"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "unique_digits" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "x" <- XV:Val ] [ "odd_digit_elements" <- ref(AR:Int) ], parent(0)) =>
         scope(.Map [ "x" <- XV ] [ "odd_digit_elements" <- ref(AR) ]
                    [ "i" <- ?_:Val ] [ "n" <- ?_:Val ] [ "is_odd" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (AR |-> list(ACC:ValSeq)) HREST:Map
        => (AR |-> list(filterOdd2(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool 0 <Int vsLen(VS)
    [all-path]

  // ---- Entry claim -- the REAL canonical-shape code, verbatim .mpy.
  claim
    <k>
      FuncDef("unique_digits", Params("x"),
        Assign(Name("odd_digit_elements"), ListExpr(.Exprs))
        For(Name("i"), Name("x"),
          Assign(Name("n"), Name("i"))
          Assign(Name("is_odd"), Bool(true))
          While(Compare(Name("n"), CmpOp(">", Int(0))),
            If(Compare(
              BinOp("%", BinOp("%", Name("n"), Int(10)), Int(2)),
              CmpOp("==", Int(0))),
              Assign(Name("is_odd"), Bool(false)),
              .Stmts)
            Assign(Name("n"), BinOp("//", Name("n"), Int(10))))
          If(Name("is_odd"),
            Expr(
              Call(
                Attribute(Name("odd_digit_elements"), "append"),
                Name("i"))),
            .Stmts))
        Return(Call(Name("sorted"), Name("odd_digit_elements"))))
      Assign(Name("result"), Call(Name("unique_digits"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "unique_digits" <- ?_:Val ]
                       [ "result" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(sortVS(filterOdd2(VS, .ValSeq)))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
