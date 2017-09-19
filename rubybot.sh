cd ~/rubybot-v3/
echo Rubybot.sh started
cp rubybot_v3.py rubybot_v3.pre.bak
echo starting up at `date`

python3 rubybot_v3.py

echo Crashed at `date`

cp rubybot_v3.py rubybot_v3.post.bak

bash rubybot.sh &