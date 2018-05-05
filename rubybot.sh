cd ~/rubybot-v3/
echo Rubybot.sh started
cp rubybot_v3.py rubybot_v3.pre.bak

while true
do
	echo Compressing logs
	zip logs.zip -rf logs
	echo Reloading git
	sh git.sh
	echo starting up at `date`
	echo starting up at `date` >/dev/stderr
	python3 rubybot_v3.py
	echo Crashed at `date`
	echo Crashed at `date` >/dev/stderr
	cat "last_trace.log"
	cp rubybot_v3.py rubybot_v3.post.bak
done
