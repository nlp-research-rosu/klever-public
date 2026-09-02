import Klean54SameChars.Inj

axiom _Set_ (x0 : SortSet) (x1 : SortSet) : Option SortSet

axiom «.Map» : Option SortMap

axiom SetItem (x0 : SortKItem) : Option SortSet

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.Set» : Option SortSet

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap