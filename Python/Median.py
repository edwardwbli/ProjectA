Choice_list = ["sex", "love", "money"]
Your_choice = raw_input("Your choice: ")
for choice in Choice_list:
    if choice == Your_choice:
        print choice 
else:
    print "No choice"

