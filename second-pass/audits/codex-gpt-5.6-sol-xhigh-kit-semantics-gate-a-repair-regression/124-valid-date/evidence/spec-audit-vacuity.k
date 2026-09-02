requires "verification.k"

module AUDIT-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation: the prompt example 06-04-2020 is valid.
  // The unchanged program and validDate10 both evaluate to true; demanding
  // false changes the result-constraining obligation.
  claim [false-six-april]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(
           Name("valid_date"),
           (str(dateCodes(48, 54, 45, 48, 52, 45, 50, 48, 50, 48)),
            .Exprs)
         )
      => false
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
