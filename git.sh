#/bin/bash
git commit frogs.frog -m "routine frog update"
git push
git fetch --all
git reset --hard origin/master
chmod +777 -R *