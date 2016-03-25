def search_text(q):
    content = read_input_filelines("1Q84Lines.txt")
    match = []
    for line in content:
        if q in line:
            match.append(line)
    return match

def read_input_filelines(path):
    f = open(path)
    content = f.readlines()
    f.close()
    return content
