#serve as our testing env for store.py
from store import Store

#create an instance of a store
test = Store()



test.upsertValue("a","mitchell")
test.upsertValue("b","temp")
test.upsertValue("c","confirmed")

# print(test.getValue("a"))
# print(test.getValue("d"))

print(test.returnTablesDict())

compare = {
   "a":"mitchell",
   "c":"test",
   "d":"works?"
}

c,b = test.returnTablesDict()
print(test.dict)
print(test.compare(compare,{}))
print(test.dict)
# print(c == compare)




