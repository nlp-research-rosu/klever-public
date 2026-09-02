requires "verification.k"

module SPEC
  imports VERIFICATION

  // The prompt's signed-leading-digit scoring convention.
  claim <py>
          <k> pointScore(-12) => 1 </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>
  claim <py>
          <k> pointScore(-11) => 0 </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>
  claim <py>
          <k> pointScore(-1) => -1 </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>
  claim <py>
          <k> pointScore(11) => 2 </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>

  // For every list of integer values, the translated function selects the
  // semantics' stable key-sort with precisely the PointKey denotation.
  claim <py>
          <k>
            invokeOrder(ListVal(VS:Vals), solutionDefs)
            => ListVal(sortWith(VS, PointKey, solutionDefs))
          </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>

  // Base cases and both exhaustive comparison branches relate the executable
  // sorter to the independent stable-sort equations in verification.k.
  claim <py>
          <k> sortWith(.Vals, PointKey, solutionDefs) => specSort(.Vals) </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>

  claim <py>
          <k>
            sortWith(IntVal(N:Int), PointKey, solutionDefs)
            => specSort(IntVal(N))
          </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>

  claim <py>
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

  claim <py>
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

  // End-to-end examples from the prompt plus boundary and stability cases.
  claim <py>
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

  claim <py>
          <k> init => .K </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue => ListVal(.Vals) </output>
        </py>

  claim <py>
          <k> init => .K </k>
          <program> solutionProgram </program>
          <input> ListExpr(Int(12), Int(21), Int(-12), Int(3)) </input>
          <output>
            NoValue => ListVal(IntVal(-12), IntVal(12), IntVal(21), IntVal(3))
          </output>
        </py>

  claim <py>
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
