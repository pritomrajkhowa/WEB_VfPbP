import sys
import os
currentdirectory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentdirectory+"/packages/setuptools/")
currentdirectory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentdirectory+"/packages/z3/python/")
from z3 import *
init(currentdirectory+"/packages/z3")
set_param(proof=True)

try:
	_p1=Int('_p1')
	_p2=Int('_p2')
	_n=Int('_n')
	_bool=Int('_bool')
	arraySort = DeclareSort('arraySort')
	_f=Function('_f',IntSort(),IntSort())
	_ToReal=Function('_ToReal',RealSort(),IntSort())
	_ToInt=Function('_ToInt',IntSort(),RealSort())
	M1=Int('M1')
	M=Int('M')
	n1=Real('n1')
	_N1=Const('_N1',IntSort())
	x1=Real('x1')
	y1=Real('y1')
	_n1=Int('_n1')
	main=Int('main')
	power=Function('power',RealSort(),RealSort(),RealSort())
	_s=Solver()
	_s.add(ForAll([_p1],Implies(_p1>=0, power(0,_p1)==0)))
	_s.add(ForAll([_p1,_p2],Implies(power(_p2,_p1)==0,_p2==0)))
	_s.add(ForAll([_p1],Implies(_p1>0, power(_p1,0)==1)))
	_s.add(ForAll([_p1,_p2],Implies(power(_p1,_p2)==1,Or(_p1==1,_p2==0))))
	_s.add(ForAll([_p1,_p2],Implies(And(_p1>0,_p2>=0), power(_p1,_p2+1)==power(_p1,_p2)*_p1)))
	_s.add(ForAll([_n],Implies(_n>=0, _f(_n)==_n)))
	_s.set("timeout",50000)
	_s.add(M == M)
	_s.add(power(n1,3) == ((((power(_N1,2))*(_N1 + 3)))/(8)))
	_s.add(power(x1,3) == ((((_N1)*(((((((((((power(_N1,5))+(((11)*(power(_N1,4))))))+(((39)*(power(_N1,3))))))+(((49)*(power(_N1,2))))))+(24*_N1)))+(4)))))/(512)))
	_s.add(power(y1,3) == _N1)
	_s.add(_N1 >= M)
	_s.add(ForAll([_n1],Implies(And(_n1 < _N1,_n1>=0),_f(_n1) < M)))
	_s.add(Or(_N1==0,_N1 - 1 < M))
	_s.add(Not(((((((_N1)*(((((((((((power(_N1,5))+(((11)*(power(_N1,4))))))+(((39)*(power(_N1,3))))))+(((49)*(power(_N1,2))))))+(24*_N1)))+(4)))))/(512)))>(((1)/(2))))))

except Exception as e:
	print( "Error(Z3Query)")
	file = open('j2llogs.logs', 'a')

	file.write(str(e))

	file.close()

	sys.exit(1)

try:
	result=_s.check()
	if sat==result:
		print( "Counter Example")
		print (_s.model())
	elif unsat==result:
		result
		try:
			if os.path.isfile('j2llogs.logs'):
				file = open('j2llogs.logs', 'a')
				file.write("\n**************\nProof Details\n**************\n"+str(_s.proof().children())+"\n")
				file.close()
			else:
				file = open('j2llogs.logs', 'w')
				file.write("\n**************\nProof Details\n**************\n"+str(_s.proof().children())+"\n")
				file.close()
		except Exception as e:
			file = open('j2llogs.logs', 'a')
			file.write("\n**************\nProof Details\n**************\n"+"Error"+"\n")
			file.close()
		print( "Successfully Proved")
	else:
		print( "Failed To Prove")
except Exception as e:
	print ("Error(Z3Query)")
	file = open('j2llogs.logs', 'a')

	file.write(str(e))

	file.close()
