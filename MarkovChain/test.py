
class cc(object):
    def __init__(self):
        self.cc = 1

def test(newOb):
    newOb.cc = 2

a = cc()
test(a)
f = open('./output/Markov.csv', 'w')
print(a.cc,file = f)
f.close()