s = {1, 2}
l = [1, 2, 3, 1, 2, 3]

def main():
    for item in l:
        methods = {
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PUT" # this is a duplicate 
        }
        if item in methods:
            print(item)
s2 = {1, 2, 3, 1} # another duplicate.