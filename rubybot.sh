cd ~/rubybot-v3/
echo Rubybot.sh started

while true
do
	echo Compressing logs
	zip logs.zip -rf logs
	echo Reloading git
	./git.sh > git.log
	echo starting up at `date`
	echo starting up at `date` >/dev/stderr
	python3 super_rubybot.py
	echo Crashed at `date`
	echo Crashed at `date` >/dev/stderr
#	cat "last_trace.log"
	sleep 1  # in case of fastloop
done
