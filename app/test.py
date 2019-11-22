import re

def text_length(text):
    pattern ='[ \n\r]'
    
    return len(re.sub(pattern, "", text))

text = "Ещё при жизни Пушкина сложилась его репутация величайшего национального русского поэта[3][4]. Пушкин рассматривается как основоположник современного русского литературного языка"
print(text_length(text))