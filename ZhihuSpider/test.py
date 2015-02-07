import ConfigParser


# cf = ConfigParser.ConfigParser()
# cf.read('config.ini')

# print type(cf.items('info'))
# print dict(cf.items('info'))

a = {'z_c0' : "12314"}
# print type(a)
# for i in a.items():
#     print type(i)
print a.items()

cf = ConfigParser.ConfigParser()
cf.read('config.ini')
for c in a.items():
    cf.set('cookies', c[0], c[1])
print dict(cf.items('cookies'))
with open('config.ini', 'wb') as configfile:
    cf.write(configfile)