import time

print("   .--.  .---. .-.  .-.  .--.  .-..-. ") 
print("  / {} \ } }}_}}  \/  { / {} \ \ {} / ") 
print(" /  /\  \| } \ | {  } |/  /\  \/ {} \ ") 
print(" `-'  `-'`-'-' `-'  `-'`-'  `-'`-'`-'      https://github.com/Pyshios ")

print("Armax is a Tool disgned manage some telegram group functions automating it with Telethon")

print("1) Extract all members from a group")
print("2) Add all group members Extracted ")
print("3) Send automatic messages")

a = input("Input your choice:")
b = int(a)
try:
    if b == 1 :
        print("Opening extractor")
        time.sleep(3)
        exec(open("extrac.py").read())
    elif b == 2:
        print("Opening automatic add ")
        time.sleep(3)
        exec(open("addall.py").read())
    elif b == 3:
        print("Opening automatic message sender ")
        time.sleep(3)
        exec(open("messageall.py").read())
except:
    print("not a valid choice")
    
    
    

