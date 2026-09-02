requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-CORE

  syntax Stmts ::= "simplifyBody" | "simplifyLoopBody" [function, total]
  syntax Stmt ::= "simplifyReturn" [function, total]
  syntax Scope ::= simplifyScope(Val, Val, Int, Int, Int, Int, Int, Val)
                   [function, total]
  syntax Bool ::= validScan(IntSeq, Int, Int, Int, Int, Int)
                  [function, total]
                | scanResult(IntSeq, Int, Int, Int, Int, Int)
                  [function]
endmodule

module VERIFICATION-BASE
  imports VERIFICATION-SYNTAX
  imports MPY

  rule simplifyLoopBody =>
    If(
      Compare(Name("ch"), CmpOp("==", Str("/"))),
      Assign(Name("part"), BinOp("+", Name("part"), Int(1))) .Stmts,
      If(
        Compare(Name("part"), CmpOp("==", Int(0))),
        Assign(
          Name("a"),
          BinOp(
            "+",
            BinOp(
              "*",
              Name("a"),
              Int(10)),
            BinOp(
              "-",
              Call(Name("ord"), Name("ch"), .Exprs),
              Int(48)))) .Stmts,
        If(
          Compare(Name("part"), CmpOp("==", Int(1))),
          Assign(
            Name("b"),
            BinOp(
              "+",
              BinOp(
                "*",
                Name("b"),
                Int(10)),
              BinOp(
                "-",
                Call(Name("ord"), Name("ch"), .Exprs),
                Int(48)))) .Stmts,
          If(
            Compare(Name("part"), CmpOp("==", Int(2))),
            Assign(
              Name("c"),
              BinOp(
                "+",
                BinOp(
                  "*",
                  Name("c"),
                  Int(10)),
                BinOp(
                  "-",
                  Call(Name("ord"), Name("ch"), .Exprs),
                  Int(48)))) .Stmts,
            Assign(
              Name("d"),
              BinOp(
                "+",
                BinOp(
                  "*",
                  Name("d"),
                  Int(10)),
                BinOp(
                  "-",
                  Call(Name("ord"), Name("ch"), .Exprs),
                  Int(48)))) .Stmts) .Stmts) .Stmts) .Stmts) .Stmts

  rule simplifyReturn =>
    Return(
      Compare(
        BinOp(
          "%",
          BinOp("*", Name("a"), Name("c")),
          BinOp("*", Name("b"), Name("d"))),
        CmpOp("==", Int(0))))

  rule simplifyBody =>
    Assign(Name("part"), Int(0))
    Assign(Name("a"), Int(0))
    Assign(Name("b"), Int(0))
    Assign(Name("c"), Int(0))
    Assign(Name("d"), Int(0))
    Assign(Name("ch"), Str(""))
    For(
      Name("ch"),
      BinOp("+", BinOp("+", Name("x"), Str("/")), Name("n")),
      .Stmts)
    simplifyReturn
    .Stmts

  rule simplifyScope(X, N, P, A, B, C, D, CH) =>
    scope(
      "x" |-> X
      "n" |-> N
      "part" |-> P
      "a" |-> A
      "b" |-> B
      "c" |-> C
      "d" |-> D
      "ch" |-> CH,
      parent(0))

  rule validScan(.IntSeq, 0, _:Int, _:Int, _:Int, _:Int) => false
  rule validScan(.IntSeq, 1, _:Int, _:Int, _:Int, _:Int) => false
  rule validScan(.IntSeq, 2, _:Int, _:Int, _:Int, _:Int) => false
  rule validScan(.IntSeq, 3, A, B, C, D) =>
    A >Int 0 andBool B >Int 0 andBool C >Int 0 andBool D >Int 0
  rule validScan(iCons(CODE, REST), 0, A, B, C, D) =>
    (CODE ==Int 47 andBool validScan(REST, 1, A, B, C, D))
      orBool
    (isDigitC(CODE)
      andBool validScan(
        REST, 0, A *Int 10 +Int (CODE -Int 48), B, C, D))
  rule validScan(iCons(CODE, REST), 1, A, B, C, D) =>
    (CODE ==Int 47 andBool validScan(REST, 2, A, B, C, D))
      orBool
    (isDigitC(CODE)
      andBool validScan(
        REST, 1, A, B *Int 10 +Int (CODE -Int 48), C, D))
  rule validScan(iCons(CODE, REST), 2, A, B, C, D) =>
    (CODE ==Int 47 andBool validScan(REST, 3, A, B, C, D))
      orBool
    (isDigitC(CODE)
      andBool validScan(
        REST, 2, A, B, C *Int 10 +Int (CODE -Int 48), D))
  rule validScan(iCons(CODE, REST), 3, A, B, C, D) =>
    isDigitC(CODE)
      andBool validScan(
        REST, 3, A, B, C, D *Int 10 +Int (CODE -Int 48))
  rule validScan(_:IntSeq, _:Int, _:Int, _:Int, _:Int, _:Int) =>
    false
    [owise]

  rule scanResult(.IntSeq, 3, A, B, C, D) =>
    pyMod(A *Int C, B *Int D) ==Int 0
    requires A >Int 0 andBool B >Int 0
      andBool C >Int 0 andBool D >Int 0
  rule scanResult(iCons(47, REST), P, A, B, C, D) =>
    scanResult(REST, P +Int 1, A, B, C, D)
    requires 0 <=Int P andBool P <Int 3
  rule scanResult(iCons(CODE, REST), 0, A, B, C, D) =>
    scanResult(REST, 0, A *Int 10 +Int (CODE -Int 48), B, C, D)
    requires isDigitC(CODE)
  rule scanResult(iCons(CODE, REST), 1, A, B, C, D) =>
    scanResult(REST, 1, A, B *Int 10 +Int (CODE -Int 48), C, D)
    requires isDigitC(CODE)
  rule scanResult(iCons(CODE, REST), 2, A, B, C, D) =>
    scanResult(REST, 2, A, B, C *Int 10 +Int (CODE -Int 48), D)
    requires isDigitC(CODE)
  rule scanResult(iCons(CODE, REST), 3, A, B, C, D) =>
    scanResult(REST, 3, A, B, C, D *Int 10 +Int (CODE -Int 48))
    requires isDigitC(CODE)
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  rule [loop-digit-bridge]:
    <k>
      #loop(str(iCons(CODE, REST)), Name("ch"), LOOPBODY:Stmts)
      ~> RETSTMTS:Stmts
      ~> #endcall
      =>
      scanResult(iCons(CODE, REST), P, A, B, C, D)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       1 |-> CALLEESCOPE:Scope
       -1 |-> BUILTINSSCOPE:Scope)
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> BUILTINSSCOPE)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires LOOPBODY ==K simplifyLoopBody
     andBool RETSTMTS ==K (simplifyReturn .Stmts)
     andBool CALLEESCOPE
       ==K simplifyScope(XARG, NARG, P, A, B, C, D, OLDCH)
     andBool BUILTINSSCOPE ==K builtinsScope
     andBool 0 <=Int P andBool P <=Int 3
     andBool isDigitC(CODE)
     andBool validScan(iCons(CODE, REST), P, A, B, C, D)
    [priority(40)]

  rule [loop-slash-bridge]:
    <k>
      #loop(str(iCons(47, REST)), Name("ch"), LOOPBODY:Stmts)
      ~> RETSTMTS:Stmts
      ~> #endcall
      =>
      scanResult(iCons(47, REST), P, A, B, C, D)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       1 |-> CALLEESCOPE:Scope
       -1 |-> BUILTINSSCOPE:Scope)
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> BUILTINSSCOPE)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires LOOPBODY ==K simplifyLoopBody
     andBool RETSTMTS ==K (simplifyReturn .Stmts)
     andBool CALLEESCOPE
       ==K simplifyScope(XARG, NARG, P, A, B, C, D, OLDCH)
     andBool BUILTINSSCOPE ==K builtinsScope
     andBool 0 <=Int P andBool P <Int 3
     andBool validScan(iCons(47, REST), P, A, B, C, D)
    [priority(40)]
endmodule
