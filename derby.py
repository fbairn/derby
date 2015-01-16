#determine which boys race in which races in a pinewood derby
import random
from optparse import OptionParser

class Boy:
    def __init__(self, id):
        self.id = id            #id can be any hashable type,
                                #but each boy must have unique id
        self.racecount = 0      #number of times raced
        self.racedagainst = {}  #number of times raced against other boys

    def __repr__(self):
        '''return a string representation'''
        return '<Boy: %s>'%str(self.id)

    def race(self, others):
        '''add 1 to race counts'''
        self.racecount += 1
        for other in others:
            self.racedagainst[other.id] = self.racedagainst.get(other.id, 0) + 1

    def info(self):
        '''print some info about race counts'''
        print 'id:', self.id
        print 'races:', self.racecount
        print 'raced against:'
        for other in self.racedagainst:
            count = self.racedagainst[other]
            print '-', other, count

    def racedagainstcount(self, others):
        '''return the total number of times the boy has raced against others'''
        count = 0
        for other in others:
            count += self.racedagainst.get(other.id, 0)
        return count


def race_boys(race):
    '''record race for each boy'''
    for boy in race:
        others = race[:]
        others.remove(boy)
        boy.race(others)

def get_boys(numberofboys):
    return [Boy(i) for i in range(numberofboys)]

def generate_races(boys, racesize):
    '''
    yield repeated races for the given number of boys
    and the number of cars in each race
    '''
    while True:
        left = boys[:]                          #create a copy of the boys list for each race
        random.shuffle(left)                    #mix it up a bit
        left.sort(key = lambda x: x.racecount)  #take boys with fewest races first
        race = [left.pop(0)]
        for i in range(racesize-1):
            if not left: break                  #no boys left to add to race
            left.sort(key = lambda x: x.racedagainstcount(race)) #take boys with fewest races in common with boys already in the race
            race.append(left.pop(0))

        race_boys(race) #mark the boys as having raced
        yield race

def race(numberofboys, racesize):
    boys = get_boys(numberofboys)
    for race in generate_races(boys, racesize):
        print race
        for boy in race:
            boy.info()
        raw_input('press enter for next race')

def get_races(numberofboys, racesize, heats):
    boys = get_boys(numberofboys)
    racegen = generate_races(boys, racesize)
    races = []
    for race in racegen:
        races.append(race)
        if all([b.racecount>=heats for b in boys]):
            break
    return races

def races_to_csv_format(races):
    result = ''
    for race in races:
        result += ','.join([str(b.id) for b in race])+'\n'
    return result


def main():
    parser = OptionParser(usage="usage: %prog boys race-size heats [options]")
    parser.add_option("-f", "--file", action="store", dest="filename",
                      default=None, help="file to save results in as csv")

    options, args = parser.parse_args()

    numberofboys = int(args[0])
    racesize = int(args[1])
    heats = int(args[2])
    races = get_races(numberofboys, racesize, heats)
    csv_format = races_to_csv_format(races)
    if options.filename:
        with open(options.filename, 'w') as file:
            file.write(csv_format)
    else:
        print csv_format

if __name__ == '__main__':
    main()
