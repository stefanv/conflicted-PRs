.PHONY: all

PROJECTS=numpy scipy scikit-image networkx

all:
	@for p in $(PROJECTS); do \
		echo "Fetching data for $$p:"; \
		python conflicted_prs.py --org=$$p --repo=$$p > data/$$p.md; \
	done
