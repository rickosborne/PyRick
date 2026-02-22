package_names := $(shell find packages -type d -depth 1 -name rickosborne*)

.PHONY: test
test:
	@.venv/bin/python -m pytest packages

.PHONY: build
build:
	$(foreach pkg, $(package_names), ~/.local/bin/uv build $(pkg))

#.PHONY: types
#types:
#	@.venv/bin/basedpyright --createstub rickosborne_vote

.PHONY: clean
clean:
	rm -Rf ./dist \
		./packages/rickosborne_vote/src/rickosborne_vote.egg-info \
		./scripts/rickosborne_scripts.egg-info

.PHONY: version-bump
version-bump:
	@.venv/bin/python scripts/version-bump.py

.PHONY: version-bump-commit
version-bump-commit:
	@.venv/bin/python scripts/version-bump.py --commit
