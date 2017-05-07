import re

W_R = r"\d\s*(?=:)"

m = re.search(W_R, " 2:  0 12 ")
print(m.group("weight"))
