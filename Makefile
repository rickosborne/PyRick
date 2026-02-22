package_names := $(shell find src -type d -depth 1 -name 'rickosborne*' -not -name '*.egg-info')

.PHONY: test
test:
	@.venv/bin/python -m pytest

.PHONY: build
build:
	$(foreach pkg, $(package_names), ~/.local/bin/uv build $(pkg))
	# Another option:
	# ~/.local/bin/uv build --all-packages

#.PHONY: types
#types:
#	@.venv/bin/basedpyright --createstub rickosborne_vote

.PHONY: clean
clean:
	rm -Rf ./dist \
		./src/rickosborne_vote/*.egg-info \
		./scripts/*.egg-info \
		./*.egg-info

.PHONY: version-bump
version-bump:
	@.venv/bin/python scripts/version-bump.py

.PHONY: version-bump-commit
version-bump-commit:
	@.venv/bin/python scripts/version-bump.py --commit
