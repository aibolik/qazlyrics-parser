arr = ["U+04D8", "U+04D9", "U+0492", "U+0493", "U+049A", "U+049B", "U+04A2", "U+04A3", "U+04E8", "U+04E9", "U+04B0", "U+04B1", "U+04AE", "U+04AF", "U+04BA", "U+04BB", "U+0406", "U+0456", ]

new = []

import string

for s in arr:
    st = string.replace(s, "U", "u")
    st = string.replace(st, "+", "")
    new.append(st)

for s in new:
    print s[0] + "'" + r'\u' + s[1:] + "'" + ",",
