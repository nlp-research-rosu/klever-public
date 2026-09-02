requires "verification-body-mutated.k"

module PROGRAM-PINNING-BODY-MUTATED
  imports MATCH-PARENS-VERIFICATION-BODY-MUTATED

  // All right-hand sides below are generated from solution.py by the trusted
  // translator's constructor tree, not copied from verification.k.
  claim
    <k> isGoodBody => Return(Str("")) .Stmts </k>
    <env> ENV:Int </env>
    <scopes> SCOPES:Map </scopes>
    <scopeLoc> SCOPELOC:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> RET:RetState </ret>
    <exc> EXC:Exc </exc>
    <exit-code> EXITCODE:Int </exit-code>
    [label(pinIsGoodBody)]
  claim
    <k> matchParensBody => If(Call(Name("is_good"), BinOp("+", Subscript(Name("lst"), Int(0)), Subscript(Name("lst"), Int(1)))), Return(Str("Yes")) .Stmts, .Stmts) If(Call(Name("is_good"), BinOp("+", Subscript(Name("lst"), Int(1)), Subscript(Name("lst"), Int(0)))), Return(Str("Yes")) .Stmts, .Stmts) Return(Str("No")) .Stmts </k>
    <env> ENV:Int </env>
    <scopes> SCOPES:Map </scopes>
    <scopeLoc> SCOPELOC:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> RET:RetState </ret>
    <exc> EXC:Exc </exc>
    <exit-code> EXITCODE:Int </exit-code>
    [label(pinMatchParensBody)]
  claim
    <k> isGoodClosure => closureVal(("s", .ParamNames), Return(Str("")) .Stmts, 0) </k>
    <env> ENV:Int </env>
    <scopes> SCOPES:Map </scopes>
    <scopeLoc> SCOPELOC:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> RET:RetState </ret>
    <exc> EXC:Exc </exc>
    <exit-code> EXITCODE:Int </exit-code>
    [label(pinIsGoodClosure)]
  claim
    <k> matchParensClosure => closureVal(("lst", .ParamNames), If(Call(Name("is_good"), BinOp("+", Subscript(Name("lst"), Int(0)), Subscript(Name("lst"), Int(1)))), Return(Str("Yes")) .Stmts, .Stmts) If(Call(Name("is_good"), BinOp("+", Subscript(Name("lst"), Int(1)), Subscript(Name("lst"), Int(0)))), Return(Str("Yes")) .Stmts, .Stmts) Return(Str("No")) .Stmts, 0) </k>
    <env> ENV:Int </env>
    <scopes> SCOPES:Map </scopes>
    <scopeLoc> SCOPELOC:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> RET:RetState </ret>
    <exc> EXC:Exc </exc>
    <exit-code> EXITCODE:Int </exit-code>
    [label(pinMatchParensClosure)]

endmodule
