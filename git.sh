#/bin/bash
git commit frogs.frog rules rules/* -m "routine frog update"
git push
git fetch --all
git reset --hard origin/master
#chmod +777 -R *
git show | head -n 5 | tail -n 3 > git.log