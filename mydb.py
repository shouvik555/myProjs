from tmpdb import simpleDB

myDB=simpleDB('test.txt')
td = {"id":"smondal", "fname":"Shouvik", "lname":"Mondal"}
myDB.write(td)
