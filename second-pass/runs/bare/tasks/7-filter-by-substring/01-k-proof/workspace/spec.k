requires "verification.k"

module SPEC
  imports VERIFICATION

  // The exact translated program reduces, for arbitrary inputs, to the
  // generic list-comprehension evaluator.  The base and two exhaustive step
  // claims prove that evaluator equal to filterRef by induction on PyList.
  claim <k> execute(solutionProgram,
                    "filter_by_substring",
                    INPUT:PyList,
                    SUBSTRING:String)
          => evalComp(INPUT,
                      substringFilter(SUBSTRING))
        </k>
    [label(UNIVERSAL-PROGRAM-REDUCTION)]

  claim <k> evalComp(Nil,
                     substringFilter(SUBSTRING:String))
          => filterRef(Nil, SUBSTRING)
        </k>
    [label(UNIVERSAL-BASE)]

  claim <k> evalComp(Cons(HEAD:String, TAIL:PyList),
                     substringFilter(SUBSTRING:String))
          => filterRef(Cons(HEAD, TAIL), SUBSTRING)
        </k>
    requires containsString(HEAD, SUBSTRING)
             andBool
             (evalComp(TAIL,
                       substringFilter(SUBSTRING))
              ==K filterRef(TAIL, SUBSTRING))
    [label(UNIVERSAL-STEP-KEEP)]

  claim <k> evalComp(Cons(HEAD:String, TAIL:PyList),
                     substringFilter(SUBSTRING:String))
          => filterRef(Cons(HEAD, TAIL), SUBSTRING)
        </k>
    requires notBool containsString(HEAD, SUBSTRING)
             andBool
             (evalComp(TAIL,
                       substringFilter(SUBSTRING))
              ==K filterRef(TAIL, SUBSTRING))
    [label(UNIVERSAL-STEP-DROP)]

  claim <k> execute(solutionProgram,
                    "filter_by_substring",
                    Nil,
                    "a")
          => Nil
        </k>
    [label(EMPTY-EXAMPLE)]

  claim <k> execute(solutionProgram,
                    "filter_by_substring",
                    Cons("abc", Cons("bacd", Cons("cde", Cons("array", Nil)))),
                    "a")
          => Cons("abc", Cons("bacd", Cons("array", Nil)))
        </k>
    [label(PROMPT-EXAMPLE)]
endmodule
