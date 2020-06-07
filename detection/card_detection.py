from os import path


if __name__ == '__main__':
    while True:
        inp = input("Enter image name or exit : ")
        if inp == "exit":
            print("Bye!")
            break
        if not path.exists(inp):
            print("The specified image does not exist!")
            continue
        print("We will do some image processing here soon!")
