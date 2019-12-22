def never_appear(list1, list2):
    dic = set(sum(list2, []))
    # print(dic)
    output = []
    for i, p in enumerate(list1):
        # print(p)
        if p not in dic:
            # print("Out")
            # output.append(p)
            output.append(i + 6)
        # else:
        #     print('In')
    return output
