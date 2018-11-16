from random import shuffle
import datetime


def read(input_path): # Return a list
    rtn = []
    lines = [line.rstrip('\n') for line in open(input_path)][1:]
    for line in lines:
        data = line.split(",")
        data = [s.strip() for s in data]
        p = Person(data[0], data[1], data[2], data[3], data[4], data[5])
        rtn.append(p)
    return rtn


def write(groups, output_path):
    max_size = max([len(g) for g in groups])
    while len(groups[0]) < max_size: groups[0].append(Person())
    while len(groups[1]) < max_size: groups[1].append(Person())
    while len(groups[2]) < max_size: groups[2].append(Person())
    while len(groups[3]) < max_size: groups[3].append(Person())

    g1 = [p.name for p in groups[0]]
    g2 = [p.name for p in groups[1]]
    g3 = [p.name for p in groups[2]]
    g4 = [p.name for p in groups[3]]

    f = open(output_path, "w")
    header = "Group1, Group2, Group3, Group4\n"
    f.write(header)
    for i in range(max_size):
        line = g1[i] + ", " + g2[i] + ", " + g3[i] + ", " + g4[i] + "\n"
        f.write(line)
    print("CSV file was created: " + output_path)



def grouping(people):
    groups = [[], [], [], []]

    tcm = []
    tncm = []
    ntcm = []
    ntncm = []
    tcf = []
    tncf = []
    ntcf = []
    ntncf = []

    # Helper categorize function
    def categorize(person):
        if person.talk:  # talk
            if person.christian:  # talk, christian
                if person.gender == "M": #talk, christian, male
                    tcm.append(person)
                else: # talk, christain, female
                    tcf.append(person)
            else: # talk, not christian
                if person.gender == "M": # talk, not christian, male
                    tncm.append(person)
                else: # talk, not christian, female
                    tncf.append(person)
        else: # not talk
            if person.christian: # not talk, christian
                if person.gender == "M": # not talk, christian, male
                    ntcm.append(person)
                else: # not talk, christian, female
                    ntcf.append(person)
            else: # not talk, not christian
                if person.gender == "M": # not talk, not christian, male
                    ntncm.append(person)
                else: # not talk, not christian, female
                    ntncf.append(person)
    # end helper function

    for p in people:
        if p.fixed_group != "0":
            g_index = int(p.fixed_group) - 1
            groups[g_index].append(p)
        else:
            categorize(p)

    shuffle(tcm)
    shuffle(tncm)
    shuffle(ntcm)
    shuffle(ntncm)
    shuffle(tcf)
    shuffle(tncf)
    shuffle(ntcf)
    shuffle(ntncf)

    not_fixed = []

    not_fixed += tcm
    not_fixed += tncm
    not_fixed += ntcm
    not_fixed += ntncm
    not_fixed += tcf
    not_fixed += tncf
    not_fixed += ntcf
    not_fixed += ntncf

    sizes = [len(g) for g in groups]
    i = which_min(sizes)

    for p in not_fixed:
        groups[i%4].append(p)
        i += 1

    return groups


def which_min(sizes):
    min_s = min(sizes)
    for i in range(len(sizes)):
        if sizes[i] == min_s: return i

class Person():
    # name, gender, talk, christian, counselor, fixed_group = None, None, None, None, None, None

    def __init__(self, name="", gender="", talk="", christian="", counselor="", fixed_group=""):
        self.name = name.upper()
        self.gender = gender.upper()
        self.talk = talk.upper() == "Y"
        self.christian = christian.upper() == "Y"
        self.counselor = counselor.upper() == "Y"
        self.fixed_group = fixed_group



    def __str__(self) -> str:
        return "Name: " + self.name + \
               " Talk = " + str(self.talk) + \
               " Christian = " + str(self.christian) + \
               " Counselor = " + str(self.counselor) + \
               " Fixed_group = " + self.fixed_group

    def getFix(self):
        return self.fixed_group

def print_groups(groups):
    for i in range(len(groups)):
        print("Group ", i+1)
        for p in groups[i]:
            print(p)

def getDate():
    now = datetime.datetime.now()
    return str(now.month) + str(now.day) + str(now.year)



if __name__ == '__main__':
    input_path = "/Users/Philip/Desktop/input.csv"
    d = getDate()
    output_path = "/Users/Philip/Desktop/" + d + "分組.csv"
    people = read(input_path)
    groups = grouping(people)
    write(groups, output_path)

