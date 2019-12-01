#serve as our testing env for store.py
from store import Store
import time
#create an instance of a store
test = Store()
ts = time.time()
test.upsertValue("a","mitchell")
test.upsertVC("a",[1,0])
test.upsertTimestamp("a",ts)
test.upsertValue("b","temp")
test.upsertVC("b",[2,0])
test.upsertTimestamp("b",ts)
# test.upsertValue("c","confirmed")
# test.upsertVC("c",[3,0])

# print(test.getValue("a"))
# print(test.getValue("d"))

print(test.returnTablesDict())
compare = {
   "a":"mitchell",
   "b":"cant",
   "c":"works"
}

compare0 = {
   "a":[1,1],
   "b":[2,0],
   "c":[4,0]
}

compare1 = {
   "a":ts,
   "b":ts+1,
   "c":ts+2
}

# c,b = test.returnTablesDict()
# print(test.dict)
print(test.comparison(compare,compare0,compare1))
# print(test.dict)
# # print(c == compare)




