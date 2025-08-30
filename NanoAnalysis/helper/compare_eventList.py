a = []
b = []

with open('reza.tex') as f:
   content=f.readlines()
   for line in content:
       a.append(line.strip())
       if 'str' in line:
          break

with open('henry.tex') as f:
   for line in f:
       b.append(line.strip())
       if 'str' in line:
          break
#b= Apr21_PhB.Apr21_PhB
print 'what Reza has but Henry does not'
c = set(a) - set(b)
print c

print "what Henry has but Reza does not"
d = set(b) - set(a)
print d
