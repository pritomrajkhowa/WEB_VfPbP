import dash, wolframalpha
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html



from pyparsing import *
import wolframalpha
appid= 'YRL93R-JLEJXTJ67Y'
appid='YRL93R-W2ATR8XGLX'
client = wolframalpha.Client(appid)
import collections


def quad_ineq_solver(inequalities):
    res = client.query(inequalities)
    solution_regions = []
    inverval_regions = []
    solution_images = []
    inverval_images = []
    for i in range(len(res['pod'])):

         if res['pod'][i]['@title']=='Solutions' or res['pod'][i]['@title']=='Solution':
           subpod_map = res['pod'][i]['subpod']
           if isinstance(subpod_map, list):
              for subpod_map_i in subpod_map:
                if 'img' in subpod_map_i.keys():
                  img_map = subpod_map_i['img']
                  check_img_set=img_map.keys()
                  if '@src' in check_img_set:
                     solution_images.append(img_map['@src'])
                  if '@alt' in check_img_set:
                     if ',' in img_map['@alt']:
                        solution=img_map['@alt'].split(',')
                        solution_regions.append(solution)
                     else:
                        solution_regions.append(img_map['@alt'])
           else:
              img_map = subpod_map['img']
              check_img_set=img_map.keys()
              if ',' in img_map['@alt']:
                  solution=img_map['@alt'].split(',')
                  solution_regions.append(solution)
              else:
                  #if '@src' in check_img_set:
                  #    solution_images.append(img_map['@src'])
                  if '@alt' in check_img_set:
                      solution_regions.append(img_map['@alt'])

         elif res['pod'][i]['@title']=='Interval notation':
           subpod_map = res['pod'][i]['subpod']
           if isinstance(subpod_map, list):
              for subpod_map_i in subpod_map:
                if 'img' in subpod_map_i.keys():
                  img_map = subpod_map_i['img']
                  check_img_set=img_map.keys()
                  if '@src' in check_img_set:
                     inverval_images.append(img_map['@src'])
                  if '@alt' in check_img_set:
                     inverval_regions.append(img_map['@alt'])
           else:
              img_map = subpod_map['img']
              check_img_set=img_map.keys()
              if '@src' in check_img_set:
                  inverval_images.append(img_map['@src'])
              if '@alt' in check_img_set:
                  inverval_regions.append(img_map['@alt'])


    return solution_regions,inverval_regions;








def simpleToken(inputExpression):
    Toknext=None
    Tokprev=None
    TokenList =[]
    # Iterate over index 
    for element in range(0, len(inputExpression)):
        if inputExpression[element]:
           if inputExpression[element].isdigit()==True or inputExpression[element].isalpha()==True or inputExpression[element]=='_':
              if Tokprev is None:
                 Tokprev = inputExpression[element]
              else:
                 Tokprev = Tokprev + inputExpression[element]
           elif inputExpression[element] in ['+','*','^','/','%','-','=','>','<','(',')']:
                if Tokprev is not None:
                   TokenList.append(Tokprev)
                   Tokprev=None
                TokenList.append(inputExpression[element])
           elif inputExpression[element]==' ':
                if Tokprev is not None:
                   TokenList.append(Tokprev)
                   Tokprev=None
                TokenList.append(inputExpression[element])
    if Tokprev is not None:
       TokenList.append(Tokprev)
    return TokenList



def replaceSpacebyMultipy(TokenList):
    TokenListUpdate = []
    for index in range(0, len(TokenList)):
        if index>0 and TokenList[index] is ' ' and index+1<len(TokenList):
           if (TokenList[index-1].isdigit()==True or TokenList[index-1].isalpha()==True or TokenList[index-1].isalnum()==True or TokenList[index-1] in ['(',')']) and (TokenList[index+1].isdigit()==True or TokenList[index+1].isalpha()==True or TokenList[index+1].isalnum()==True or TokenList[index+1] in ['(',')']):
              TokenListUpdate.append("*")
        else:
           TokenListUpdate.append(TokenList[index])
    return TokenListUpdate




def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, str):
            for sub in flatten(el):
                yield sub
        else:
            yield el



def replaceOrigin(expression,symMap):
    new_expression=[]
    for element in expression:
        if element in symMap.keys():
           new_expression.append(symMap[element])
        else:
           new_expression.append(element)
    return new_expression




expr = Forward()

double = Word(nums + ".").setParseAction(lambda t:float(t[0]))
integer = Word(nums).setParseAction(lambda t:int(t[0]))
variable = Word(alphas)
string = dblQuotedString
funccall = Group(variable + "(" + Group(Optional(delimitedList(expr))) + ")")
array_func = Group(funccall + "[" + Group(delimitedList(expr, "][")) + "]")
array_var = Group(variable + "[" + Group(delimitedList(expr, "][")) + "]")

operand = double | string | array_func | funccall | array_var | variable

expop = Literal('**')
signop = oneOf('+ -')
multop = oneOf('* /  ')
plusop = oneOf('+ -')

expr << operatorPrecedence( operand,
[("^", 2, opAssoc.RIGHT),
(signop, 1, opAssoc.RIGHT),
(multop, 2, opAssoc.LEFT),
(plusop, 2, opAssoc.LEFT),]
)

def expessConstruct(expression):
    result = expr.parseString(expression)
    return list(flatten(result));


def mapingTable(listofSymbol,Var,alter_map):
    new_equation=[]
    count = 0
    list_of_symbol = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','Y','Z']
    for element in listofSymbol:
        if element==Var:

           new_equation.append('X')
           alter_map[element]='X'

        elif element not in ['+','*','^','/','%','-','=','>','<','(',')'] and element!=Var and element.isdigit()==False:

           if element in alter_map.keys():

              new_equation.append(alter_map[element])

           else:

              alter_map[element]=list_of_symbol[count]
              new_equation.append(list_of_symbol[count])
              count=count+1
        else:
              new_equation.append(element)
    return new_equation


def constructEqu(TokenList):
    equation=''
    for index in range(0, len(TokenList)):
        equation+= TokenList[index]
    return equation




def findBound(Var, assumption, equation1, equation2):

    alter_map={}

    outPutStr=''

    if Var is None or Var.strip()=='':
       return "\nPlease Enter Variable For Which You Want to Solve Equations\n"

    #Construct list of Symbol
    if assumption is not None and assumption.strip()!='':
       assumptionSymbol = simpleToken(assumption)
    else:
       assumptionSymbol = None

    if equation1 is not None and equation1.strip()!='':
       equation1Symbol = simpleToken(equation1)
    else:
       equation1Symbol = None

    if equation2 is not None and equation2.strip()!='':
       equation2Symbol = simpleToken(equation2)
    else:
       equation2Symbol = None


    #Construct list of Symbol
    if assumptionSymbol is not None:
       strAssumption=constructEqu(mapingTable(assumptionSymbol,Var,alter_map))
    else:
       strAssumption=None

    if equation1Symbol is not None:
       strEquation1=constructEqu(mapingTable(equation1Symbol,Var,alter_map))
    else:
       strEquation1=None

    if equation2Symbol is not None:
       strEquation2=constructEqu(mapingTable(equation2Symbol,Var,alter_map))
    else:
       strEquation2=None

    if equation1Symbol is None and equation2Symbol is None:

       return "\nPlease Enter Equations\n"

    solution_regions=[]
    inverval_regions=[]

    try:
       EquToSolve=''
       if strAssumption is not None:
          EquToSolve+=strAssumption

       if strEquation1 is not None and EquToSolve!='':
          EquToSolve+=','+strEquation1
       elif EquToSolve=='':
          EquToSolve+=strEquation1

       if strEquation2 is not None and EquToSolve!='':
          EquToSolve+=','+strEquation2
       elif EquToSolve=='':
          EquToSolve+=strEquation2

       solution_regions,inverval_regions = quad_ineq_solver(EquToSolve)

    except:
       pass

    #alter_map2 = {y:x for x,y in alter_map.iteritems()}

    alter_map2 = dict((y,x) for x,y in alter_map.items())

    #print("Input Assumption : "+str(assumption))
    outPutStr+="Input Assumption : "+str(assumption)+'\n\n'
    #print("Input Equation 1 : "+str(equation1))
    outPutStr+="Input Equation 1 : "+str(equation1)+'\n\n'
    #print("Input Equation 2 : "+str(equation2))
    outPutStr+="Input Equation 2 : "+str(equation2)+'\n\n'
    #print("Solving Equations For Variable : "+str(Var))
    outPutStr+="Solving Equations For Variable : "+str(Var)+'\n\n'

    if len(solution_regions)>0:
       outPutStr+='Solution(s):\n\n'
       for solution_region in solution_regions:
          #if len(solution_region)>1:
          if isinstance(solution_region, list):
              condSymbol = simpleToken(solution_region[0])
              solnSymbol = simpleToken(solution_region[1])
              condition = replaceOrigin(condSymbol,alter_map2)
              soln = replaceOrigin(solnSymbol,alter_map2)
              outPutStr+=constructEqu(condition)+' -> '+constructEqu(soln)+'\n'
              #print(constructEqu(condition)+' -> '+constructEqu(soln))
          else:
              solnSymbol = simpleToken(solution_region)
              soln = replaceOrigin(solnSymbol,alter_map2)
              outPutStr+=constructEqu(soln)+"\n"
              #print(constructEqu(soln))+'<br>\n'
       outPutStr+='\nInterval(s):\n\n'
       #print('Intervals')
       for inverval_region in inverval_regions:
           inverval_value = replaceOrigin(inverval_region,alter_map2)
           outPutStr+=constructEqu(inverval_value)+'\n'
           #print(constructEqu(inverval_value))


    else:
          outPutStr+='System is unable to find Solution\n\n'
          #print('System is unable to find Solution')
    return outPutStr





if __name__ == '__main__':
        #'Please Enter Variable For Which You Want to Solve Equations.'
        #'Please Enter Pre-Condition.'
        #'Please Enter the First Equation.'
        #'Please Enter the Second Equation.'
	findBound(equat1, equat2, equat3, equat4)
