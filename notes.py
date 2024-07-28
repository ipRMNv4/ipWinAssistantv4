import datetime

time = datetime.datetime.now()
formatted_time = time.strftime("%d/%m/%Y %H:%M:%S")

def notes():
    while True:
        i = input("Type anything to save....\n")
        if i.lower() == "exit":
            return
        with open(r"PATH_TO_FILE","a") as f:
            f.write(f"{formatted_time}:\n{i} \n")

notes()
