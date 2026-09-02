requires "verification.k"

module SPEC
  imports VERIFICATION

  // End-to-end executions through loading, environments, control flow,
  // arithmetic, collection, and sorting.
  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 1 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult => result(vl(1 :: .Ints)) </result>
    </python>

  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 2 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult => result(vl(1 :: .Ints)) </result>
    </python>

  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 3 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult => result(vl(1 :: 3 :: 5 :: .Ints)) </result>
    </python>

  // This is the example required by prompt.py.
  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 5 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult => result(vl(1 :: 5 :: .Ints)) </result>
    </python>

  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 6 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult => result(vl(1 :: 3 :: 5 :: .Ints)) </result>
    </python>

  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 7 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result>
        noResult => result(vl(1 :: 5 :: 7 :: 11 :: 13 :: 17 :: .Ints))
      </result>
    </python>

  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 19 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result>
        noResult =>
          result(vl(1 :: 5 :: 11 :: 13 :: 17 :: 19 :: 29 :: .Ints))
      </result>
    </python>

  // A long trajectory (112 Collatz transitions) stress-tests the loop.
  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 27 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result>
        noResult => result(vl(
          1 :: 5 :: 23 :: 27 :: 31 :: 35 :: 41 :: 47 :: 53 :: 61 ::
          71 :: 91 :: 103 :: 107 :: 121 :: 137 :: 155 :: 161 :: 167 ::
          175 :: 233 :: 251 :: 263 :: 283 :: 319 :: 325 :: 377 :: 395 ::
          425 :: 433 :: 445 :: 479 :: 577 :: 593 :: 719 :: 911 :: 1079 ::
          1367 :: 1619 :: 2051 :: 2429 :: 3077 :: .Ints))
      </result>
    </python>

  // Symbolic branch correctness for every positive even current term.
  claim [even-step]:
    <python>
      <k> exec(collatzBranch .Stmts) => .K </k>
      <input> 0 </input>
      <functions> .Map </functions>
      <env>
        ("n" |-> vi(2 *Int M) "odds" |-> vl(OS))
        => ("n" |-> vi(M) "odds" |-> vl(OS))
      </env>
      <result> noResult </result>
    </python>
    requires M >Int 0

  // Symbolic branch correctness for every odd term greater than one.
  claim [odd-step]:
    <python>
      <k> exec(collatzBranch .Stmts) => .K </k>
      <input> 0 </input>
      <functions> .Map </functions>
      <env>
        ("n" |-> vi(2 *Int M +Int 1) "odds" |-> vl(OS))
        => ("n" |-> vi(6 *Int M +Int 4)
            "odds" |-> vl(appendInts(OS, (2 *Int M +Int 1) :: .Ints)))
      </env>
      <result> noResult </result>
    </python>
    requires M >Int 0

  // Independent checks on the observers used to state the output contract.
  claim
    <python>
      <k> checkSorted(17 :: 1 :: 7 :: 5 :: 13 :: 11 :: .Ints)
            => true </k>
      <input> 0 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>

  claim
    <python>
      <k> checkAllOdd(17 :: 1 :: 7 :: 5 :: 13 :: 11 :: .Ints)
            => true </k>
      <input> 0 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
endmodule
