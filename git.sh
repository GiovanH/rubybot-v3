#/bin/bash -v
git fetch --all
git commit frogs.frog rules rules/* -m "routine frog update"
git merge --no-edit
git push
#git reset --hard origin/master
#chmod +777 -R *
git show > git.log
