i=['tic', 'tac', 'toe'];
i=sorted(i); 
print(i);
i=reversed(i);
print(i);
def update(*args,**kwargs):
    p=' 1=1 '
    for i,t in kwargs.items():
        p = p+ 'and %s=%s ' %(i,str(t))
        sql = "update  'user' set (%s) where %s" %(args[0],p.strip(', '))
    print(sql)

update('aaa',uu='\'uu\'',id=3)
