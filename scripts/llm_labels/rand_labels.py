P,K,E,V,X,B,G,A,L='paksaan','ketidakpercayaan','eksklusi','privasi','exit_siasat','beban','gagal_teknis','patuh_menerima','lainnya'
R={}
def add(start,rows):
    assert all(len(r.split(','))==10 for r in rows), [len(r.split(',')) for r in rows]
    for i,x in enumerate(','.join(rows).split(',')): R[start+i]=eval(x)
add(0,["L,G,G,A,B,A,P,A,P,A","A,A,G,B,G,A,G,X,G,L","B,G,B,G,G,G,A,L,X,P","G,B,A,A,G,B,G,L,A,A",
"G,A,L,G,A,B,A,A,A,A","X,G,A,G,A,B,G,L,A,A","B,A,A,G,B,A,L,E,B,G","A,E,A,G,G,A,G,B,A,L",
"L,A,G,B,G,A,B,L,G,P","G,A,A,A,A,A,A,A,G,G","A,B,K,P,A,A,A,B,L,A","B,A,G,B,A,G,G,A,A,G",
"G,X,A,G,E,G,A,G,A,B","B,G,G,G,L,L,L,A,B,B","A,E,B,A,L,B,B,G,P,L"])
add(150,["G,B,G,G,A,G,A,A,B,B","X,A,G,P,B,G,A,G,B,A","A,G,A,A,A,G,B,G,A,B","A,A,X,G,G,L,L,A,A,B",
"A,G,A,G,G,A,A,A,L,B","A,G,A,A,B,B,B,G,A,A","A,A,G,A,G,X,A,A,P,A","L,L,A,B,A,G,G,B,A,P",
"A,L,A,G,A,A,A,B,G,K","A,A,A,A,P,L,B,B,P,A","G,L,G,A,A,A,L,L,A,G","G,B,A,B,A,A,B,G,G,B",
"A,P,G,B,L,B,G,A,L,L","L,G,G,G,L,A,A,B,A,L","A,G,G,G,A,A,A,A,L,A"])
add(300,["K,A,G,A,A,A,A,G,A,P","A,G,G,B,A,G,L,G,A,A","L,G,A,G,G,G,A,A,B,G","B,A,G,A,A,L,A,B,B,A",
"A,B,G,B,B,A,A,A,P,B","A,A,A,B,K,G,B,G,L,P","K,A,A,A,A,A,B,B,L,G","G,G,G,A,A,A,G,A,L,G",
"B,A,A,G,L,B,G,A,L,G","L,G,A,A,A,A,K,G,A,L","K,A,B,G,L,A,G,G,A,A","G,A,L,G,G,G,A,B,A,B",
"A,G,A,L,A,B,B,B,B,K","B,A,A,A,P,G,B,B,G,A","X,A,A,A,G,A,A,L,A,A"])
