requires "verification.k"

module CONSTRUCTOR-PINNING-SPEC
  imports VERIFICATION-BASE

  claim
    <k> intersectionBody ~> K:K
      =>
Assign ( Name ( "left" ) , Call ( Name ( "max" ) , Subscript ( Name ( "interval1" ) , Int ( 0 ) ) , Subscript ( Name ( "interval2" ) , Int ( 0 ) ) , .Exprs ) )  Assign ( Name ( "right" ) , Call ( Name ( "min" ) , Subscript ( Name ( "interval1" ) , Int ( 1 ) ) , Subscript ( Name ( "interval2" ) , Int ( 1 ) ) , .Exprs ) )  Assign ( Name ( "length" ) , BinOp ( "-" , Name ( "right" ) , Name ( "left" ) ) )  If ( Compare ( Name ( "length" ) , CmpOp ( "<=" , Int ( 1 ) ) ) , Return ( Str ( "NO" ) )  .Stmts , .Stmts )  Assign ( Name ( "divisor" ) , Int ( 2 ) )  For ( Name ( "divisor" ) , Call ( Name ( "range" ) , Int ( 2 ) , Name ( "length" ) , .Exprs ) , If ( Compare ( BinOp ( "%" , Name ( "length" ) , Name ( "divisor" ) ) , CmpOp ( "==" , Int ( 0 ) ) ) , Return ( Str ( "NO" ) )  .Stmts , .Stmts )  .Stmts )  Return ( Str ( "YES" ) )  .Stmts
      ~> K
    </k>
    [label(constructor-pinning)]
endmodule
