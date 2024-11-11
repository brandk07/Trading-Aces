
STOCKNAMES = ['QSYN','NRLX','CMDX','PRBM','GFRG','ASCS','BGTX','MCAN','VITL']
positiveEvents = {}
negativeEvents = {}
with open('Assets\companyNews.txt','r') as f:
    lines = f.readlines()
    lines = [l.replace("\n",'') for l in lines]

    for stock in STOCKNAMES:
        index = lines.index(stock)
        positiveEvents[stock] = lines[index+1:index+6]
        negativeEvents[stock] = lines[index+7:index+12]

print(positiveEvents["VITL"])
print(negativeEvents["VITL"])
