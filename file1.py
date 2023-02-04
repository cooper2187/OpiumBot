# def num():
#     a = input('Введите число: ')
#     b = list(a)
#     a = len(b)
#     print(f"Before: {''.join(b)}")
#     x = []
#     xn = []
#     xnx = []
#     u = 1
#     y = 4
#     g = 1


#     if a <= 3:
#         print(''.join(b))


#     elif a %3 == 0:
#         x.append(b[0] + b[1] + b[2])
#         i = 3
#         while i < a:
#             x.append(b[i])
#             i = i + 1
#         if len(b) >= 6:
#             xn.append(x[0])
#             gg = len(b)/3
#             while g < gg:
#                 xn.append(x[u:y])
#                 u = u + 3
#                 y = y + 3
#                 g = g + 1
#             for ab in xn:
#                 xnx.append(''.join(ab))
#             print(f"After: {' '.join(xnx)}")
#         else:
#             print(x[1:])


#     elif a %3 >=2:
#         x.append(b[0] + b[1])
#         i = 2
#         while i < a:
#             x.append(b[i])
#             i = i + 1
#         if len(b) >= 5:
#             xn.append(x[0])
#             gg = len(b)/3
#             while g < gg:
#                 xn.append(x[u:y])
#                 u = u + 3
#                 y = y + 3
#                 g = g + 1
#             for ab in xn:
#                 xnx.append(''.join(ab))
#             print(f"After: {' '.join(xnx)}")
#         else:
#             print(x[1:])


#     else:
#         x.append(b[0])
#         i = 1
#         while i < a:
#             x.append(b[i])
#             i = i + 1
#         if len(b) >= 4:
#             xn.append(x[0])
#             gg = len(b)/3
#             while g < gg:
#                 xn.append(x[u:y])
#                 u = u + 3
#                 y = y + 3
#                 g = g + 1
#             for ab in xn:
#                 xnx.append(''.join(ab))
#             print(f"After: {' '.join(xnx)}")
#         else:
#             print(x[1:])


# num()

def triada_num(x: int):
    return f'{x:,}'.replace(',', ' ')