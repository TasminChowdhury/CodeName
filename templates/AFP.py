# # author: Tasmin Chowdhury
#
# import string
# import re
#
# vectorlist = []
# Typearray = []
# stack = []
#
#
# def find_acronym(phrase, s):
#     # remove punctuation
#     exclude = set(string.punctuation)
#     exclude.discard('-')
#     phrase = ''.join(ch for ch in phrase if ch not in exclude)
#
#     # table = str.maketrans({key: N for key in string.punctuation})
#     # phrase = phrase.translate(table)
#     phrase = phrase.split()
#     acronym = [word for word in phrase if word.isupper()]
#     print(phrase)
#     print(acronym)
#     find_prewindow(acronym, phrase, s)
#
#
# def find_prewindow(acr, phr, s):
#     for a in range(len(acr)):
#         k = acr[a]
#         # print(k)
#         winsize = 2 * len(k)
#         print(winsize)
#         # typearray = [0]*winsize
#         acr_index = phr.index(k)
#         # print(acr_index)
#         # typearray[acr_index]='a'
#
#         first = acr_index - winsize
#         # print(first)
#         wordsin_window = phr[first:acr_index]
#         print(wordsin_window)
#         firstletterofwordsinwindow = acronym(wordsin_window, s)
#         firstletterofwordsinwindow = [c.lower() for c in firstletterofwordsinwindow]
#         print(firstletterofwordsinwindow)
#         lcs(k.lower(), firstletterofwordsinwindow)
#         if len(vectorlist) > 1:
#             definition_list = compare_vectors()
#         else:
#             definition_list = vectorlist[0]
#
#         for i in range(len(definition_list)):
#             if definition_list[i] > 0:
#                 first = i
#                 break
#         i = len(definition_list) - 1
#         while True:
#             if definition_list[i] > 0:
#                 last = i
#                 break
#         result = str(wordsin_window[first:last + 1])
#         print(acr[a], result)
#         print(Typearray)
#
#
# def acronym(phrase, s):
#     k = []
#     s_index = 0
#     n_index = 0
#
#     for word in phrase:
#         if re.findall(r'\w+-\w+[-\w+]*', word):
#             print(word)
#             hy_index = phrase.index(word)
#             # typearray[hy_index]='H'
#             Typearray.append('H')
#             hy_index += hy_index
#             # hyphenated = re.findall(r'\w+-\w+[-\w+]*',text)
#             m = word.split('-')
#             # print(hy_index)
#             # print(typearray)
#             for i in range(len(m)):
#                 k.append(m[i][0])
#                 if i < len(m) - 1:
#                     # typearray[hy_index]='h'
#                     Typearray.append('h')
#                     hy_index += hy_index
#                     # print(hy_index)
#                     # print(typearray)
#         elif word in s:
#             # print('stopword')
#             # print(word)
#             k.append(word[0])
#             s_index = phrase.index(word, s_index)
#             # print(s_index)
#             # typearray[s_index]='s'
#             Typearray.append('s')
#             # print(typearray)
#         else:
#             # print('normal')
#             k.append(word[0])
#             n_index = phrase.index(word, n_index)
#             # print(n_index)
#             # typearray[n_index]='w'
#             Typearray.append('w')
#             # print(typearray)
#     return k
#
#
# def lcs(X, Y):
#     # find the length of the strings
#     m = len(X)
#     n = len(Y)
#     # print(X,Y)
#     # declaring the array for storing the dp values
#     C = [[None] * (n + 1) for i in range(m + 1)]
#     # declaring array to store track
#     B = [[None] * (n + 1) for i in range(m + 1)]
#     for i in range(m + 1):
#         for j in range(n + 1):
#             if i == 0 or j == 0:
#                 C[i][j] = 0
#             elif X[i - 1] == Y[j - 1]:
#                 C[i][j] = C[i - 1][j - 1] + 1
#                 B[i][j] = 'c'
#             else:
#                 if C[i - 1][j] > C[i][j - 1]:
#                     C[i][j] = C[i - 1][j]
#                     B[i][j] = 'u'
#                 else:
#                     C[i][j] = C[i][j - 1]
#                     B[i][j] = 'l'
#     # print(C)
#     # print(B)
#     parse_LCS_matrix(B, 0, 0, m, n, C[m][n])
#
#
# def parse_LCS_matrix(B, start_i, start_j, m, n, lcs_length):
#     # print(lcs_length)
#     for i in range(start_i, m + 1):
#         for j in range(start_j, n + 1):
#             # print(B[i][j])
#             if B[i][j] == 'c':
#                 # print(i,j)
#                 stack.append([i, j])
#                 # print(stack)
#
#                 if lcs_length == 1:
#                     vector = build_vector(n)
#                     if vector not in vectorlist:
#                         vectorlist.append(vector)
#                     # print(vector)
#                     # print(vectorlist)
#                 else:
#                     parse_LCS_matrix(B, i + 1, j + 1, m, n, lcs_length - 1)
#
#
# def build_vector(n):
#     v = [0] * n
#     while stack:
#         k = stack.pop()
#         v[k[1] - 1] = k[0]
#     print(v)
#     # print(vectorlist)
#     return v
#
#
# def vector_values(V, T):
#     size = [0] * len(V)
#     distance = [0] * len(V)
#     stopcount = [0] * len(V)
#     misses = [0] * len(V)
#     for k in range(len(V)):
#         i = 0
#         while i < len(V[k]) - 1 and V[k][i] == 0:
#             i = i + 1
#         first = i
#         i = len(V[k]) - 1
#         while i > 0 and V[k][i] == 0:
#             i = i - 1
#         last = i
#         size[k] = last - first + 1
#         distance[k] = len(V[k]) - last - 1
#         for i in range(first, last):
#             if V[k][i] > 0 and T[i] == 's':
#                 stopcount[k] += 1
#             else:
#                 if V[k][i] == 0 and T[i] != 's' and T[i] != 'h':
#                     misses[k] += 1
#
#     return misses, stopcount, distance, size
#
#
# def comp_vector(A, B):
#     # print(vectorlist)
#     misses, stopcount, distance, size = vector_values(vectorlist, Typearray)
#     # print(misses)
#     # print(stopcount)
#     # print(distance)
#     # print(size)
#     A_index = vectorlist.index(A)
#     B_index = vectorlist.index(B)
#     # print(A,B)
#     # print(A_index,B_index)
#     # print(misses)
#     if misses[A_index] > misses[B_index]:
#         # print('m')
#         return B_index
#     elif misses[A_index] < misses[B_index]:
#         # print('m')
#         return A_index
#     if stopcount[A_index] > stopcount[B_index]:
#         # print('s')
#         return B_index
#     elif stopcount[A_index] < stopcount[B_index]:
#         # print('s')
#         return A_index
#     if distance[A_index] > distance[B_index]:
#         # print('d')
#         return B_index
#     elif distance[A_index] < distance[B_index]:
#         # print('d')
#         return A_index
#     if size[A_index] > size[B_index]:
#         # print('si')
#         return B_index
#     elif size[A_index] < size[B_index]:
#         # print('si')
#         return A_index
#     return A_index
#
#
# def compare_vectors():
#     stackvector = []
#     stackvector.extend(vectorlist)
#     print(stackvector)
#     # print(Typearray)
#     while stackvector:
#         if len(stackvector) == 2:
#             A = stackvector.pop()
#             B = stackvector.pop()
#             # print(A,B)
#             great = comp_vector(A, B)
#             # print(great)
#             greatvector = vectorlist[great]
#             # print(greatvector)
#             break
#         A = stackvector.pop()
#         B = stackvector.pop()
#         great = comp_vector(A, B)
#         greatvector = vectorlist[great]
#         stackvector.append(greatvector)
#     return greatvector
#
#
# def main():
#     with open("text.txt") as f:
#         text = f.read()
#     stopwords = ['the', 'of', 'and', 'in', 'as']
#     find_acronym(text, stopwords)
#
#
# main()

# T = int(input())
# for x in range(1, T + 1):
#     N, P = map(int, input().split())
#     S = map(int, input().split())
#     S = sorted(S, reverse = True)
#     y = hours = sum(S[0] - s for s in S[:P])
#     for i in range(1, N - P + 1):
#         hours -= (S[i - 1] - S[i]) * (P - 1)
#         hours += S[i] - S[P + i - 1]
#         if hours < y:
#             y = hours
#     print("Case #{}: {}".format(x, y), flush = True)

# T = int(input())
# for x in range(1, T + 1):
#     N = int(input())
#     S = list(map(int, input().split()))
#     print(S)
#     count = 0
#     for i in range(1, N - 1):
#         print(S[i-1],S[i],S[i+1])
#         if S[i-1]<S[i]>S[i+1]:
#             count += 1
#     print("Case #{}: {}".format(x, count), flush = True)
#
# T = int(input())
# for x in range(1, T + 1):
#
#     S = str(input())
#     stack = []
#
#     for i in range(len(S)):
#         ch = S[i]
#
#         if ch == ')':
#             temp = ''
#             while stack and stack[-1] != '(':
#                 temp = stack.pop() + temp
#             stack.pop()
#             if stack and stack[-1].isdigit():
#                 temp = temp * int(stack.pop())
#             stack.append(temp)
#             continue
#
#         stack.append(ch)
#     start = [1, 1]
#     stack = ''.join(stack)
#     for i in range(len(stack)):
#         if stack[i] == 'N':
#             start = (start[0] - 1 + 10 ** 9) % (10 ** 9), start[1]
#         elif stack[i] == 'S':
#             start = (start[0] + 1) % (10 ** 9), start[1]
#         elif stack[i] == 'E':
#             start = start[0], (start[1] + 1) % (10 ** 9)
#         elif stack[i] == 'W':
#             start = start[0], (start[1] - 1 + 10 ** 9) % (10 ** 9)
#         #print(start, stack[i])
#     print("Case #{}: {} {}".format(x, start[1], start[0]), flush=True)


T = int(input())
for x in range(1, T + 1):
    N, D = map(int, input().split())

    S = list(map(int, input().split()))
    keep = [0] * (len(S)-1)
    first_num = []
    for i in range(len(S)):
        ch = S[i]
        if i == 0:
            first_num.append(ch)
            start = 2
            while True:
                temp = ch*start
                if temp>D: break
                first_num.append(temp)
                start += 1
        else:
            d = D
            while True:
                if d%ch == 0:
                    keep[i - 1] = d
                    break
                d -= 1

    first = first_num
    ans = -1
    for i in range(len(first)):
        now = first[i]
        flag = True
        for k in keep:
            if k < now:
                flag = False
                break
        if flag:
            ans = now
        else: break

    print("Case #{}: {}".format(x, ans), flush=True)