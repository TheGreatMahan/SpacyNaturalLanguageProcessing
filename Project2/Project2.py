import spacy
from locale import atof, setlocale, LC_NUMERIC

def numToMoney(num):
    return "${:,.0f}".format(num)

def companyArrToString(arr):
    myString = ""
    size = len(arr)
    if(size == 0):
        myString = ""

    elif(size == 1):
        myString = arr[0]
        
    elif(size == 2):
        myString = arr[0] + " and " + arr[1]

    else:
        counter = 0
        while(counter < size - 2):
            myString += arr[counter]+", "
            counter += 1
        
        myString += arr[size - 2] + " and " + arr[size - 1]

    return myString

def specificAmountForEachCompanyToString(companies, amounts):
    size = len(companies)
    myString = ""
    if(size <= 1):
        myString = ""

    elif(size > 1):
        counter = 0
        while(counter < size - 1):
            myString += numToMoney(amounts[counter]) + " to " + companies[counter]+", "
            counter += 1

        myString += "and " + numToMoney(amounts[counter]) + " to " + companies[counter]

    return myString

setlocale(LC_NUMERIC, 'English_Canada.1252')
nlp = spacy.load('en_core_web_sm')
f = open('EmailLog.txt', mode='r', encoding='utf-8')
data = f.read()

allEmails = data.split("<<End>>")
sumTotal= 0.0

# save spaCy data to a text file
of = open('pos.txt', mode='wt', encoding='utf-8')


for email in allEmails:
    lines = email.split('\n')
    nlpObj=nlp(email)
    email = ''
    amountArray = []
    companyArray = [ent.text for ent in nlpObj.ents if ent.label_ == 'ORG']
    sumNumber = 0.0
    for token in nlpObj:
        if(token.text in companyArray):
            if(token.dep_ == 'npadvmod'):
                companyArray.remove(token.text)
        if(token.pos_ != 'SPACE'):
            of.write(token.text + ", " + token.pos_ + ", " + token.tag_ + ", " + token.dep_ + ", " + str(spacy.explain(token.dep_)) + '\n')
        if(token.like_email):
            email = token.text
        elif token.tag_ == '$':
            phrase = ''
            i = token.i+1
            while nlpObj[i].tag_ == 'CD':
                if(nlpObj[i].text == 'million'):
                    phrase += ',000,000'
                if(nlpObj[i].text == 'thousand'):
                    phrase += ',000'
                elif(nlpObj[i].text == 'hundred'):
                    phrase += '00'
                else:
                    phrase += nlpObj[i].text
                i += 1
            amountArray.append(atof(phrase))
            sumNumber += atof(phrase)

    if(email != ''):
        print(email + " : "  + numToMoney(sumNumber) + " to " + companyArrToString(companyArray) + ". " + specificAmountForEachCompanyToString(companyArray, amountArray) + "\n")

    sumTotal += sumNumber
print("Total Requests: " + "${:,.2f}".format(sumTotal) + "\n")
    
f.close()
of.close()
