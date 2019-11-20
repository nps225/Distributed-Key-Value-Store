#serve as our testing env for store.py
from store import Store

#create an instance of a store
test = Store()

test.upsertValue("a","mitchell")
test.upsertValue("b","temp")
test.upsertValue("c","confirmed")

print(test.getValue("a"))
print(test.getValue("d"))

print(test.deleteValue("a"))

test.returnStore()




