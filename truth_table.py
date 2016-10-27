from Tkinter import Tk
import copy

ops=['(','~','*','x','+',')']

varCount=input('Number of Variables: ')
resultantVar='F'

validVars=[]
for place in range(0,varCount):
	validVars.append(str(unichr(65+place)))

if resultantVar in validVars:
	resultantVar='Result'

logEq=raw_input('Logic Equation: ')

def pre_process(equation):
	nxt=0
	while nxt < len(equation)-1:
		pair = equation[nxt:nxt+2]
		if pair[0] in validVars and pair[1] in validVars:
			equation=equation[:nxt+1]+'*'+equation[nxt+1:]
		elif pair[0] in validVars and pair[1]==ops[1]:
			equation=equation[:nxt+1]+'*'+equation[nxt+1:]
		elif pair[0]==ops[5] and pair[1]==ops[1]:
			equation=equation[:nxt+1]+'*'+equation[nxt+1:]
		elif pair[0]==ops[5] and pair[1] in validVars:
			equation=equation[:nxt+1]+'*'+equation[nxt+1:]
		elif pair[0] in validVars and pair[1]==ops[0]:
			equation=equation[:nxt+1]+'*'+equation[nxt+1:]
		elif pair[0]==ops[5] and pair[1]==ops[0]:
			equation=equation[:nxt+1]+'*'+equation[nxt+1:]
		nxt+=1
	return equation

def create_opArray(equation):
	terms=[]
	opInd=0
	while opInd < len(equation):
		hi=-1
		try:
			hi=ops.index(equation[opInd:opInd+1])
		except ValueError:
			pass
		if hi>=0:
			if hi==0:
				nextTerm=extract_term(equation[opInd+1:],ops[hi])
				opInd+=2+len(nextTerm)
				if len(nextTerm)>1:
					nextTerm = create_opArray(nextTerm)
				terms.append(nextTerm)
			elif hi==1:
				nextTerm=extract_term(equation[opInd+1:],ops[hi])
				opInd+=1+len(nextTerm)
				if len(nextTerm)>1:
					nextTerm = create_opArray(nextTerm)
				terms.append([ops[hi], nextTerm])
			elif hi==2:
				nextTerm=extract_term(equation[opInd+1:],ops[hi])
				opInd+=1+len(nextTerm)
				if len(nextTerm)>1:
					nextTerm = create_opArray(nextTerm)
				prevTerm=terms.pop()
				terms.append([ops[hi],prevTerm, nextTerm])
			elif hi==3:
				nextTerm=extract_term(equation[opInd+1:],ops[hi])
				opInd+=1+len(nextTerm)
				if len(nextTerm)>1:
					nextTerm = create_opArray(nextTerm)
				prevTerm=terms.pop()
				terms.append([ops[hi],prevTerm, nextTerm])
			elif hi==4:
				nextTerm=extract_term(equation[opInd+1:],ops[hi])
				opInd+=1+len(nextTerm)
				if len(nextTerm)>1:
					nextTerm = create_opArray(nextTerm)
				prevTerm=terms.pop()
				terms.append([ops[hi],prevTerm, nextTerm])
			else:
				opInd+=1
		else:
			nextTerm = extract_term(equation[opInd:],-1)
			opInd+=len(nextTerm)
			if len(nextTerm)>1:
				nextTerm=create_opArray(nextTerm)
			terms.append(nextTerm)
	if len(terms)==1:
		terms=terms[0]
	return terms

def extract_term(equation, operation):
	if operation==ops[0]:
		operation=')'
	if operation==-1:
		operation='('
	term = ""
	nestPar=0
	for nxt in equation:
		if nxt == ops[0]:
			nestPar+=1
		if nestPar==0:
			if nxt in ops:
				if nxt==ops[1]:
					if ops.index(nxt)>ops.index(operation):
						break
				else:
					if ops.index(nxt)>=ops.index(operation):
						break
		if nxt == ops[5]:
			nestPar-=1
		term+=nxt
	return term

def evaluate_table(baseArray, validVarVals):
	if type(baseArray) is str:
		return validVarVals[validVars.index(baseArray)]
	hi = ops.index(baseArray[0])
	val=0
	if hi==1:
		val = not evaluate_table(baseArray[1],validVarVals)
	elif hi==2:
		val = evaluate_table(baseArray[1],validVarVals) and evaluate_table(baseArray[2],validVarVals)
	elif hi==3:
		val = evaluate_table(baseArray[1],validVarVals) != evaluate_table(baseArray[2],validVarVals)
	elif hi==4:
		val = evaluate_table(baseArray[1],validVarVals) or evaluate_table(baseArray[2],validVarVals)
	val=int(val)
	return val
	#while opInd < len(baseArray):

def generate_array(numVars):
	numRows = 2**numVars
	resultArray=[]
	for i in range(0,numRows):
		resRow=[]
		for j in range(0,numVars):
			e=2**(numVars-j)
			if (i)%e>=e/2:
				resRow.append(1)
			else:
				resRow.append(0)
		resultArray.append(resRow)
	return resultArray

def display_result(opArray):
	display=copy.deepcopy(resultArray)
	fline=copy.deepcopy(results)
	fline.insert(0,copy.deepcopy(resultantVar))
	display.insert(0,copy.deepcopy(validVars))
	for line in range(0,len(display)):
		display[line].append('|')
		display[line].append(fline[line])
		display[line].insert(0,'|')
		if line==0:
			ind="#"
		else:
			ind=str(line-1)
		display[line].insert(0,ind)
	gapLine=[]
	for ind in range(0,varCount+4):
		if ind==1 or ind==varCount+2:
			gapLine.append("+")
		else:
			gapLine.append("-")
	display.insert(1,gapLine)

	displaystr=""
	count=0
	for line in display:
		for let in line:
			displaystr=displaystr+" "+str(let)
		displaystr=displaystr+"\n"
		count+=1
	print displaystr
	raw_input("Press Enter to Continue...")

opArray=create_opArray(pre_process(logEq))

resultArray=generate_array(varCount)
results=[]
for inputs in resultArray:
	fin = evaluate_table(opArray, inputs)
	results.append(fin)

copyPasta="\\begin\{center}\n\\begin\{tabular}\{c c c c | c}\n"
for val in validVars:
	copyPasta=copyPasta+str(val)+" & "
copyPasta=copyPasta+str(resultantVar)+"\\\\\n"
for line in range(0,len(resultArray)):
	if line%4==0:
		copyPasta=copyPasta+"\\hline\n"
	for val in resultArray[line]:
		copyPasta=copyPasta+str(val)+" & "
	copyPasta=copyPasta+str(results[line])+"\\\\\n"
copyPasta=copyPasta+"\\end\{tabular}\n\\end\{center}\n"

r=Tk()
r.withdraw()
r.clipboard_clear()
r.clipboard_append(copyPasta)

if raw_input("Display Table? (Y/N): ").lower()=="y":
	display_result(opArray)

r.destroy()

