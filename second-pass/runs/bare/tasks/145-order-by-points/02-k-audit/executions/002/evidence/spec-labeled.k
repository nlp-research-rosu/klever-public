requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [label(c01-score-neg12)]:
        <py>
          <k> pointScore(-12) => 1 </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>
  claim [label(c02-score-neg11)]:
        <py>
          <k> pointScore(-11) => 0 </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>
  claim [label(c03-score-neg1)]:
        <py>
          <k> pointScore(-1) => -1 </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>
  claim [label(c04-score-11)]:
        <py>
          <k> pointScore(11) => 2 </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>

  claim [label(c05-invoke)]:
        <py>
          <k>
            invokeOrder(ListVal(VS:Vals), solutionDefs)
            => ListVal(sortWith(VS, PointKey, solutionDefs))
          </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>

  claim [label(c06-sort-empty)]:
        <py>
          <k> sortWith(.Vals, PointKey, solutionDefs) => specSort(.Vals) </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>

  claim [label(c07-sort-single)]:
        <py>
          <k>
            sortWith(IntVal(N:Int), PointKey, solutionDefs)
            => specSort(IntVal(N))
          </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>

  claim [label(c08-insert-le)]:
        <py>
          <k>
            insertWith(
              IntVal(N:Int), (IntVal(M:Int), .Vals), PointKey, solutionDefs)
            => specInsert(IntVal(N), (IntVal(M), .Vals))
          </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>
    requires pointScore(N) <=Int pointScore(M)

  claim [label(c09-insert-gt)]:
        <py>
          <k>
            insertWith(
              IntVal(N:Int), (IntVal(M:Int), .Vals), PointKey, solutionDefs)
            => specInsert(IntVal(N), (IntVal(M), .Vals))
          </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>
    requires pointScore(N) >Int pointScore(M)

  claim [label(c10-example)]:
        <py>
          <k> init => .K </k>
          <program> solutionProgram </program>
          <input>
            ListExpr(Int(1), Int(11), Int(-1), Int(-11), Int(-12))
          </input>
          <output>
            NoValue =>
            ListVal(IntVal(-1), IntVal(-11), IntVal(1), IntVal(-12), IntVal(11))
          </output>
        </py>

  claim [label(c11-empty)]:
        <py>
          <k> init => .K </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue => ListVal(.Vals) </output>
        </py>

  claim [label(c12-stability)]:
        <py>
          <k> init => .K </k>
          <program> solutionProgram </program>
          <input> ListExpr(Int(12), Int(21), Int(-12), Int(3)) </input>
          <output>
            NoValue => ListVal(IntVal(-12), IntVal(12), IntVal(21), IntVal(3))
          </output>
        </py>

  claim [label(c13-is-ordered)]:
        <py>
          <k>
            isOrdered(
              IntVal(-1), IntVal(-11), IntVal(1), IntVal(-12), IntVal(11))
            => true
          </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>
endmodule
