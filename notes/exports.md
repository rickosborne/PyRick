# Exports

In the TypeScript/EcmaScript/JavaScript ecosystem, there's a concept of distinguishing a top-level value from an
exported value:

```javascript
// These are available to all other code in this file,
// but are not exported as part of this module's public API.
const someFunctionImpl = () => true;

// These are exported as part of the public API for this module.
export const SOME_VALUE = 123;
export const someFunction = () => {
  someFunctionImpl();
  return "abc";
};
```

Python doesn't exactly match this pattern.
There's no concept of `export`.
If a value is defined at the module level, it is exported.

There's one minor exception: values which start with `_` are exported, but they are not imported by default when using
`from whatever import *`.

(Which you shouldn't be using `import *` anyway. Who raised you?)

The `_` is also a signal to devs that they should pretend to ignore it, as it's an implementation detail.

# There's also no IIFE

"Aha!" you might say, "I can hide implementation details with closures and an IIFE!"

```javascript
export const memoizedWhatever = (() => {
  let value = undefined;
  return () => {
    value ??= someLongRunningCalculation();
    return value;
  };
})();
```

"Surely, I can do the same thing in Python! ... Right?"

No.
Well, not exactly.
Python doesn't really have a concept of a function expression.
It has `lambda`, but that is limited to a single expression only.

The closest equivalent would be a closure like:

```python
def _memoizeWhatever():
  value = None

  def memoized():
    nonlocal value
    if value is None:
      value = someLongRunningCalculation()

  return memoized


memoizedWhatever = _memoizeWhatever()
```

By prefixing the closure builder with `_`, that tells the importer and other devs that it's an internal implementation
detail of the module.
Python won't prevent them from importing and using it if they really want to, but it's as good as you can get.

A maybe more pythonic way of doing it might involve a class:

```python
class _WhateverMemoizer:
  value = None

  @classmethod
  def whatever(cls):
    if cls.value is None:
      cls.value = someLongRunningCalculation()
    return cls.value


memoizedWhatever = lambda _: _WhateverMemoizer().whatever()
```

But at that point, it would probably be more pythonic to just expose the class, move the class stuff to instance stuff,
and not try to wrap it in a function:

```python
class Whatever:
  def __init__(self):
    self.value = None

  def whatever(self):
    if self.value is None:
      self.value = someLongRunningCalculation()
    return self.value
```

It's also nice and easy to read.

Python devs will understand that the API is to just do:

```python
calculated = Whatever().whatever()
```

## What about `__all__`?

Technically, you can also control exports via `__all__`.
Sort of.

```python
# Note that this does not include `_memoizedWhatever`.
__all__ = ["memoizedWhatever"]
```

This is *almost* like the old `module.exports` from CJS.
It's a list of the top-level values which Python should treat as exported and as part of the public API.

Except ... not really.
Like the `_` pattern, it's really only a guide, and really only useful for `import *`.

It *can* be useful for the pythonic equivalent of TS/JS's barrel files:

```javascript
export {A} from "src/a.js";
export {B} from "src/b.js";
```

The equivalent in Python's `__init__.py`:

```python
from .src.a import A
from .src.b import B

__all__ = ["A"]
```

This would allow consumers of your package to simplify their imports:

```python
from your_package import A, B
```

This also makes it moderately clear that the public API is whatever is exported at the top-level, and not just anything
from anywhere in the package.
The downside, of course, is then maintaining that `__all__` list and the imports to power it.
Just like TS/JS barrel files.
