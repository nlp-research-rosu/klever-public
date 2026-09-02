requires "verification.k"

module PINNING-SPEC
  imports VERIFICATION

  claim [body-constructor-identity]:
    <k>
      programBody()
      =>
      Assign ( Name ( "found" ) , Bool ( false ) )  Assign ( Name ( "i" ) , Int ( 0 ) )  Assign ( Name ( "j" ) , Int ( 0 ) )  Assign ( Name ( "k" ) , Int ( 0 ) )  While ( Compare ( Name ( "i" ) , CmpOp ( "<" , Call ( Name ( "len" ) , Name ( "l" ) , .Exprs ) ) ) , Assign ( Name ( "j" ) , BinOp ( "+" , Name ( "i" ) , Int ( 1 ) ) )  While ( Compare ( Name ( "j" ) , CmpOp ( "<" , Call ( Name ( "len" ) , Name ( "l" ) , .Exprs ) ) ) , Assign ( Name ( "k" ) , BinOp ( "+" , Name ( "j" ) , Int ( 1 ) ) )  While ( Compare ( Name ( "k" ) , CmpOp ( "<" , Call ( Name ( "len" ) , Name ( "l" ) , .Exprs ) ) ) , If ( Compare ( BinOp ( "+" , BinOp ( "+" , Subscript ( Name ( "l" ) , Name ( "i" ) ) , Subscript ( Name ( "l" ) , Name ( "j" ) ) ) , Subscript ( Name ( "l" ) , Name ( "k" ) ) ) , CmpOp ( "==" , Int ( 0 ) ) ) , Assign ( Name ( "found" ) , Bool ( true ) )  .Stmts , .Stmts )  AugAssign ( Name ( "k" ) , "+" , Int ( 1 ) )  .Stmts )  Assign ( Name ( "k" ) , Int ( 0 ) )  AugAssign ( Name ( "j" ) , "+" , Int ( 1 ) )  .Stmts )  Assign ( Name ( "j" ) , Int ( 0 ) )  AugAssign ( Name ( "i" ) , "+" , Int ( 1 ) )  .Stmts )  Return ( Name ( "found" ) )  .Stmts
    </k>

  claim [closure-constructor-identity]:
    <k>
      triplesClosure()
      =>
      closureVal(("l", .ParamNames), Assign ( Name ( "found" ) , Bool ( false ) )  Assign ( Name ( "i" ) , Int ( 0 ) )  Assign ( Name ( "j" ) , Int ( 0 ) )  Assign ( Name ( "k" ) , Int ( 0 ) )  While ( Compare ( Name ( "i" ) , CmpOp ( "<" , Call ( Name ( "len" ) , Name ( "l" ) , .Exprs ) ) ) , Assign ( Name ( "j" ) , BinOp ( "+" , Name ( "i" ) , Int ( 1 ) ) )  While ( Compare ( Name ( "j" ) , CmpOp ( "<" , Call ( Name ( "len" ) , Name ( "l" ) , .Exprs ) ) ) , Assign ( Name ( "k" ) , BinOp ( "+" , Name ( "j" ) , Int ( 1 ) ) )  While ( Compare ( Name ( "k" ) , CmpOp ( "<" , Call ( Name ( "len" ) , Name ( "l" ) , .Exprs ) ) ) , If ( Compare ( BinOp ( "+" , BinOp ( "+" , Subscript ( Name ( "l" ) , Name ( "i" ) ) , Subscript ( Name ( "l" ) , Name ( "j" ) ) ) , Subscript ( Name ( "l" ) , Name ( "k" ) ) ) , CmpOp ( "==" , Int ( 0 ) ) ) , Assign ( Name ( "found" ) , Bool ( true ) )  .Stmts , .Stmts )  AugAssign ( Name ( "k" ) , "+" , Int ( 1 ) )  .Stmts )  Assign ( Name ( "k" ) , Int ( 0 ) )  AugAssign ( Name ( "j" ) , "+" , Int ( 1 ) )  .Stmts )  Assign ( Name ( "j" ) , Int ( 0 ) )  AugAssign ( Name ( "i" ) , "+" , Int ( 1 ) )  .Stmts )  Return ( Name ( "found" ) )  .Stmts, 0)
    </k>

  claim [binding-constructor-identity]:
    <k> .K </k>
    <scopes>
      0 |-> scope(
        (solutionBindings()
          =>
          "triples_sum_to_zero"
            |-> closureVal(("l", .ParamNames), Assign ( Name ( "found" ) , Bool ( false ) )  Assign ( Name ( "i" ) , Int ( 0 ) )  Assign ( Name ( "j" ) , Int ( 0 ) )  Assign ( Name ( "k" ) , Int ( 0 ) )  While ( Compare ( Name ( "i" ) , CmpOp ( "<" , Call ( Name ( "len" ) , Name ( "l" ) , .Exprs ) ) ) , Assign ( Name ( "j" ) , BinOp ( "+" , Name ( "i" ) , Int ( 1 ) ) )  While ( Compare ( Name ( "j" ) , CmpOp ( "<" , Call ( Name ( "len" ) , Name ( "l" ) , .Exprs ) ) ) , Assign ( Name ( "k" ) , BinOp ( "+" , Name ( "j" ) , Int ( 1 ) ) )  While ( Compare ( Name ( "k" ) , CmpOp ( "<" , Call ( Name ( "len" ) , Name ( "l" ) , .Exprs ) ) ) , If ( Compare ( BinOp ( "+" , BinOp ( "+" , Subscript ( Name ( "l" ) , Name ( "i" ) ) , Subscript ( Name ( "l" ) , Name ( "j" ) ) ) , Subscript ( Name ( "l" ) , Name ( "k" ) ) ) , CmpOp ( "==" , Int ( 0 ) ) ) , Assign ( Name ( "found" ) , Bool ( true ) )  .Stmts , .Stmts )  AugAssign ( Name ( "k" ) , "+" , Int ( 1 ) )  .Stmts )  Assign ( Name ( "k" ) , Int ( 0 ) )  AugAssign ( Name ( "j" ) , "+" , Int ( 1 ) )  .Stmts )  Assign ( Name ( "j" ) , Int ( 0 ) )  AugAssign ( Name ( "i" ) , "+" , Int ( 1 ) )  .Stmts )  Return ( Name ( "found" ) )  .Stmts, 0)),
        parent(-1))
      ...
    </scopes>
endmodule
