from asyncio import set_child_watcher
import random
import time
import matplotlib.pyplot as plt
from class_Path import *

class Test() :

    def __init__(self,file_path) :

        self.ged = file_path
        self.graph = Graph(file_path).print()
        self.path = Path(file_path)
        self.set = self.random_couples_set()
        self.paths, self.distances, self.execution_times = self.comparison_data()
    

    def random_set(self) :
        keys = list(self.graph.keys())
        set = []
        j = 0
        while j < 10 :
            i = random.randint(0,len(keys)-1)
            set += [keys[i]]
            j += 1
        return set 
    

    def random_couples_set(self) :
        set = []
        serie1,serie2 = self.random_set(), self.random_set()
        for i in range(len(serie1)) :
            set += [[serie1[i],serie2[i]]]
        return set


    def comparison_data(self) :
        distances = []
        paths = []
        execution_times = []
        for i in range(len(self.set)) : 
            start = time.time()
            shortest_path = self.path.get(self.set[i][0],self.set[i][1])
            if shortest_path != None :
                distances += [shortest_path[0]]
                paths += [shortest_path[1]]
                end = time.time()
                execution_times += [end-start]
        return paths, distances, execution_times


    def comparison_Dataframe(self) :
        df = pd.DataFrame({
            'Individuals' : self.set,
            'Path' : self.paths,
            'Distance' : self.distances,
            'Execution time (s)' : self.execution_times})
        df.set_index('Individuals',inplace=True)
        df.sort_values(by='Distance', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
        return df


    def average(self) :
        return sum(self.execution_times)/len(self.execution_times)

    
    def plot_Distance_Time(self) :
        a,b = np.polyfit(self.distances,self.execution_times,1)
        plt.scatter(self.distances,self.execution_times,marker='+')
        plt.plot(self.distances,a * np.array(self.distances) + b, color='r', linestyle='--', linewidth=0.5)
        plt.axis('equal')
        plt.xlabel('Path length')
        plt.ylabel('Execution time (seconds)')
        plt.title("Execution time in terms of path length")
        plt.text(50, 50, 'y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x', size=14)
        plt.show()

