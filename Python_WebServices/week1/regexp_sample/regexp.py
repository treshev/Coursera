def calculate(data, findall):
    matches = findall(r"([abc])([+-]?)=([abc]?)([+-]?\d*)")
    # matches = findall(r"([abc])([+-]{0,1})=([abc]{0,1})([+-]{0,1}\d*)") -- submited
    for v1, s, v2, n in matches:
        if s == '+':
            data[v1] = data[v1] + data.get(v2, 0) + int(n or 0)
        elif s == '-':
            data[v1] = data[v1] - (data.get(v2, 0) + int(n or 0))
        else:
            data[v1] = data.get(v2, 0) + int(n or 0)
    return data
