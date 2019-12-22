def get_freq(infolist):
    infoList = sum(infolist, [])
    dict = {}
    for key in infoList:
        dict[key] = dict.get(key, 0) + 1
    return dict
