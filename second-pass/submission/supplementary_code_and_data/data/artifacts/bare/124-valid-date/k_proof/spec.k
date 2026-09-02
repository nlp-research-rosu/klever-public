requires "verification.k"

module VALID-DATE-SPEC
  imports VALID-DATE-VERIFICATION

  // The examples in the prompt.
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("03-11-2000")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("15-01-2012")))
          => boolVal(false) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("04-0-2040")))
          => boolVal(false) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("06-04-2020")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("06/04/2020")))
          => boolVal(false) </k>

  // Empty, wrong-width, wrong-separator, and non-digit inputs.
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("")))
          => boolVal(false) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("03-11-200")))
          => boolVal(false) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("003-11-2000")))
          => boolVal(false) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("aa-bb-cccc")))
          => boolVal(false) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("03-1a-2000")))
          => boolVal(false) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("03-11-20x0")))
          => boolVal(false) </k>

  // Month and lower-day boundaries.
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("00-01-2020")))
          => boolVal(false) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("13-01-2020")))
          => boolVal(false) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("12-00-2020")))
          => boolVal(false) </k>

  // February has 1..29 days; leap-year arithmetic is intentionally absent
  // from the stated HumanEval contract.
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("02-01-2020")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("02-29-1900")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("02-30-2020")))
          => boolVal(false) </k>

  // The four 30-day months.
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("04-30-2020")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("04-31-2020")))
          => boolVal(false) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("06-30-2020")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("06-31-2020")))
          => boolVal(false) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("09-30-2020")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("09-31-2020")))
          => boolVal(false) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("11-30-2020")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("11-31-2020")))
          => boolVal(false) </k>

  // The seven 31-day months and unrestricted four-digit year field.
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("01-31-0000")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("03-31-9999")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("05-31-2020")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("07-31-2020")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("08-31-2020")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("10-31-2020")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("12-31-2020")))
          => boolVal(true) </k>
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("01-32-2020")))
          => boolVal(false) </k>

  // Symbolic arithmetic partition: D is arbitrary in each claim. Together
  // these claims cover every in-range month and establish its exact day cap.
  claim <k> boolVal(validMonthDay(2, D))
          => boolVal(D >=Int 1 andBool D <=Int 29) </k>

  claim <k> boolVal(validMonthDay(4, D))
          => boolVal(D >=Int 1 andBool D <=Int 30) </k>
  claim <k> boolVal(validMonthDay(6, D))
          => boolVal(D >=Int 1 andBool D <=Int 30) </k>
  claim <k> boolVal(validMonthDay(9, D))
          => boolVal(D >=Int 1 andBool D <=Int 30) </k>
  claim <k> boolVal(validMonthDay(11, D))
          => boolVal(D >=Int 1 andBool D <=Int 30) </k>

  claim <k> boolVal(validMonthDay(1, D))
          => boolVal(D >=Int 1 andBool D <=Int 31) </k>
  claim <k> boolVal(validMonthDay(3, D))
          => boolVal(D >=Int 1 andBool D <=Int 31) </k>
  claim <k> boolVal(validMonthDay(5, D))
          => boolVal(D >=Int 1 andBool D <=Int 31) </k>
  claim <k> boolVal(validMonthDay(7, D))
          => boolVal(D >=Int 1 andBool D <=Int 31) </k>
  claim <k> boolVal(validMonthDay(8, D))
          => boolVal(D >=Int 1 andBool D <=Int 31) </k>
  claim <k> boolVal(validMonthDay(10, D))
          => boolVal(D >=Int 1 andBool D <=Int 31) </k>
  claim <k> boolVal(validMonthDay(12, D))
          => boolVal(D >=Int 1 andBool D <=Int 31) </k>

  // All out-of-range months and all sub-one days are rejected symbolically.
  claim <k> boolVal(validMonthDay(M, _D)) => boolVal(false) </k>
    requires M <Int 1 orBool M >Int 12
  claim <k> boolVal(validMonthDay(M, D)) => boolVal(false) </k>
    requires M >=Int 1 andBool M <=Int 12 andBool D <Int 1
endmodule
