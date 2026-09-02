requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [empty-contract]:
    <k> boot(solutionProgram) => .K </k>
    <input> input(.Ints) </input>
    <function> .Function => function("arr", solutionBody) </function>
    <env> .Map => "arr" |-> listVal(.Ints) </env>
    <result> noResult => result(contract(.Ints)) </result>

  claim [nonempty-initialization]:
    <k> boot(solutionProgram)
      => loop("x", X, IS, solutionLoopBody)
      ~> exec(Return(BinOp("*", Name("total"), Name("sign"))) .Stmts)
    </k>
    <input> input(X, IS) </input>
    <function> .Function => function("arr", solutionBody) </function>
    <env> .Map =>
      "arr" |-> listVal(X, IS)
      "total" |-> 0
      "sign" |-> 1
      "x" |-> 0
    </env>
    <result> noResult </result>

  claim [negative-step]:
    <k> loop("x", X, IS, solutionLoopBody) => loop("x", IS, solutionLoopBody) ...</k>
    <env>
      RHO:Map
      "x" |-> _OLD:Int
      "total" |-> T:Int
      "sign" |-> S:Int
      => RHO
         "x" |-> X
         "total" |-> T +Int magnitude(X)
         "sign" |-> S *Int integerSign(X)
    </env>
    requires X <Int 0

  claim [positive-step]:
    <k> loop("x", X, IS, solutionLoopBody) => loop("x", IS, solutionLoopBody) ...</k>
    <env>
      RHO:Map
      "x" |-> _OLD:Int
      "total" |-> T:Int
      "sign" |-> S:Int
      => RHO
         "x" |-> X
         "total" |-> T +Int magnitude(X)
         "sign" |-> S *Int integerSign(X)
    </env>
    requires X >Int 0

  claim [zero-step]:
    <k> loop("x", X, IS, solutionLoopBody) => loop("x", IS, solutionLoopBody) ...</k>
    <env>
      RHO:Map
      "x" |-> _OLD:Int
      "total" |-> T:Int
      "sign" |-> S:Int
      => RHO
         "x" |-> 0
         "total" |-> T +Int magnitude(X)
         "sign" |-> S *Int integerSign(X)
    </env>
    requires X ==Int 0

  claim [loop-exit]:
    <k> loop("x", .Ints, solutionLoopBody)
      ~> exec(Return(BinOp("*", Name("total"), Name("sign"))) .Stmts)
      => .K
    </k>
    <env> _RHO:Map "total" |-> T:Int "sign" |-> S:Int </env>
    <result> noResult => result(T *Int S) </result>

  claim [example-negative]:
    <k> boot(solutionProgram) => .K </k>
    <input> input(1, 2, 2, -4) </input>
    <function> .Function => function("arr", solutionBody) </function>
    <env> .Map =>
      "arr" |-> listVal(1, 2, 2, -4)
      "total" |-> 9
      "sign" |-> -1
      "x" |-> -4
    </env>
    <result> noResult => result(contract(1, 2, 2, -4)) </result>

  claim [example-zero]:
    <k> boot(solutionProgram) => .K </k>
    <input> input(0, 1) </input>
    <function> .Function => function("arr", solutionBody) </function>
    <env> .Map =>
      "arr" |-> listVal(0, 1)
      "total" |-> 1
      "sign" |-> 0
      "x" |-> 1
    </env>
    <result> noResult => result(contract(0, 1)) </result>

  claim [example-three-negative]:
    <k> boot(solutionProgram) => .K </k>
    <input> input(-1, -2, -3) </input>
    <function> .Function => function("arr", solutionBody) </function>
    <env> .Map =>
      "arr" |-> listVal(-1, -2, -3)
      "total" |-> 6
      "sign" |-> -1
      "x" |-> -3
    </env>
    <result> noResult => result(contract(-1, -2, -3)) </result>
endmodule
