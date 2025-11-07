import uuid

print("uuid1:", uuid.uuid1())
print("-----------")
print("uuid4:", uuid.uuid4())
print("-----------")
print("uuid3:", uuid.uuid3(uuid.NAMESPACE_DNS, "python.org"))
print("-----------")
print("uuid5:", uuid.uuid5(uuid.NAMESPACE_DNS, "python.org"))
