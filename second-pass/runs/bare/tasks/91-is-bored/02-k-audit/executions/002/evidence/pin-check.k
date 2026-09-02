requires "verification.k"

module PIN-CHECK
  imports VERIFICATION

  claim <k> done </k>
        <program> solutionModule =>
          Module ( FuncDef ( "is_bored" , Params ( "S" ) , Assign ( Name ( "count" ) , Int ( 0 ) )  For ( Name ( "sentence" ) , Call ( Attribute ( Call ( Attribute ( Call ( Attribute ( Name ( "S" ) , "replace" ) , Str ( "!" ) , Str ( "." ) , .Exprs ) , "replace" ) , Str ( "?" ) , Str ( "." ) , .Exprs ) , "split" ) , Str ( "." ) , .Exprs ) , If ( Call ( Attribute ( Call ( Attribute ( Name ( "sentence" ) , "strip" ) , .Exprs ) , "startswith" ) , Str ( "I " ) , .Exprs ) , AugAssign ( Name ( "count" ) , "+" , Int ( 1 ) )  .Stmts , .Stmts )  .Stmts )  Return ( Name ( "count" ) )  .Stmts )  .Stmts ) </program>
        <input> "" </input>
        <result> 0 </result>

endmodule
