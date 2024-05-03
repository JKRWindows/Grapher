# Getting Started
Add this repo as a submodule with:
```bash
git add submodule https://github.com/JKRWindows/Grapher
```

Then the object can be initialized started with:
```py
import Grapher

dot = Grapher.Dot('filename', 'png')
```

You must write to the file with a context manager:
```py
with Grapher.Dot('filename', 'png') as f:
    f.write('digraph { a -> b }')
```

This will automatically handle opening and closing the stdin pipe to `dot`.  