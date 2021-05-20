import re

exR=r'&\*(\w*|\d*|(.)*)%*&'
# &* - *&
questionR = r'\$%(\w*|\d*|(.)*)\^%'
# $% -- %$

answerR = r'\^%(\w*|\d*|(.)*)%\$'
#^% - %$


keyR = r'\#@(\w*|\d*|(.)*)@\#'
def QA(data):
    question = re.search(questionR,data).group(0)
    answer = re.search(answerR,data).group()
    return [question[2:-2],answer[2:-2]]


    
def EX(data):
    return re.search(exR,data).group(0)[2:-2]

def KEY(data):
    return re.search(keyR,data).group(0)[2:-2]

def TIME(data):
    time = re.search("\d{2}:\d{2}",data)[0]
    return ''.join(time.split(':')[::-1])