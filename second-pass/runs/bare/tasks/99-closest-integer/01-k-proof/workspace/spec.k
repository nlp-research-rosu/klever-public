requires "verification.k"

module SPEC
  imports VERIFICATION

  // One symbolic execution covers every exact rational value N/D (D > 0),
  // hence in particular every finite decimal string.
  claim
    <k> solutionProgram => .K </k>
    <arg> rationalString(N, D) </arg>
    <env> .Map =>
      ("value" |-> rationalString(N, D)
       "number" |-> exactNum(N, D)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(roundNearestAway(N, D)) </result>
    requires D >Int 0

  // The two equidistant families establish the required away-from-zero tie
  // behavior for every integer magnitude.
  claim
    <k> solutionProgram => .K </k>
    <arg> rationalString((2 *Int I) +Int 1, 2) </arg>
    <env> .Map =>
      ("value" |-> rationalString((2 *Int I) +Int 1, 2)
       "number" |-> exactNum((2 *Int I) +Int 1, 2)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(I +Int 1) </result>
    requires I >=Int 0

  claim
    <k> solutionProgram => .K </k>
    <arg> rationalString(0 -Int ((2 *Int I) +Int 1), 2) </arg>
    <env> .Map =>
      ("value" |-> rationalString(0 -Int ((2 *Int I) +Int 1), 2)
       "number" |-> exactNum(0 -Int ((2 *Int I) +Int 1), 2)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(0 -Int (I +Int 1)) </result>
    requires I >=Int 0

  // Representative symbolic intervals on both sides of each half boundary.
  claim
    <k> solutionProgram => .K </k>
    <arg> rationalString((4 *Int I) +Int 1, 4) </arg>
    <env> .Map =>
      ("value" |-> rationalString((4 *Int I) +Int 1, 4)
       "number" |-> exactNum((4 *Int I) +Int 1, 4)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(I) </result>
    requires I >=Int 0

  claim
    <k> solutionProgram => .K </k>
    <arg> rationalString((4 *Int I) +Int 3, 4) </arg>
    <env> .Map =>
      ("value" |-> rationalString((4 *Int I) +Int 3, 4)
       "number" |-> exactNum((4 *Int I) +Int 3, 4)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(I +Int 1) </result>
    requires I >=Int 0

  claim
    <k> solutionProgram => .K </k>
    <arg> rationalString(0 -Int ((4 *Int I) +Int 1), 4) </arg>
    <env> .Map =>
      ("value" |-> rationalString(0 -Int ((4 *Int I) +Int 1), 4)
       "number" |-> exactNum(0 -Int ((4 *Int I) +Int 1), 4)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(0 -Int I) </result>
    requires I >=Int 0

  claim
    <k> solutionProgram => .K </k>
    <arg> rationalString(0 -Int ((4 *Int I) +Int 3), 4) </arg>
    <env> .Map =>
      ("value" |-> rationalString(0 -Int ((4 *Int I) +Int 3), 4)
       "number" |-> exactNum(0 -Int ((4 *Int I) +Int 3), 4)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(0 -Int (I +Int 1)) </result>
    requires I >=Int 0

  // Original examples exercise the concrete decimal-string parser too.
  claim
    <k> solutionProgram => .K </k>
    <arg> pyStr("10") </arg>
    <env> .Map =>
      ("value" |-> pyStr("10")
       "number" |-> exactNum(10, 1)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(10) </result>

  claim
    <k> solutionProgram => .K </k>
    <arg> pyStr("15.3") </arg>
    <env> .Map =>
      ("value" |-> pyStr("15.3")
       "number" |-> exactNum(153, 10)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(15) </result>

  claim
    <k> solutionProgram => .K </k>
    <arg> pyStr("14.5") </arg>
    <env> .Map =>
      ("value" |-> pyStr("14.5")
       "number" |-> exactNum(145, 10)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(15) </result>

  claim
    <k> solutionProgram => .K </k>
    <arg> pyStr("-14.5") </arg>
    <env> .Map =>
      ("value" |-> pyStr("-14.5")
       "number" |-> exactNum(-145, 10)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(-15) </result>
endmodule
