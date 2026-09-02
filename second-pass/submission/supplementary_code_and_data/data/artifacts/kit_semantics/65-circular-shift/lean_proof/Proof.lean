import Klean65CircularShift.Lemmas

namespace Proof

/- KORE symbol: LblInt2String'LParUndsRParUnds'STRING-COMMON'Unds'String'Unds'Int; frozen source obligations: rule-c953bda1443d09246288e179353879835e55885076958d7951972dec67e512cf. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «Int2String(_)_STRING-COMMON_String_Int» (value : SortInt) : SortString :=
  value.repr

private def asciiChar (character : Char) : Prop :=
  character.toNat < 128

private def allAscii : List Char → Prop
  | [] => True
  | character :: rest => asciiChar character ∧ allAscii rest

private def strToCodesList : List Char → Option SortIntSeq
  | [] => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | character :: rest =>
      if character.toNat < 128 then
        match strToCodesList rest with
        | some codes =>
            some
              (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                (Int.ofNat character.toNat) codes)
        | none => none
      else
        none

/- KORE symbol: LblstrToCodes'LParUndsRParUnds'MPY-STR'Unds'IntSeq'Unds'String; frozen source obligations: rule-c953bda1443d09246288e179353879835e55885076958d7951972dec67e512cf. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «strToCodes(_)_MPY-STR_IntSeq_String?» (value : SortString) : Option SortIntSeq :=
  strToCodesList value.toList

private theorem decimalDigitAscii (value : Nat) :
    asciiChar (Nat.digitChar (value % 10)) := by
  have bound : value % 10 < 10 := Nat.mod_lt value (by decide)
  have alternatives :
      value % 10 = 0 ∨ value % 10 = 1 ∨ value % 10 = 2 ∨
      value % 10 = 3 ∨ value % 10 = 4 ∨ value % 10 = 5 ∨
      value % 10 = 6 ∨ value % 10 = 7 ∨ value % 10 = 8 ∨
      value % 10 = 9 := by
    omega
  rcases alternatives with
    alternative | alternative | alternative | alternative | alternative |
    alternative | alternative | alternative | alternative | alternative <;>
    simp [alternative, asciiChar, Nat.digitChar]

private theorem toDigitsCoreAllAscii
    (fuel value : Nat) (accumulator : List Char)
    (accumulatorAscii : allAscii accumulator) :
    allAscii (Nat.toDigitsCore 10 fuel value accumulator) := by
  induction fuel generalizing value accumulator with
  | zero =>
      simpa [Nat.toDigitsCore] using accumulatorAscii
  | succ fuel inductionHypothesis =>
      simp only [Nat.toDigitsCore]
      split
      · change asciiChar (Nat.digitChar (value % 10)) ∧ allAscii accumulator
        exact ⟨decimalDigitAscii value, accumulatorAscii⟩
      · apply inductionHypothesis
        change asciiChar (Nat.digitChar (value % 10)) ∧ allAscii accumulator
        exact ⟨decimalDigitAscii value, accumulatorAscii⟩

private theorem natDigitsAllAscii (value : Nat) :
    allAscii (Nat.toDigits 10 value) := by
  unfold Nat.toDigits
  apply toDigitsCoreAllAscii
  trivial

private theorem intReprAllAscii (value : Int) :
    allAscii value.repr.toList := by
  cases value with
  | ofNat natural =>
      simpa [Int.repr, Nat.repr, List.asString] using
        natDigitsAllAscii natural
  | negSucc natural =>
      simp only [Int.repr, Nat.repr, List.asString]
      change asciiChar '-' ∧ allAscii (Nat.toDigits 10 natural.succ)
      exact ⟨by unfold asciiChar; decide, natDigitsAllAscii natural.succ⟩

private theorem strToCodesListIsSome
    (characters : List Char) (charactersAscii : allAscii characters) :
    (strToCodesList characters).isSome = true := by
  revert charactersAscii
  induction characters with
  | nil =>
      intro _
      rfl
  | cons character rest inductionHypothesis =>
      intro charactersAscii
      have headAscii : asciiChar character := charactersAscii.1
      have tailAscii : allAscii rest := charactersAscii.2
      have tailSome := inductionHypothesis tailAscii
      unfold asciiChar at headAscii
      simp only [strToCodesList, if_pos headAscii]
      cases encodedRest : strToCodesList rest with
      | none =>
          simp [encodedRest] at tailSome
      | some codes =>
          rfl

theorem final :
    Klean65CircularShift.Lemmas.targetStatement «Int2String(_)_STRING-COMMON_String_Int» «strToCodes(_)_MPY-STR_IntSeq_String?» := by
  unfold Klean65CircularShift.Lemmas.targetStatement
  intro value
  have encoded :
      («strToCodes(_)_MPY-STR_IntSeq_String?»
        («Int2String(_)_STRING-COMMON_String_Int» value)).isSome = true := by
    apply strToCodesListIsSome
    exact intReprAllAscii value
  simp [encoded]

end Proof
