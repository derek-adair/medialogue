def querydict_to_dict(query_dict):
    # request.POST only returns the first value in a list, this grabs it all
    # Lovingly stolen from: https://tinyurl.com/h6my82s6
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data
