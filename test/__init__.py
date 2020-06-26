import sys, os
testdir = os.path.dirname(__file__)
projdir = os.path.dirname(testdir)
srcdir = os.path.join(projdir, "src")
print(srcdir)
sys.path.insert(0, srcdir)