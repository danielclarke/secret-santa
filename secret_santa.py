#!/usr/bin/env python

import csv
import random
import os
import string

class Santa:
    def __init__(self, name, giftee, family, exclusions):
        this.name = name
        this.giftee = giftee
        this.family = family
        this.exclusions = exclusions
        this.exclusions.append(this.name)

def shapes(list_2d):
    s = []
    for r in list_2d:
        s.append(len(r))
    return s

def read_families(directory):
    '''Reads a directory of .csv files where each family is in its
       own .csv file. family members are written on rows according to
       generation. The family members are stored in a dictionary with
       last name as the key word. the dict is the return arg.
    '''
    surnames = [x[2] for x in os.walk(directory)][0]
    families = {}
    for s in surnames:
        f = open(directory + '/' + s, 'r')
        reader = csv.reader(f)
        families[s] = [r for r in reader]
    return families

def check_shuffle(a):
    for i in range(len(a) - 1):
        if a[i][1] == a[i + 1][1]:
            return False
    if a[-1][1] == a[0][1]:
        return False
    return True

def assign_santas(families):
    santas = {}
    #organise each family member in into generation groups
    pool = [[] for k in range(len(families[families.keys()[0]]))]
    for j in range(len(families[families.keys()[0]])):
        for i in families.keys():
            pool[j] = pool[j] + [[f, i] for f in families[i][j]]

    #shuffle the groups so that no two people from the same family
    #are next to each other
    for i in range(len(pool)):
        while not check_shuffle(pool[i]):
            random.shuffle(pool[i])

    #santas and giftees are paired within the same generation
    for j in range(len(pool)):
        for i in range(len(pool[j]) - 1):
            santas[pool[j][i][0] + ' ' + pool[j][i][1]] = \
            pool[j][i + 1][0] + ' ' + pool[j][i + 1][1]
        #assign the first person's santa to be the last person
        santas[pool[j][-1][0] +  ' ' + pool[j][-1][1]] = \
        pool[j][0][0] + ' ' + pool[j][0][1]

    return santas

def check_santas(santas, families):
    #check each family member is a santa and giftee
    for key in families.keys():
        for generation in families[key]:
            for member in generation:
                if (member + ' ' + key in santas.keys()) == False:
                    print member + ' ' + key + " is not a santa"
                    break
                if (member + ' ' + key in santas.values()) == False:
                    print member + ' ' + key + " is not a giftee"
                    break
    #check that no santa is giving to a person in the same family
    for santa in santas:
        if santas[santa].split()[1] == santa.split()[1]:
            print "santa assignment within the same family: " + \
                santa.split()[1]
            break

def main():
    santas = assign_santas(read_families('families'))
    f = open("santas_list.txt", "w")
    for s in santas.items():
        f.write(string.capwords(s[0]) + " is a Santa for " + string.capwords(s[1]))
        f.write("\n")
    check_santas(santas, read_families('families'))

if __name__ == '__main__':
    main()