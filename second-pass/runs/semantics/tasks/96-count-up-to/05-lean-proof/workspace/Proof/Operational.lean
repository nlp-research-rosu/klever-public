import Proof.KMapTactic

/-- A direct packaging of MPY's ordinary local-scope lookup rule.  The
premises are precisely the generated hook equations needed by that rule. -/
theorem Rewrites.localLookup
    (L : SortInt) (M outer scopes singleton : SortMap)
    (X : SortString) (V : SortVal) (parent : SortParent)
    {rest : SortK}
    {env : SortEnvCell} {scopeLoc : SortScopeLocCell}
    {heap : SortHeapCell} {heapLoc : SortHeapLocCell}
    {stack : SortStackCell} {ret : SortRetCell} {exc : SortExcCell}
    {exitCode : SortExitCodeCell}
    {generatedCounter : SortGeneratedCounterCell}
    (contains :
      «_in_keys(_)_MAP_Bool_KItem_Map» ((@inj SortString SortKItem) X) M =
        some true)
    (makeScope :
      _root_.«_|->_» ((@inj SortInt SortKItem) L)
          ((@inj SortScope SortKItem)
            (.«scope(_,_)_MPY-CORE_Scope_Map_Parent» M parent)) =
        some singleton)
    (joinScope : _root_._Map_ singleton outer = some scopes)
    (lookup :
      «Map:lookup» M ((@inj SortString SortKItem) X) =
        some ((@inj SortVal SortKItem) V))
    (project :
      «project:Val»
          (.kseq ((@inj SortVal SortKItem) V) .dotk) =
        some V) :
    Rewrites
      { k := { val := .kseq (.«#look(_,_)_MPY-CORE_KItem_String_Int» X L) rest }
        env := env
        scopes := { val := scopes }
        scopeLoc := scopeLoc
        heap := heap
        heapLoc := heapLoc
        stack := stack
        ret := ret
        exc := exc
        exitCode := exitCode
        generatedCounter := generatedCounter }
      { k := { val := .kseq ((@inj SortVal SortKItem) V) rest }
        env := env
        scopes := { val := scopes }
        scopeLoc := scopeLoc
        heap := heap
        heapLoc := heapLoc
        stack := stack
        ret := ret
        exc := exc
        exitCode := exitCode
        generatedCounter := generatedCounter } := by
  exact Rewrites._db779c6
    (M := M)
    (_DotVar2 := outer)
    (_Gen0 := parent)
    (_Val0 := true)
    (_Val1 := singleton)
    (_Val2 := scopes)
    (_Val3 := (@inj SortVal SortKItem) V)
    (_Val4 := V)
    (_Val5 := singleton)
    (_Val6 := scopes)
    contains makeScope joinScope lookup project makeScope joinScope rfl

/-- A direct packaging of MPY's ordinary assignment-to-local rule. -/
theorem Rewrites.localAssign
    (L : SortInt) (M updated outer scopes newScopes singleton newSingleton : SortMap)
    (X : SortString) (V : SortVal) (parent : SortParent)
    {rest : SortK}
    {scopeLoc : SortScopeLocCell} {heap : SortHeapCell}
    {heapLoc : SortHeapLocCell} {stack : SortStackCell}
    {ret : SortRetCell} {exc : SortExcCell}
    {exitCode : SortExitCodeCell}
    {generatedCounter : SortGeneratedCounterCell}
    (makeScope :
      _root_.«_|->_» ((@inj SortInt SortKItem) L)
          ((@inj SortScope SortKItem)
            (.«scope(_,_)_MPY-CORE_Scope_Map_Parent» M parent)) =
        some singleton)
    (joinScope : _root_._Map_ singleton outer = some scopes)
    (update :
      «Map:update» M ((@inj SortString SortKItem) X)
          ((@inj SortVal SortKItem) V) =
        some updated)
    (makeNewScope :
      _root_.«_|->_» ((@inj SortInt SortKItem) L)
          ((@inj SortScope SortKItem)
            (.«scope(_,_)_MPY-CORE_Scope_Map_Parent» updated parent)) =
        some newSingleton)
    (joinNewScope :
      _root_._Map_ newSingleton outer = some newScopes) :
    Rewrites
      { k := { val := (SortK.kseq
          ((@inj SortStmt SortKItem)
            (.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
              (.«Name(_)_MPY-SYNTAX_Expr_String» X)
              ((@inj SortVal SortExpr) V)))
          rest) }
        env := { val := L }
        scopes := { val := scopes }
        scopeLoc := scopeLoc
        heap := heap
        heapLoc := heapLoc
        stack := stack
        ret := ret
        exc := exc
        exitCode := exitCode
        generatedCounter := generatedCounter }
      { k := { val := rest }
        env := { val := L }
        scopes := { val := newScopes }
        scopeLoc := scopeLoc
        heap := heap
        heapLoc := heapLoc
        stack := stack
        ret := ret
        exc := exc
        exitCode := exitCode
        generatedCounter := generatedCounter } := by
  exact Rewrites._e6f504a
    (M := M)
    (_DotVar2 := outer)
    (_Val0 := singleton)
    (_Val1 := scopes)
    (_Val2 := updated)
    (_Val3 := newSingleton)
    (_Val4 := newScopes)
    makeScope joinScope update makeNewScope joinNewScope

/-- A direct packaging of MPY's ordinary augmented assignment rule. -/
theorem Rewrites.localAugAssign
    (L : SortInt) (M updated outer scopes newScopes singleton newSingleton : SortMap)
    (X OP : SortString) (old rhs value : SortVal) (parent : SortParent)
    {rest : SortK}
    {scopeLoc : SortScopeLocCell} {heap : SortHeapCell}
    {heapLoc : SortHeapLocCell} {stack : SortStackCell}
    {ret : SortRetCell} {exc : SortExcCell}
    {exitCode : SortExitCodeCell}
    {generatedCounter : SortGeneratedCounterCell}
    (contains :
      «_in_keys(_)_MAP_Bool_KItem_Map» ((@inj SortString SortKItem) X) M =
        some true)
    (makeScope :
      _root_.«_|->_» ((@inj SortInt SortKItem) L)
          ((@inj SortScope SortKItem)
            (.«scope(_,_)_MPY-CORE_Scope_Map_Parent» M parent)) =
        some singleton)
    (joinScope : _root_._Map_ singleton outer = some scopes)
    (lookup :
      «Map:lookup» M ((@inj SortString SortKItem) X) =
        some ((@inj SortVal SortKItem) old))
    (project :
      «project:Val» (.kseq ((@inj SortVal SortKItem) old) .dotk) =
        some old)
    (applyBin :
      «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» OP old rhs =
        some value)
    (update :
      «Map:update» M ((@inj SortString SortKItem) X)
          ((@inj SortVal SortKItem) value) =
        some updated)
    (makeNewScope :
      _root_.«_|->_» ((@inj SortInt SortKItem) L)
          ((@inj SortScope SortKItem)
            (.«scope(_,_)_MPY-CORE_Scope_Map_Parent» updated parent)) =
        some newSingleton)
    (joinNewScope :
      _root_._Map_ newSingleton outer = some newScopes) :
    Rewrites
      { k := { val := (SortK.kseq
          ((@inj SortStmt SortKItem)
            (.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr»
              (.«Name(_)_MPY-SYNTAX_Expr_String» X) OP
              ((@inj SortVal SortExpr) rhs)))
          rest) }
        env := { val := L }
        scopes := { val := scopes }
        scopeLoc := scopeLoc
        heap := heap
        heapLoc := heapLoc
        stack := stack
        ret := ret
        exc := exc
        exitCode := exitCode
        generatedCounter := generatedCounter }
      { k := { val := rest }
        env := { val := L }
        scopes := { val := newScopes }
        scopeLoc := scopeLoc
        heap := heap
        heapLoc := heapLoc
        stack := stack
        ret := ret
        exc := exc
        exitCode := exitCode
        generatedCounter := generatedCounter } := by
  exact Rewrites._460aaab
    (M := M)
    (_DotVar2 := outer)
    (_Val0 := true)
    (_Val1 := singleton)
    (_Val2 := scopes)
    (_Val3 := (@inj SortVal SortKItem) old)
    (_Val4 := old)
    (_Val5 := value)
    (_Val6 := updated)
    (_Val7 := newSingleton)
    (_Val8 := newScopes)
    contains makeScope joinScope lookup project applyBin update
      makeNewScope joinNewScope rfl
