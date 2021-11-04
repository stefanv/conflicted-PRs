## Set up token

Generate a personal access token on GitHub.  Add `repo` permissions.

```
export GH_TOKEN="abcdefg"
```

## Pull PR data

```
make
```

Usually, GitHub doesn't have the mergeable status available on the
first run.  If you see "UNKNOWN" in the output data file, simply run
`make` again.

## Plot histogram of PRs

```
cd data
python hist-prs.py
```
