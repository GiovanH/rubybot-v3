#/bin/bash -v
git fetch --all
git commit jobj/* -m "routine object update"
git merge --no-edit
git push
#git reset --hard origin/master
#chmod +777 -R *
git status
git show
