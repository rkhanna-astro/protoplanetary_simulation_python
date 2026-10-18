def funbvpk(Ktest):
    global Cs0

    Cs_end = process(Ktest)
    res_cs = Cs_end - Cs0
    return res_cs

# Example usage
Cs0 = 10  # Example global variable
def process(Ktest):
    # Example process function
    return Ktest * 2

Ktest = 5
result = funbvpk(Ktest)
print(result)