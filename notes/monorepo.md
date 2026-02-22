# Notes on monorepo configuration

tl;dr: As of 2026-02-22, this is still harder than it needs to be.

## Locations for tests

It looks like the traditional pythonic idiom is to have tests not just distinct from the rest of the source, but also
from the specific packages they're testing:

```
src/
    some-package/
        __init__.py
tests/
    some-package/
        __init__.py
        test_some_method.py
```

This is, of course, madness.

I mean, it seems like there's good historical reason: their build tools were not great at making distinctions between "
things included into `dist`" versus not.
So the easiest fix was to just make sure tests were never in `src`.

This seems a little better today, but the "front-end/back-end build tools" thing has only made this murkier.

But you might also make the argument that you should only ever be testing the public API, so your tests should always
`from some_package import some_method` just like consuming code would do.
This is reasonable.
Except it starts to bump up against the magic of `PYTHONPATH`.

Should your `tests` directory have an `__init__.py` so you don't get errors about relative imports?
Should it be listed as its own `package` in the `pyproject.toml`?
Or have its own `pyproject.toml`?
Should it use uv workspaces?

Honestly, I have no clue.
I haven't found a single approach which Just Works.

For now, I've settled on:

1. Each package under `src` gets its own `tests`, so its tests are contiguous with its source.
2. Tests use relative imports, like `..whatever`, which means you need a `tests/__init__.py`.
3. Dist packagers need to know to exclude tests, if you prefer.
   (It's reasonable to intentionally distribute tests with your package, if you prefer.)
   To do this, you'll need to set up rules in `Manifest.in` or some equivalent.

This has drawbacks:

- You need to explicitly exclude test files from dist packages.
- You can't use full/absolute imports — they have to be relative.

I did also try just setting up sibling paths:

```
src/
    some-package/
    some-tackage-tests/
```

But I can't figure out how to tell uv that any `*-tests` directory is a workspace (which needs path magic) but
***is not*** a package (which needs to be built).

## Root versus package config

It looks like uv suffers from the same problem of any tool which tries to cover both project management and package
management — the two are distinct, with distinct use-cases.
Just like TypeScript and tsconfig.

(Java's `maven` figured this out, where the root pom is the project management and the leaf poms are the package
management. But it's still very confusing for devs.)

This repo ***does not*** have a `[project]` or `[build-system]` section in the root `pyproject.toml`.
It instead tries to use that root file only for project management — that is, high-level non-package-specific
dependencies and configuration.

The leaf `pyproject.toml` files in the packages then have their `[project]` and `[build-system]` set, but as little else
as possible.

***Note that this is not idiomatic/pythonic.***

Some tooling really struggles with this — especially the ones which rely on src-vs-flat layout detection and implicit
namespace detection.

## Namespaces

I'd love to publish packages such as `rickosborne.vote` instead of `rickosborne_vote`.
But uv and various build tools have Very Strong Opinions about how this should or should not work, and I've yet to find
the magic layout or configuration to get it to work.

In theory, it's supposed to be as easy as:

```
src/
    rickosborne/
        # no __init__.py here
        vote/
            __init__.py
            pyproject.toml  # project.name = "rickosborne.vote"
pyproject.toml  # no project
```

I also tried:

```
src/
    rickosborne/
        # no __init__.py here
        pyproject.toml  # maybe?  project.name = "rickosborne"?
        src/
            rickosborne_vote/
                pyproject.toml  # project.name = "rickosborne.vote"
                src/
                    __init__.py
pyproject.toml  # no project
```

This is, of course, ludicrous.
And it doesn't work.
But it seems like people swear it does work and is The Right Way.

I need to fiddle with it more.

## Multiple packages

This mostly falls under the sections above.
I'm not sure the current setup will work with multiple packages and inter-package dependencies.

## `src` vs flat layout

There are lots of tools in the ecosystem which prefer one layout over the other.
And a few tools which claim to support both, but really don't.

It would be nice if the `pyproject.toml` had a nice simple way of saying:

- This is the path to the workspace for `vote`.
- Within the `vote` workspace, the sources are here.
- When you bundle everything up, restructure it to eliminate `src` directories and the like.

That last point is a major perk of using flat layout, as then your dist matches your source.
It just requires lots of overhead in managing include/exclude rules.
