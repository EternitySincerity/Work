import hashlib
src='fdsfaasfdsafdsa'.encode('utf-8')
m2 = hashlib.md5()
m2.update(src)
print('\t'.join([src.decode('utf-8'),m2.hexdigest()]))
