def split_list(lst,nb): 
    # ln = length of smaller sublists 
    # extra = number of longer sublists (they have ln+1 items) 
    ln,extra = divmod(len(lst),nb) 
    pos = ln*(nb-extra) # position where larger sublists begin 
    return [ lst[i*ln:(i+1)*ln] for i in xrange(nb-extra) ] + [lst[pos+i*(ln+1):pos+(i+1)*(ln+1)] for i in xrange(extra)]
x = range(1,8009)
c = 0
for ln in  split_list(x,50):
    print len(ln)
    c += 1
print c