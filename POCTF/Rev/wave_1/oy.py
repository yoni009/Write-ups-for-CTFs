token_base = "3YJSvfUgzSASoaC3"
print("Length:", len(token_base))
# Let's check other potential 16-char cuts in that immediate vicinity
print(token_base[:-1]) # 15 chars
# What if the 3 at the end belongs to something else and the token is 16 chars from the 'Y'?
print("Alternative:", "3YJSvfUgzSASoaC3"[:-1]) # wait