requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false result mutation.  At S = "" and C = "", execution
  // returns an empty result string, not "X".
  claim <k>
          execute(solutionPgm, S:String, C:String)
          => returned(
               tupleVal(
                 strVal("X" +String deleteChars(S, C)),
                 boolVal(deleteChars(S, C)
                         ==String reverseString(deleteChars(S, C)))))
        </k>
endmodule
