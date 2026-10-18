T = [73, 74, 75, 71, 69, 72, 76, 73]

# 1 1 4 ...

stack = []
ans = [0]*len(T)

for i in range(len(T)):
    temp = T[i]

    if stack:
        top = stack[-1]
        while stack and T[i] > top[0]:
            top, ind = stack.pop()
            ans[ind] = i - ind

            if stack:
                top = stack[-1]
        
    stack.append((T[i], i))

print(ans)




