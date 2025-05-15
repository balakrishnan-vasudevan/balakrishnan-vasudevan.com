
Script
```
#!/bin/bash
WATCH_DIR="/Users/bvasudevan/Documents/Notes_Vault/Notes"
DEBOUNCE_SECONDS=600

cd "$WATCH_DIR"

while true; do
  # Wait for a change
  fswatch -1 "$WATCH_DIR"
  # Wait for a quiet period
  sleep "$DEBOUNCE_SECONDS"
  # If there are changes, commit and push
  git add .
  msg="edits - $(date '+%m%d%Y %H%M')"
  if ! git diff --cached --quiet; then
    git commit -am "$msg"
    git push
  fi
done
```

fswatch

```
nohup fswatch -o /Users/bvasudevan/Documents/Notes_Vault/Notes | xargs -n1 ~/Repos/Scripts/git_auto_push.sh > ~/Repos/Scripts/fswatch.log  2>&1 &
```


```
ps aux | grep fswatch

bvasudevan       54230   0.0  0.0 410724160   1520 s002  S+   10:40AM   0:00.01 grep fswatch

bvasudevan       53984   0.0  0.0 410604448   5504 s002  SN   10:40AM   0:00.01 fswatch -o /Users/bvasudevan/Documents/Notes_Vault/Notes
```
