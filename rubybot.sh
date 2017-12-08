cd ~/rubybot-v3/
echo Rubybot.sh started
cp rubybot_v3.py rubybot_v3.pre.bak

while true
do
	echo Reloading git
	sh git.sh
	echo starting up at `date`
	python3 rubybot_v3.py
	echo Crashed at `date`
	cat "last_trace.log"
	cp rubybot_v3.py rubybot_v3.post.bak
done
