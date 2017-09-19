cd ~/discord/rubybot/
echo Rubybot.sh started
cp rubybot_2.py rubybot_2.py.pre.bak
echo starting up at `date`

python3 rubybot_2.py

echo Crashed at `date`

cp rubybot_2.py rubybot_2.py.post.bak

bash rubybot.sh 