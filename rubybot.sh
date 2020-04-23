cd ~/rubybot-v3/
echo Rubybot.sh started

while true
do
	echo Compressing logs

	if [ "$(ls -A /media/usb/)" ]; then
	    zip_target=/media/usb/discord.zip
	else
	    zip_target=./discord.zip
	fi

	if [ ! -f ${zip_target} ]; then
	    zip ${zip_target} -r logs &
	else
	    zip ${zip_target} -rf logs &
	fi

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
