class yrange:
	def __init__(self, n):
		self.n = n
		self.i = n - 1

	def __iter__(self):
		return self

	def next(self):
		if self.i >= 0:
			i = self.i
			self.i -= 1
			return i
		else:
			return None

print type(yrange(3))


def yyrange(n):
	i = 0
	while i < n:
		yield i
		i += 1

print type(yyrange(3))

class A:
	b = B()

class B:
	a = A()