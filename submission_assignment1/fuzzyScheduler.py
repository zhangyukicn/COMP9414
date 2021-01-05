import cspConsistency
import cspProblem
import searchGeneric
import sys



'''
Domin:
Days = ['mon','tue','wed','thu','fri']
time = ['9am','10am','11am','12am','1pm','2pm','3pm','4pm','5pm']

variable:
A number of task
[task，<name>, <duration>]

constraint：
binary constraints
hard domin conmstraints
soft deadline constraints

cost = 
h(S) =
'''


class Extend_CSP(cspProblem.CSP):
    def __init__(self,domains,constraints,soft_constraints,cost):
        super().__init__(domains,constraints)

        #soft_constraints
        self.soft_constraints = soft_constraints

        #cost
        self.cost = cost



class Search_with_AC_from_Cost_CSP(cspConsistency.Search_with_AC_from_CSP):

    def __init__(self,csp):
        super().__init__(csp)
        self.cost = []
        self.soft_cons = csp.soft_constraints
        #print(self.soft_cons)

        self.soft_cost = csp.cost
        #print(self.soft_cost) #10

    def heuristic(self,node):
        #print(node)
        add_sum = 0

        for sub_node in node:
            #print(sub_node)
            if sub_node in self.soft_cons:
                #print(node[sub_node])
                temp_cost =[]
                min_temp_cost = 0
                #print(self.soft_cons[sub_node])

                for i in node[sub_node]:
                    if i[1] <= self.soft_cons[sub_node]:
                        temp_cost.append(0)
                    elif i[1] > self.soft_cons[sub_node]:
                        mini_cost =(int(i[1])//10 - int(self.soft_cons[sub_node])//10) *24 + (int(i[1])%10 -int(self.soft_cons[sub_node])%10)
                        #print(mini_cost)
                        delay = int(self.soft_cost[sub_node]) * mini_cost
                        #print(delay)
                        temp_cost.append(delay)
                    min_temp_cost = min(temp_cost)
                add_sum += min_temp_cost
                #print(f'min_temp_cost: {min_temp_cost}')
        #print(add_sum)
        #print(delay)
        return add_sum







class GreedySearcher(searchGeneric.AStarSearcher):

    max_display_level =0

    def add_to_frontier(self,path):
        """add path to the frontier with the appropriate cost"""
        value = self.problem.heuristic(path.end())
        self.frontier.add(path, value)


#0,begin,
#1.end
def before_function(task1,task2):
    return task1[1] <= task2[0]


def same_day_function(task1,task2):
    return task1[0]//10 == task2[0]//10


def after_function(task1,task2):
    return task1[0] >= task2[1]


def starts_at_function(task1,task2):
    return task1[0] == task2[1]


def ne_(day):
    def day_(x):
        return day == (int(x[0])//10)
    return day_

def ne_time(time):
    def time_(x):
        return time == (int(x[0])%10)
    return time_

def start_before_d_t(daytime):
    def s_before_d_t_(x):
        return int(x[0]) <= daytime
    return s_before_d_t_

def start_after_d_t(daytime):
    def s_after_d_t_(x):
        return int(x[0]) >= daytime
    return s_after_d_t_

def ends_before_d_t(daytime):
    def end_before_d_t_(x):
        return int(x[1]) <= daytime
    return end_before_d_t_

def ends_after_d_t(daytime):
    def end_after_d_t_(x):
        return int(x[1]) >= daytime
    return end_after_d_t_

def start_before_t(time):
    #print(time)
    def s_before_t_(x):
        return (int(x[0])%10) <= time
    return s_before_t_

def start_after_t(time):
    def s_after_t_(x):
        return (int(x[0])%10) >= time
    return s_after_t_

def ends_before_t(time):
    #print(time)
    def end_before_t_(x):
        return (int(x[1])%10) <= time
    return end_before_t_

def ends_after_t(time):
    def end_after_t(x):
        return (int(x[1])%10) >= time
    return end_after_t

def starts_in(time1,time2):
    def starts_in_t1_t2(x):
        return time1 <= int(x[0]) <= time2
    return starts_in_t1_t2

def ends_in(time1,time2):
    def ends_in_t1_t2(x):
        return time1 <= int(x[1]) <= time2
    return ends_in_t1_t2



if __name__== '__main__':
    Text = sys.argv[1]
    #Text = 'input1.txt'
    file = open(Text,'r')

    orignal_variable = []
    variable =[]
    constraint = []
    domain =[]
    duration_time =[]
    task_duration ={}
    task_domain = {}
    binary_constrain =[]
    soft_constraints =[]
    hard_domain_constrain=[]
    soft_deadline_constrain =[]
    soft_domain = {}
    soft_cost = {}

    week_number ={'mon':10,'tue':20,'wed':30,'thu':40,'fri':50}
    day_number ={'9am':1,'10am':2,'11am':3,'12pm':4,'1pm':5,'2pm':6,'3pm':7,'4pm':8,'5pm':9,}
    final_week_number ={10:'mon',20:'tue',30:'wed',40:'thu',50:'fri'}
    final_day_number ={1:'9am',2:"10am",3:"11am",4:'12pm',5:'1pm',6:'2pm',7:'3pm',8:'4pm',9:'5pm'}

    for line in file:
        if line.startswith("task,"):
            line = line.replace(' ',',')
            orignal_variable.append(line[len("task,")+1:].strip())
            #print(line)
        if line.startswith("constraint,"):
            line = line.replace(' ',',')
            constraint.append(line[len("constraint,")+1:].strip())
            #print(line)
        if line.startswith("domain,"):
            line = line.strip()
            line = line.replace(',', '')
            line = line.split(' ')
            if len(line) == 6 and line[5] not in (week_number and day_number):
                soft_deadline_constrain.append(line)
            else:
                hard_domain_constrain.append(line)

    #print(soft_deadline_constrain)
#split line in variale and spilt in task_duration_dict
    #print(orignal_variable)
    for i in range(0,len(orignal_variable)):
        for j in range(0,len(orignal_variable[i])):
            if orignal_variable[i][j]==',':
                variable.append(orignal_variable[i][:j])
                duration_time.append(orignal_variable[i][j+1:])
                task_duration[orignal_variable[i][:j]]=int(orignal_variable[i][j+1:])
    #print("task:",variable)
    #print("duration_time:",duration_time)
    #print('task_duration:',task_duration)


#add the domain:
    for j in week_number.values():
        for i in day_number.values():
            domain.append(j+i)
    #print(domain)


#compare and judge the duration with domain:
    for key in task_duration.keys():
        temp_time= set()
        for time in domain:
            if time % 10 + int(task_duration[key]) <=9:
                temp_time.add(time)
        task_domain[key]=sorted(set((x,x+task_duration[key]) for x in temp_time))
    #print(task_domain)



#constrain
#binary constrains
    #print(constraint)
    for i in constraint:
        if 'before' in i:
            i =i.replace('before','')
            i =i.replace(',,',',')
            #print(i)
            befer_variable_set =[]
            for j in i:
                if j==',':
                    befer_variable_set.append(i[:i.index(j)])
                    befer_variable_set.append(i[i.index(j)+1:])

            befer_variable_set =tuple(befer_variable_set)
            #print(befer_variable_set)
            binary_constrain.append(cspProblem.Constraint(befer_variable_set,before_function))
        #print(binary_constrain)

        if 'same-day' in i:
            i =i.replace('same-day','')
            i =i.replace(',,',',')
            #print(i)
            same_day_variable_set = []
            for j in i:
                if j==',':
                    same_day_variable_set.append(i[:i.index(j)])
                    same_day_variable_set.append(i[i.index(j)+1:])
            same_day_variable_set =tuple(same_day_variable_set)
            binary_constrain.append(cspProblem.Constraint(same_day_variable_set,same_day_function))
        #print(binary_constrain)

        if 'after' in i:
            i =i.replace('after','')
            i =i.replace(',,',',')
            #print(i)
            after_variable_set = []
            for j in i:
                if j==',':
                    after_variable_set.append(i[:i.index(j)])
                    after_variable_set.append(i[i.index(j)+1:])
            after_variable_set =tuple(after_variable_set)
            binary_constrain.append(cspProblem.Constraint(after_variable_set,after_function))
            #print(i)

        elif 'starts-at' in i:
            i = i.replace('starts-at','')
            i =i.replace(',,',',')
            #print(i)
            starts_at_set = []
            for j in i:
                if j==',':
                    starts_at_set.append(i[:i.index(j)])
                    starts_at_set.append(i[i.index(j)+1:])
            after_variable_set =tuple(starts_at_set)
            binary_constrain.append(cspProblem.Constraint(starts_at_set,starts_at_function))
            #print(i)

#domain
#hard domin constrains
    #print(hard_domain_constrain)
    for line in hard_domain_constrain:
        if len(line) ==3:
            #print(line)
            hard_domain_constrain_varaiable =[]
            if line[2] in week_number:
                #print(line[2])
                hard_domain_constrain_varaiable.append(line[1])
                hard_domain_constrain_varaiable = tuple(hard_domain_constrain_varaiable)
                binary_constrain.append(cspProblem.Constraint(hard_domain_constrain_varaiable,ne_(week_number[line[2]]//10)))

            if line[2] in day_number:
                #print(line[2])
                hard_domain_constrain_varaiable.append(line[1])
                hard_domain_constrain_varaiable = tuple(hard_domain_constrain_varaiable)
                binary_constrain.append(cspProblem.Constraint(hard_domain_constrain_varaiable,ne_time(day_number[line[2]])))

        if len(line) == 4:
            hard_domain_constrain_varaiable = []
            if line[2] =='starts-before':
                hard_domain_constrain_varaiable.append(line[1])
                time = day_number[line[3]]
                hard_domain_constrain_varaiable = tuple(hard_domain_constrain_varaiable)
                binary_constrain.append(cspProblem.Constraint(hard_domain_constrain_varaiable,start_before_t(time)))

            if line[2] =='ends-before':
                hard_domain_constrain_varaiable.append(line[1])
                time = day_number[line[3]]
                #print(time)
                hard_domain_constrain_varaiable = tuple(hard_domain_constrain_varaiable)
                binary_constrain.append(cspProblem.Constraint(hard_domain_constrain_varaiable,ends_before_t(time)))

            if line[2] =='starts-after':
                hard_domain_constrain_varaiable.append(line[1])
                time = day_number[line[3]]
                hard_domain_constrain_varaiable = tuple(hard_domain_constrain_varaiable)
                binary_constrain.append(cspProblem.Constraint(hard_domain_constrain_varaiable,start_after_t(time)))

            if line[2] =='ends-after':
                hard_domain_constrain_varaiable.append(line[1])
                time = day_number[line[3]]
                hard_domain_constrain_varaiable = tuple(hard_domain_constrain_varaiable)
                binary_constrain.append(cspProblem.Constraint(hard_domain_constrain_varaiable,ends_after_t(time)))

        if len(line) == 5:
            hard_domain_constrain_varaiable = []
            if line[2] =='starts-before':
                hard_domain_constrain_varaiable.append(line[1])
                day = week_number[line[3]]
                time = day_number[line[4]]
                daytime = day + time
                hard_domain_constrain_varaiable = tuple(hard_domain_constrain_varaiable)
                binary_constrain.append(cspProblem.Constraint(hard_domain_constrain_varaiable,start_before_d_t(daytime)))

            if line[2] =='starts-after':
                hard_domain_constrain_varaiable.append(line[1])
                day = week_number[line[3]]
                time = day_number[line[4]]
                daytime = day + time
                hard_domain_constrain_varaiable = tuple(hard_domain_constrain_varaiable)
                binary_constrain.append(cspProblem.Constraint(hard_domain_constrain_varaiable,start_after_d_t(daytime)))

            if line[2]=='ends-before':
                hard_domain_constrain_varaiable.append(line[1])
                day = week_number[line[3]]
                time = day_number[line[4]]
                daytime = day + time
                hard_domain_constrain_varaiable = tuple(hard_domain_constrain_varaiable)
                binary_constrain.append(cspProblem.Constraint(hard_domain_constrain_varaiable,ends_before_d_t(daytime)))

            if line[2]=='ends-after':
                hard_domain_constrain_varaiable.append(line[1])
                daytime = week_number[line[3]] + day_number[line[4]]
                hard_domain_constrain_varaiable = tuple(hard_domain_constrain_varaiable)
                binary_constrain.append(cspProblem.Constraint(hard_domain_constrain_varaiable,ends_after_d_t(daytime)))

        if len(line) == 6:
            time1 =0
            day2 =0
            hard_domain_constrain_varaiable =[]
            if line[2] == 'starts-in':
                hard_domain_constrain_varaiable.append(line[1])
                hard_domain_constrain_varaiable = tuple(hard_domain_constrain_varaiable)
                day1 =line[3]
                time2 =line[5]
                time1day2 =line[4]
                for i in time1day2:
                    if i =="-":
                        time1 = time1day2[:time1day2.index(i)]
                        day2 = time1day2[time1day2.index(i)+1:]
                day1time1 = week_number[day1]+day_number[time1]
                day2time2 = week_number[day2]+day_number[time2]
                binary_constrain.append(cspProblem.Constraint(hard_domain_constrain_varaiable,starts_in(day1time1,day2time2)))
                #print(day1time1)
                #print(day2time2)

            if line[2] == 'ends-in':
                hard_domain_constrain_varaiable.append(line[1])
                hard_domain_constrain_varaiable = tuple(hard_domain_constrain_varaiable)
                day1 =line[3]
                time2 =line[5]
                time1day2 =line[4]
                for i in time1day2:
                    if i =="-":
                        time1 = time1day2[:time1day2.index(i)]
                        day2 = time1day2[time1day2.index(i)+1:]
                day1time1 = week_number[day1]+day_number[time1]
                day2time2 = week_number[day2]+day_number[time2]
                binary_constrain.append(cspProblem.Constraint(hard_domain_constrain_varaiable,ends_in(day1time1,day2time2)))
                #print(day1time1)


    #domain
    #soft deadline constrains
    #print(soft_deadline_constrain)
    for line in soft_deadline_constrain:
        #print(line[1])
        #print(line[3])
        cost = line[5]
        time = week_number[line[3]]+day_number[line[4]]
        #print(time)
        soft_domain[line[1]] = time
        soft_cost[line[1]] = cost
    #print(soft_cost)


    #print()
    #print(binary_constrain)




#create CSP：
    #print("soft_cost:",soft_cost)
    CSP = Extend_CSP(task_domain,binary_constrain,soft_domain,soft_cost)
    SearchProblem = Search_with_AC_from_Cost_CSP(CSP)

    solution = GreedySearcher(SearchProblem).search()

    if solution:
        end = solution.end()
        for task in end:
            for item in end[task]:
                time = item[0]%10
                time_ = final_day_number[item[0]%10]
                day = final_week_number[item[0] - time]
                print(f'{task}:{day} {time_}')
        print("cost:{}".format(SearchProblem.heuristic(end)))
    else:
        print('No solution')

    #print(solution)

    '''
    solution = GreedySearcher(SearchProblem).search().end()
    if solution:
        for task in solution:
            for item in solution[task]:
                time = item[0]%10
                time_ = final_day_number[item[0]%10]
                day = final_week_number[item[0] - time]
                print(f'{task}:{day} {time_}')
        print("cost:{}".format(SearchProblem.heuristic(solution)))
    else:
        print('No solution')
    '''







