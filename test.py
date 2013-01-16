from twisterclient import TwisterClient as TC

tc = TC("http://monty.ccnmtl.columbia.edu:8823/")
print tc.beta(n=10,alpha=1,beta=2).values
print tc.expo(n=10,lambd=5).values
print tc.randint(n=10,a=0,b=100).values
