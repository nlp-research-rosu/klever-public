requires "verification.k"

module SPEC
  imports MPY-VERIFICATION

  // Structural proof of the filter algorithm.  The base case plus one rule
  // for every PyVal constructor characterize lists of arbitrary finite
  // length: integer instances are prepended, every other head is skipped,
  // and the same comprehension processes the symbolic tail VS.
  claim <k>
          comprehend(VList(.PyVals), "value", Name("value"),
            filterCondition(), _ENV)
          => VList(.PyVals)
        </k>

  claim <k>
          comprehend(VList(VInt(I), VS), "value", Name("value"),
            filterCondition(), ENV)
          => prepend(VInt(I),
               comprehend(VList(VS), "value", Name("value"),
                 filterCondition(), ENV))
        </k>

  claim <k>
          comprehend(VList(VBool(B), VS), "value", Name("value"),
            filterCondition(), ENV)
          => prepend(VBool(B),
               comprehend(VList(VS), "value", Name("value"),
                 filterCondition(), ENV))
        </k>

  claim <k>
          comprehend(VList(VString(_S), VS), "value", Name("value"),
            filterCondition(), ENV)
          => comprehend(VList(VS), "value", Name("value"),
               filterCondition(), ENV)
        </k>

  claim <k>
          comprehend(VList(VFloat(_F), VS), "value", Name("value"),
            filterCondition(), ENV)
          => comprehend(VList(VS), "value", Name("value"),
               filterCondition(), ENV)
        </k>

  claim <k>
          comprehend(VList(VList(_INNER), VS), "value", Name("value"),
            filterCondition(), ENV)
          => comprehend(VList(VS), "value", Name("value"),
               filterCondition(), ENV)
        </k>

  claim <k>
          comprehend(VList(VDict, VS), "value", Name("value"),
            filterCondition(), ENV)
          => comprehend(VList(VS), "value", Name("value"),
               filterCondition(), ENV)
        </k>

  claim <k>
          comprehend(VList(VNone, VS), "value", Name("value"),
            filterCondition(), ENV)
          => comprehend(VList(VS), "value", Name("value"),
               filterCondition(), ENV)
        </k>

  claim <k>
          comprehend(VList(VOpaque(_O), VS), "value", Name("value"),
            filterCondition(), ENV)
          => comprehend(VList(VS), "value", Name("value"),
               filterCondition(), ENV)
        </k>

  // Semantic lemma: the list-comprehension evaluator agrees with an
  // independently defined stable-filter model on a heterogeneous example.
  claim <k>
          eval(filterExpression(),
            bind("values",
              VList(VString("a"), VFloat("3.14"), VInt(5)), .Env))
          => VList(onlyIntegerInstances(
               VString("a"), VFloat("3.14"), VInt(5)))
        </k>

  // The two examples in the HumanEval prompt, proved through module loading,
  // name binding, function invocation, and comprehension evaluation.
  claim
      <k> bootstrap ~> invoke("filter_integers",
            VList(VString("a"), VFloat("3.14"), VInt(5))) => .K </k>
      <program> solutionModule() </program>
      <functions>
        .Functions
        =>
        bindFunction("filter_integers",
          function("values", Return(filterExpression())), .Functions)
      </functions>
      <env>
        .Env
        =>
        bind("values",
          VList(VString("a"), VFloat("3.14"), VInt(5)), .Env)
      </env>
      <return> noResult => result(VList(VInt(5))) </return>

  claim
      <k> bootstrap ~> invoke("filter_integers",
            VList(VInt(1), VInt(2), VInt(3), VString("abc"),
                  VDict, VList(.PyVals))) => .K </k>
      <program> solutionModule() </program>
      <functions>
        .Functions
        =>
        bindFunction("filter_integers",
          function("values", Return(filterExpression())), .Functions)
      </functions>
      <env>
        .Env
        =>
        bind("values",
          VList(VInt(1), VInt(2), VInt(3), VString("abc"),
                VDict, VList(.PyVals)), .Env)
      </env>
      <return>
        noResult => result(VList(VInt(1), VInt(2), VInt(3)))
      </return>

  // Boundary cases: empty input and Python's bool-is-an-int behavior.
  claim <k>
          eval(filterExpression(), bind("values", VList(.PyVals), .Env))
          => VList(.PyVals)
        </k>

  claim <k>
          eval(filterExpression(),
            bind("values",
              VList(VBool(true), VBool(false), VInt(0),
                    VInt(-4), VFloat("2.0")), .Env))
          => VList(VBool(true), VBool(false), VInt(0), VInt(-4))
        </k>

  // Symbolic payloads cover every runtime value constructor.  This checks
  // type selection independently of particular integer/string contents.
  claim <k>
          eval(filterExpression(),
            bind("values",
              VList(VString(S), VFloat(F), VInt(I), VBool(B),
                    VList(INNER), VDict, VNone, VOpaque(O), VInt(J)),
              .Env))
          => VList(onlyIntegerInstances(
               VString(S), VFloat(F), VInt(I), VBool(B),
               VList(INNER), VDict, VNone, VOpaque(O), VInt(J)))
        </k>

  // Postcondition witnesses: every value in each computed result is an int
  // instance, while order and duplicates are retained by the model.
  claim <k>
          containsOnlyIntegerInstances(
            onlyIntegerInstances(
              VString("x"), VInt(2), VInt(2), VDict,
              VBool(true), VFloat("2.0"), VInt(-1)))
          => true
        </k>

  claim <k>
          onlyIntegerInstances(
            VString("x"), VInt(2), VInt(2), VDict,
            VBool(true), VFloat("2.0"), VInt(-1))
          => VInt(2), VInt(2), VBool(true), VInt(-1)
        </k>
endmodule
