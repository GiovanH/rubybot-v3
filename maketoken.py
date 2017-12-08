import pickle
filehandler = open("token", 'wb')
token=input()
pickle.dump(token, filehandler)
filehandler.close()
