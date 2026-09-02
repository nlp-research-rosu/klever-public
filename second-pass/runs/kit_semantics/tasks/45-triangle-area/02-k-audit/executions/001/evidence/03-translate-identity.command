python3 py2mpy.py solution.py > solution.regenerated.mpy && cmp -s solution.regenerated.mpy solution.mpy && sha256sum solution.py solution.mpy solution.regenerated.mpy
