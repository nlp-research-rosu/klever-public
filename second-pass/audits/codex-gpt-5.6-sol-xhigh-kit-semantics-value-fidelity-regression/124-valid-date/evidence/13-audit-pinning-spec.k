requires "verification.k"

module AUDIT-PINNING-SPEC
  imports VERIFICATION

  // SOURCE_TERM_SHA256 is recorded by the audit's byte-identity evidence.
  claim [module-load-pins-closure]:
    <k> #loadAll(
          Module ( FuncDef ( "valid_date" , Params ( "date" , .ParamNames ) , If ( Compare ( Call ( Name ( "len" ) , Name ( "date" ) , .Exprs ) , CmpOp ( "!=" , Int ( 10 ) ) ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  If ( Compare ( Subscript ( Name ( "date" ) , Int ( 2 ) ) , CmpOp ( "!=" , Str ( "-" ) ) ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  If ( Compare ( Subscript ( Name ( "date" ) , Int ( 5 ) ) , CmpOp ( "!=" , Str ( "-" ) ) ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  If ( BoolOp ( "or" , Compare ( Subscript ( Name ( "date" ) , Int ( 0 ) ) , CmpOp ( "<" , Str ( "0" ) ) ) , Compare ( Subscript ( Name ( "date" ) , Int ( 0 ) ) , CmpOp ( ">" , Str ( "9" ) ) ) , .Exprs ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  If ( BoolOp ( "or" , Compare ( Subscript ( Name ( "date" ) , Int ( 1 ) ) , CmpOp ( "<" , Str ( "0" ) ) ) , Compare ( Subscript ( Name ( "date" ) , Int ( 1 ) ) , CmpOp ( ">" , Str ( "9" ) ) ) , .Exprs ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  If ( BoolOp ( "or" , Compare ( Subscript ( Name ( "date" ) , Int ( 3 ) ) , CmpOp ( "<" , Str ( "0" ) ) ) , Compare ( Subscript ( Name ( "date" ) , Int ( 3 ) ) , CmpOp ( ">" , Str ( "9" ) ) ) , .Exprs ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  If ( BoolOp ( "or" , Compare ( Subscript ( Name ( "date" ) , Int ( 4 ) ) , CmpOp ( "<" , Str ( "0" ) ) ) , Compare ( Subscript ( Name ( "date" ) , Int ( 4 ) ) , CmpOp ( ">" , Str ( "9" ) ) ) , .Exprs ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  If ( BoolOp ( "or" , Compare ( Subscript ( Name ( "date" ) , Int ( 6 ) ) , CmpOp ( "<" , Str ( "0" ) ) ) , Compare ( Subscript ( Name ( "date" ) , Int ( 6 ) ) , CmpOp ( ">" , Str ( "9" ) ) ) , .Exprs ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  If ( BoolOp ( "or" , Compare ( Subscript ( Name ( "date" ) , Int ( 7 ) ) , CmpOp ( "<" , Str ( "0" ) ) ) , Compare ( Subscript ( Name ( "date" ) , Int ( 7 ) ) , CmpOp ( ">" , Str ( "9" ) ) ) , .Exprs ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  If ( BoolOp ( "or" , Compare ( Subscript ( Name ( "date" ) , Int ( 8 ) ) , CmpOp ( "<" , Str ( "0" ) ) ) , Compare ( Subscript ( Name ( "date" ) , Int ( 8 ) ) , CmpOp ( ">" , Str ( "9" ) ) ) , .Exprs ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  If ( BoolOp ( "or" , Compare ( Subscript ( Name ( "date" ) , Int ( 9 ) ) , CmpOp ( "<" , Str ( "0" ) ) ) , Compare ( Subscript ( Name ( "date" ) , Int ( 9 ) ) , CmpOp ( ">" , Str ( "9" ) ) ) , .Exprs ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  Assign ( Name ( "month_text" ) , Subscript ( Name ( "date" ) , Slice ( NoBound , Int ( 2 ) , NoBound ) ) )  Assign ( Name ( "day_text" ) , Subscript ( Name ( "date" ) , Slice ( Int ( 3 ) , Int ( 5 ) , NoBound ) ) )  Assign ( Name ( "month" ) , Call ( Name ( "int" ) , Name ( "month_text" ) , .Exprs ) )  Assign ( Name ( "day" ) , Call ( Name ( "int" ) , Name ( "day_text" ) , .Exprs ) )  If ( BoolOp ( "or" , Compare ( Name ( "month" ) , CmpOp ( "<" , Int ( 1 ) ) ) , Compare ( Name ( "month" ) , CmpOp ( ">" , Int ( 12 ) ) ) , .Exprs ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  If ( Compare ( Name ( "day" ) , CmpOp ( "<" , Int ( 1 ) ) ) , Return ( Bool ( false ) )  .Stmts , .Stmts )  If ( Compare ( Name ( "month" ) , CmpOp ( "==" , Int ( 2 ) ) ) , Return ( Compare ( Name ( "day" ) , CmpOp ( "<=" , Int ( 29 ) ) ) )  .Stmts , .Stmts )  If ( BoolOp ( "or" , Compare ( Name ( "month" ) , CmpOp ( "==" , Int ( 4 ) ) ) , Compare ( Name ( "month" ) , CmpOp ( "==" , Int ( 6 ) ) ) , Compare ( Name ( "month" ) , CmpOp ( "==" , Int ( 9 ) ) ) , Compare ( Name ( "month" ) , CmpOp ( "==" , Int ( 11 ) ) ) , .Exprs ) , Return ( Compare ( Name ( "day" ) , CmpOp ( "<=" , Int ( 30 ) ) ) )  .Stmts , .Stmts )  Return ( Compare ( Name ( "day" ) , CmpOp ( "<=" , Int ( 31 ) ) ) )  .Stmts )  .Stmts )
        ) => .K
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "valid_date" |-> validDateClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
