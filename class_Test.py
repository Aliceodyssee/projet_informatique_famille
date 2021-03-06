from asyncio import set_child_watcher
import random
import time
import matplotlib.pyplot as plt
from class_Path import *

class Test() :

    def __init__(self,file_path) :

        self.ged = file_path
        self.graph = Graph(file_path).build()
        self.path = Path(file_path)
        self.set = self.random_couples_set()
        self.data_set = [['@I173@','@I6452@'],['@I10994@','@I8418@'],['@I903@','@I895@'],['@I2239@','@I2243@'],['@I10105@','@I6794@'],['@I6214@','@I6225@'],['@I8709@','@I8723@'],['@I10914@','@I8821@'],['@I3139@','@I3014@'],['@I6013@','@I2181@'],['@I11247@','@I11232@'],['@I7488@','@I7479@'],['@I8359@','@I8944@'],['@I9383@','@I7501@']]
        self.paths, self.distances, self.dij_distances, self.execution_times,self.dij_execution_times, self.difference = self.comparison_data()
    

    def random_set(self) :
        keys = list(self.graph.keys())
        set = []
        j = 0
        while j < 5 :
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
        dij_distances = []
        paths = []
        execution_times = []
        dij_execution_times = []
        difference = []

        for i in range(len(self.data_set)) : 
            start = time.time()
            shortest_path = self.path.get(self.data_set[i][0],self.data_set[i][1])
            end = time.time()
            #print(self.data_set[i])
            if shortest_path != None :

                dij_start = time.time()
                #dij_shortest_path = self.path.get_dij(self.set[i][0],self.set[i][1])
                dij_shortest_path = self.path.get_dij(self.data_set[i][0],self.data_set[i][1])
                dij_end = time.time()

                distances += [shortest_path[0]]
                dij_distances += [dij_shortest_path[0]]
                paths += [dij_shortest_path[1]]
                execution_times += [end-start]
                dij_execution_times += [dij_end-dij_start]
                difference += [execution_times[-1]-dij_execution_times[-1]]

        return paths, distances, dij_distances, execution_times, dij_execution_times, difference



    def comparison_Dataframe(self) :
        df = pd.DataFrame({
            'Individuals' : self.data_set,
            'Path' : self.paths,
            'Distance' : self.distances,
            'Dijkstar distance' : self.dij_distances,
            'Execution time (s)' : self.execution_times,
            'Dijkstar execution time (s)' : self.dij_execution_times, 
            'Difference of execution time (s)' : self.difference })
        df.set_index('Individuals',inplace=True)
        df.sort_values(by='Distance', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
        return df


    def average(self) :
        return sum(self.execution_times)/len(self.execution_times), sum(self.dij_execution_times)/len(self.dij_execution_times)

    
    def plot_Distance_Time(self) :
        a,b = np.polyfit(self.distances,self.execution_times,1)
        plt.scatter(self.distances,self.execution_times,marker='o', label = 'Naive version')
        plt.scatter(self.dij_distances,self.dij_execution_times, marker='+',color='g', label = "Dijkstra")
        plt.plot(self.distances,a * np.array(self.distances) + b, color='r', linestyle='--', linewidth=0.5)
        plt.axis('equal')
        plt.legend()
        plt.xlabel('Path length')
        plt.ylabel('Execution time (seconds)')
        plt.title("Execution time in terms of path length")
        plt.text(4, 10, 'y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x', size=14)
        plt.show()


    def plot_difference(self):

        rate = 0
        for k in self.difference:
            if k > 0 :
                rate += 1
        
        print(f"In {rate/len(self.difference)*100}% of cases, the Dijkstra algorithm is faster.")

        a,b = np.polyfit(self.distances,self.difference,1)
        plt.scatter(self.distances,self.difference, marker='+')
        plt.hlines(y=0,xmin=min(self.distances),xmax=max(self.distances),color='r')
        plt.title("Difference in execution time between the naive and Dijkstar algorithms")
        plt.show()