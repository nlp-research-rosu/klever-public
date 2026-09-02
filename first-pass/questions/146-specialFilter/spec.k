// spec.k — specialFilter, TRAP-FREE (P146). Element-loop invariant over the
// abstract seq (three frame variants: num<=10 prefixes never bind the branch
// locals) with TAIL posts; entry over the real single FuncDef.
//
//   kompile verification.k --backend haskell --main-module SPECIALFILTER-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module SPECIALFILTER-SPEC

requires "verification.k"

module SPECIALFILTER-SPEC
  imports SPECIALFILTER-VERIFICATION

  claim
    <k>
      #loop(list(VS:ValSeq), Name("num"),
        If(Compare(Name("num"), CmpOp(">", Int(10))),
          Assign(Name("odd_digits"), TupleExpr(Int(1), Int(3), Int(5), Int(7), Int(9)))
          Assign(Name("number_as_string"), Call(Name("str"), Name("num")))
          If(BoolOp("and",
              Compare(Call(Name("int"), Subscript(Name("number_as_string"), Int(0))),
                CmpOp("in", Name("odd_digits"))),
              Compare(Call(Name("int"), Subscript(Name("number_as_string"), UnaryOp("-", Int(1)))),
                CmpOp("in", Name("odd_digits")))),
            AugAssign(Name("count"), "+", Int(1)),
            .Stmts),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "specialFilter" <- SFV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "nums" <- NSV:Val ] [ "count" <- C:Int ], parent(0))
           => scope((.Map [ "nums" <- NSV ] [ "count" <- sfCount(VS, C) ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]

  claim
    <k>
      #loop(list(VS:ValSeq), Name("num"),
        If(Compare(Name("num"), CmpOp(">", Int(10))),
          Assign(Name("odd_digits"), TupleExpr(Int(1), Int(3), Int(5), Int(7), Int(9)))
          Assign(Name("number_as_string"), Call(Name("str"), Name("num")))
          If(BoolOp("and",
              Compare(Call(Name("int"), Subscript(Name("number_as_string"), Int(0))),
                CmpOp("in", Name("odd_digits"))),
              Compare(Call(Name("int"), Subscript(Name("number_as_string"), UnaryOp("-", Int(1)))),
                CmpOp("in", Name("odd_digits")))),
            AugAssign(Name("count"), "+", Int(1)),
            .Stmts),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "specialFilter" <- SFV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "nums" <- NSV:Val ] [ "count" <- C:Int ] [ "num" <- _:Val ], parent(0))
           => scope((.Map [ "nums" <- NSV ] [ "count" <- sfCount(VS, C) ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]

  claim
    <k>
      #loop(list(VS:ValSeq), Name("num"),
        If(Compare(Name("num"), CmpOp(">", Int(10))),
          Assign(Name("odd_digits"), TupleExpr(Int(1), Int(3), Int(5), Int(7), Int(9)))
          Assign(Name("number_as_string"), Call(Name("str"), Name("num")))
          If(BoolOp("and",
              Compare(Call(Name("int"), Subscript(Name("number_as_string"), Int(0))),
                CmpOp("in", Name("odd_digits"))),
              Compare(Call(Name("int"), Subscript(Name("number_as_string"), UnaryOp("-", Int(1)))),
                CmpOp("in", Name("odd_digits")))),
            AugAssign(Name("count"), "+", Int(1)),
            .Stmts),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "specialFilter" <- SFV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "nums" <- NSV:Val ] [ "count" <- C:Int ] [ "num" <- _:Val ] [ "odd_digits" <- _:Val ] [ "number_as_string" <- _:Val ], parent(0))
           => scope((.Map [ "nums" <- NSV ] [ "count" <- sfCount(VS, C) ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]

  claim
    <k>
      FuncDef("specialFilter", Params("nums"),
        Assign(Name("count"), Int(0))
        For(Name("num"), Name("nums"),
          If(Compare(Name("num"), CmpOp(">", Int(10))),
          Assign(Name("odd_digits"), TupleExpr(Int(1), Int(3), Int(5), Int(7), Int(9)))
          Assign(Name("number_as_string"), Call(Name("str"), Name("num")))
          If(BoolOp("and",
              Compare(Call(Name("int"), Subscript(Name("number_as_string"), Int(0))),
                CmpOp("in", Name("odd_digits"))),
              Compare(Call(Name("int"), Subscript(Name("number_as_string"), UnaryOp("-", Int(1)))),
                CmpOp("in", Name("odd_digits")))),
            AugAssign(Name("count"), "+", Int(1)),
            .Stmts),
          .Stmts))
        Return(Name("count")))
      Assign(Name("result"), Call(Name("specialFilter"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "specialFilter" <- ?_:Val ] [ "result" <- sfCount(VS, 0) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
