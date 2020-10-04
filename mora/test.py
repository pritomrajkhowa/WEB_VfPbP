from mora.core import Program, core
from mora.utils import Update
from diofant import sympify, Rational

print(repr(sympify("x*y+y")))

var_list=[]
var_list.append(sympify("x"))
var_list.append(sympify("y"))
var_list.append(sympify("n"))
print(var_list)


init_map ={}
update_map ={}

#var1 = sympify("y")

#update_string1 = []

#update_string1.append((sympify("y+1"),sympify("1")))

#update1 = Update(var1, update_string1)

var1="y"

init_val_string1 = "0"

update_string1 = "y + 1 @ 1"

init_val1 = Update(var1, init_val_string1)

update1 = Update(var1, update_string1)

init_map[var1] = init_val1

update_map[var1] = update1



#print(update1)

#var2 = sympify("n")

#update_string2 = []

#update_string2.append((sympify("n+1"),sympify("1/2")))
#update_string2.append((sympify("n"),sympify("1/2")))


#update2 = Update(var2, update_string2)

var2 = "n"

init_val_string2 = "0"

update_string2 = "n + 1 @ 1/2; n @ 1/2"

init_val2 = Update(var2, init_val_string2)

update2 = Update(var2, update_string2)

init_map[var2] = init_val2

update_map[var2] = update2

#print(update2)


#var3 = sympify("x")

#update_string3 = []

#update_string3.append((sympify("x+n"),sympify("1/2")))
#update_string3.append((sympify("x"),sympify("1/2")))


#update3 = Update(var3, update_string3)

var3 = "x"

init_val_string3 = "0"

update_string3 = "x + n @ 1/2; x @ 1/2"

init_val3 = Update(var3, init_val_string3)

update3 = Update(var3, update_string3)

init_map[var3] = init_val3

update_map[var3] = update3

#print(update3)

print(update_map)

print(init_map)

program = Program()

program.variables = var_list

program.initial_values = update_map

program.updates = init_map

core(program, 3)


