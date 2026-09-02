requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  claim [body-sensitive-entry]:
    <bt>
      <k> boot => .K </k>
      <program> bodyMutatedProgram </program>
      <input> XS:IntSeq </input>
      <threshold> T:Int </threshold>
      <l> unbound => slot(VList(XS)) </l>
      <t> unbound => slot(VInt(T)) </t>
      <x> unbound => ?_FINAL_X:Slot </x>
      <result>
        noResult => result(allBelowBodyMutation(XS, T))
      </result>
    </bt>
endmodule
