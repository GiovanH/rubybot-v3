async def sent_message(msg):
  print(mg)

with open("last_trace.log",'r') as tracefile:
    brk = tracefile.read()
    await send_message("I just came online. Last error: \n" + brk)
