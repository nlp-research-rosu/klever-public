requires "verification.k"

module PROGRAM-PINNING-SPEC
  imports MATCH-PARENS-VERIFICATION

  // All right-hand sides below are generated from solution.py by the trusted
  // translator's constructor tree, not copied from verification.k.
  claim
    <k> isGoodLoopBody => If(Compare(Name("char"), CmpOp("==", Str("("))), AugAssign(Name("balance"), "+", Int(1)) .Stmts, AugAssign(Name("balance"), "-", Int(1)) .Stmts) If(Compare(Name("balance"), CmpOp("<", Int(0))), Return(Str("")) .Stmts, .Stmts) .Stmts </k>
    <env> ENV:Int </env>
    <scopes> SCOPES:Map </scopes>
    <scopeLoc> SCOPELOC:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> RET:RetState </ret>
    <exc> EXC:Exc </exc>
    <exit-code> EXITCODE:Int </exit-code>
    [label(pinIsGoodLoopBody)]

  claim
    <k> isGoodBody => Assign(Name("balance"), Int(0)) For(Name("char"), Name("s"), If(Compare(Name("char"), CmpOp("==", Str("("))), AugAssign(Name("balance"), "+", Int(1)) .Stmts, AugAssign(Name("balance"), "-", Int(1)) .Stmts) If(Compare(Name("balance"), CmpOp("<", Int(0))), Return(Str("")) .Stmts, .Stmts) .Stmts) If(Compare(Name("balance"), CmpOp("==", Int(0))), Return(Str("T")) .Stmts, .Stmts) Return(Str("")) .Stmts </k>
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
    <k> isGoodClosure => closureVal(("s", .ParamNames), Assign(Name("balance"), Int(0)) For(Name("char"), Name("s"), If(Compare(Name("char"), CmpOp("==", Str("("))), AugAssign(Name("balance"), "+", Int(1)) .Stmts, AugAssign(Name("balance"), "-", Int(1)) .Stmts) If(Compare(Name("balance"), CmpOp("<", Int(0))), Return(Str("")) .Stmts, .Stmts) .Stmts) If(Compare(Name("balance"), CmpOp("==", Int(0))), Return(Str("T")) .Stmts, .Stmts) Return(Str("")) .Stmts, 0) </k>
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
