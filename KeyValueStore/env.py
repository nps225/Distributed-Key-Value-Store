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
   "c":"test"
}

compare0 = {
   "a":[1,0],
   "b":[2,0],
   "c":[3,0]
}

compare1 = {
   "a":ts,
   "b":ts,
   "c":ts
}

# c,b = test.returnTablesDict()
# print(test.dict)
print(test.comparison(compare,compare0,compare1))
# print(test.dict)
# # print(c == compare)




