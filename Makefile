.PHONY: test
test:
	@.venv/bin/python -m pytest packages

.PHONY: build
build:
	@~/.local/bin/uv build packages/*

#.PHONY: types
#types:
#	@.venv/bin/basedpyright --createstub rickosborne_vote

.PHONY: clean
clean:
	rm -Rf ./dist ./packages/rickosborne_vote/src/rickosborne_vote.egg-info
