requires "/tmp/audit-work/161-solve/verification.k"

module CONSTRUCTOR-COMPARE
  imports VERIFICATION

  claim [trusted-regeneration-equals-proof-module]:
    <k> solutionModule() => Module ( FuncDef ( "solve" , Params ( "s" , .ParamNames ) , Assign ( Name ( "result" ) , Call ( Attribute ( Name ( "s" ) , "swapcase" ) , .Exprs ) )  If ( Compare ( Name ( "result" ) , CmpOp ( "==" , Name ( "s" ) ) ) , Return ( Subscript ( Name ( "s" ) , Slice ( NoBound , NoBound , UnaryOp ( "-" , Int ( 1 ) ) ) ) )  .Stmts , .Stmts )  Return ( Name ( "result" ) )  .Stmts )  .Stmts ) </k>
endmodule
