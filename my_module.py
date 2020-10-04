from mora.core import Program, core
from mora.utils import Update
from diofant import sympify, Rational




def myCore_function(input_list, goal):

    update_map={}

    init_map={}

    var_list =[]

    closed_form_soln = {}

    
    for var in input_list[0].keys():

        var_list.append(sympify(var))

    
    for item in input_list[0]:

        list_item = input_list[0][item]

        var=sympify(item)

        update_string = None

        for x in list_item:

            if update_string is None:

               update_string=x

            else:

               update_string+=";"+x

        update = Update(var, update_string)

        update_map[var] = update


    for item in input_list[1]:

        var = sympify(item)

        init_val_string = input_list[1][item]

        init_map[var]=  Update(var, init_val_string) 

    program = Program()

    program.variables = var_list

    program.initial_values = init_map 

    program.updates = update_map

    invariants = core(program, goal)

    for x in input_list[-1]:

       for y in range(1,int(goal)+1):

           key = x+'^'+str(y)

           new_closed_form = str(sympify(invariants[key]))

           new_closed_form = str(sympify(new_closed_form).subs({sympify("n"):sympify(input_list[-2][x])}))

           if y>1:

              closed_form_soln['power('+input_list[-1][x]+","+str(y)+")"] = new_closed_form

           else:

              closed_form_soln[input_list[-1][x]] = new_closed_form


    return closed_form_soln




#myCore_function([{'x3': ['(x3+n3) @ 1/2', 'x3 @ 1/2'], 'y3': ['(y3+1) @ 1'], 'n3': ['(n3+1) @ 1/2', 'n3 @ 1/2']}, {'x3': '0', 'y3': '0', 'n3': '0'}, {'_n1': '_N1'}, {'x3': '_n1', 'y3': '_n1', 'n3': '_n1'}, {'x3': 'x3(_n1)', 'y3': 'y3(_n1)', 'n3': 'n3(_n1)'}],3)





