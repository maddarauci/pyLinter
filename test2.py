s = {1, 2} # Unused global 
l = [1, 2, 3, 1, 2, 3]


def main():
    var = 5 # Unused local 
    methods = {
        "GET",
        "PUT",
        "POST",
        "DELETE",
        "PUT", # duplicate 
    }

    if item in methods:
        print(item)

s2 = {1, 2, 3, 3} # Unused, and has a duplicate 
var = 7 
print(var)