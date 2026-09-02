// spec.k — even_odd_palindrome, TRAP-FREE (P107). The outer invariant runs a
// REAL nested-closure call per iteration (both if/elif arms); the straight-line
// callee reduces via the digitCodes/sliceIS bridges to the palindrome atom and
// #pop restores the fixed shape. Closed-frame pair + entry.
//
//   kompile verification.k --backend haskell --main-module EVEN-ODD-PALINDROME-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module EVEN-ODD-PALINDROME-SPEC

requires "verification.k"

module EVEN-ODD-PALINDROME-SPEC
  imports EVEN-ODD-PALINDROME-VERIFICATION

  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        If(BoolOp("and",
            Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(1))),
            Call(Name("is_palindrome"), Name("i"))),
          AugAssign(Name("odd_palindrome_count"), "+", Int(1)),
          If(BoolOp("and",
              Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
              Call(Name("is_palindrome"), Name("i"))),
            AugAssign(Name("even_palindrome_count"), "+", Int(1)),
            .Stmts)))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "even_odd_palindrome" <- EOPV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "n" <- N:Int ]
                [ "is_palindrome" <- closureValC("n", .ParamNames,
              Return(Compare(Call(Name("str"), Name("n")),
                CmpOp("==",
                  Subscript(Call(Name("str"), Name("n")),
                    Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))) .Stmts, .Map) ]
                [ "even_palindrome_count" <- EC:Int ] [ "odd_palindrome_count" <- OC:Int ], parent(0))
           => scope((.Map [ "n" <- N ] [ "is_palindrome" <- ?_:Val ]
                [ "even_palindrome_count" <- evenPal(I, HI, EC) ]
                [ "odd_palindrome_count" <- oddPal(I, HI, OC) ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 1
    [all-path]

  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        If(BoolOp("and",
            Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(1))),
            Call(Name("is_palindrome"), Name("i"))),
          AugAssign(Name("odd_palindrome_count"), "+", Int(1)),
          If(BoolOp("and",
              Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
              Call(Name("is_palindrome"), Name("i"))),
            AugAssign(Name("even_palindrome_count"), "+", Int(1)),
            .Stmts)))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "even_odd_palindrome" <- EOPV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "n" <- N:Int ]
                [ "is_palindrome" <- closureValC("n", .ParamNames,
              Return(Compare(Call(Name("str"), Name("n")),
                CmpOp("==",
                  Subscript(Call(Name("str"), Name("n")),
                    Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))) .Stmts, .Map) ]
                [ "even_palindrome_count" <- EC:Int ] [ "odd_palindrome_count" <- OC:Int ] [ "i" <- _:Val ], parent(0))
           => scope((.Map [ "n" <- N ] [ "is_palindrome" <- ?_:Val ]
                [ "even_palindrome_count" <- evenPal(I, HI, EC) ]
                [ "odd_palindrome_count" <- oddPal(I, HI, OC) ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 1
    [all-path]

  // ---- entry
  claim
    <k>
      FuncDef("even_odd_palindrome", Params("n"),
        FuncDef("is_palindrome", Params("n"), CellVars(.ParamNames), FreeVars(.ParamNames),
          Return(Compare(Call(Name("str"), Name("n")),
            CmpOp("==",
              Subscript(Call(Name("str"), Name("n")),
                Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))))
        Assign(Name("even_palindrome_count"), Int(0))
        Assign(Name("odd_palindrome_count"), Int(0))
        For(Name("i"), Call(Name("range"), Int(1), BinOp("+", Name("n"), Int(1))),
          If(BoolOp("and",
            Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(1))),
            Call(Name("is_palindrome"), Name("i"))),
          AugAssign(Name("odd_palindrome_count"), "+", Int(1)),
          If(BoolOp("and",
              Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
              Call(Name("is_palindrome"), Name("i"))),
            AugAssign(Name("even_palindrome_count"), "+", Int(1)),
            .Stmts)))
        Return(TupleExpr(Name("even_palindrome_count"), Name("odd_palindrome_count"))))
      Assign(Name("result"), Call(Name("even_odd_palindrome"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "even_odd_palindrome" <- ?_:Val ]
                       [ "result" <- tuple(vCons(evenPal(1, N +Int 1, 0), vCons(oddPal(1, N +Int 1, 0), .ValSeq))) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1
    [all-path]
endmodule
