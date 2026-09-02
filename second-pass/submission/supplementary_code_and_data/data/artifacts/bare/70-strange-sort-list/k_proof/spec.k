requires "verification.k"

module SPEC
  imports VERIFICATION

  // Base cases quantify the singleton value over all mathematical integers.
  claim
    <program> solutionProgram </program>
    <input> nil </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(nil)) </result>
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, nil) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, nil))) </result>

  // Exhaustive insertion-sort path partitions for symbolic lengths 2, 3,
  // and 4.  Each family covers every ordering, equality, and sign choice.
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, nil)) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, nil)))) </result>
    requires A <=Int B
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, nil)) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, nil)))) </result>
    requires A >Int B
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, nil))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, nil))))) </result>
    requires B <=Int C andBool A <=Int B
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, nil))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, nil))))) </result>
    requires B <=Int C andBool A >Int B andBool A <=Int C
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, nil))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, nil))))) </result>
    requires B <=Int C andBool A >Int C
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, nil))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, nil))))) </result>
    requires B >Int C andBool A <=Int C
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, nil))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, nil))))) </result>
    requires B >Int C andBool A >Int C andBool A <=Int B
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, nil))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, nil))))) </result>
    requires B >Int C andBool A >Int B
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C <=Int D andBool B <=Int C andBool A <=Int B
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C <=Int D andBool B <=Int C andBool A >Int B andBool A <=Int C
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C <=Int D andBool B <=Int C andBool A >Int C andBool A <=Int D
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C <=Int D andBool B <=Int C andBool A >Int D
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C <=Int D andBool B >Int C andBool B <=Int D andBool A <=Int C
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C <=Int D andBool B >Int C andBool B <=Int D andBool A >Int C andBool A <=Int B
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C <=Int D andBool B >Int C andBool B <=Int D andBool A >Int B andBool A <=Int D
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C <=Int D andBool B >Int C andBool B <=Int D andBool A >Int D
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C <=Int D andBool B >Int D andBool A <=Int C
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C <=Int D andBool B >Int D andBool A >Int C andBool A <=Int D
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C <=Int D andBool B >Int D andBool A >Int D andBool A <=Int B
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C <=Int D andBool B >Int D andBool A >Int B
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C >Int D andBool B <=Int D andBool A <=Int B
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C >Int D andBool B <=Int D andBool A >Int B andBool A <=Int D
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C >Int D andBool B <=Int D andBool A >Int D andBool A <=Int C
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C >Int D andBool B <=Int D andBool A >Int C
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C >Int D andBool B >Int D andBool B <=Int C andBool A <=Int D
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C >Int D andBool B >Int D andBool B <=Int C andBool A >Int D andBool A <=Int B
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C >Int D andBool B >Int D andBool B <=Int C andBool A >Int B andBool A <=Int C
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C >Int D andBool B >Int D andBool B <=Int C andBool A >Int C
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C >Int D andBool B >Int C andBool A <=Int D
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C >Int D andBool B >Int C andBool A >Int D andBool A <=Int C
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C >Int D andBool B >Int C andBool A >Int C andBool A <=Int B
  claim
    <program> solutionProgram </program>
    <input> cons(A:Int, cons(B:Int, cons(C:Int, cons(D:Int, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(strangeSpec(cons(A, cons(B, cons(C, cons(D, nil)))))) </result>
    requires C >Int D andBool B >Int C andBool A >Int B

  // The examples from prompt.py are also stated verbatim.
  claim
    <program> solutionProgram </program>
    <input> cons(1, cons(2, cons(3, cons(4, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(cons(1, cons(4, cons(2, cons(3, nil))))) </result>
  claim
    <program> solutionProgram </program>
    <input> cons(5, cons(5, cons(5, cons(5, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(cons(5, cons(5, cons(5, cons(5, nil))))) </result>
  claim
    <program> solutionProgram </program>
    <input> nil </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(nil) </result>

  // Additional unsorted, negative, odd-length execution checks.
  claim
    <program> solutionProgram </program>
    <input> cons(3, cons(-1, cons(2, cons(3, cons(0, nil))))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(cons(-1, cons(3, cons(0, cons(3, cons(2, nil)))))) </result>
  claim
    <program> solutionProgram </program>
    <input> cons(4, cons(1, cons(7, cons(2, cons(6, nil))))) </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(cons(1, cons(7, cons(2, cons(6, cons(4, nil)))))) </result>
endmodule

