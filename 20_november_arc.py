#loging files - dəqiq gösrərər və bank sistemlərində istdifədə olunur
#used for terminals systems (warning line- there no enough currency)
#import log 
import json
class deposite:
    def __init__(self,income,outcome,user):
        self.income=income
        self.outcome=outcome
        self.user=user
        return f"hello dear{user} you have {(income-outcome)}"
my_json={
  
    "u1":  
    {
      "username": "Alice",
      "income": 600.00,
      "outcome": 200.00
    },
    "u2":
    {
      "username": "Bob",
      "income": 1200.00,
      "outcome": 450.00
    },
    "u3":
    {
      "username": "Charlie",
      "income": 800.00,
      "outcome": 350.00
    }
  
} 
   
my_json=json.loads(my_json)
values=my_json.values()
for i in values:
    a=values[i]["income"]
    b=values[i]["outcome"]
    u=values[i]["username"]
    p=deposite(a,b,u)
c=int(a)-int(b)   
if c>0:
    print(p)
else:
    print("there no enough deposite")    






