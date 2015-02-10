def yrange(n):
    i = 0
    while i < n:
        yield i
        i += 1



a = yrange(3)

print type(a.next())