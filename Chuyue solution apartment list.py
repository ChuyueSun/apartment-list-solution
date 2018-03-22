from pythonds.graphs import Graph, Vertex
from pythonds.basic import Queue



def buildGraph(filename) :
    '''
    This function builds a graph for all words in filename
    Create edges for any two friends
    input: txt file
    output: a graph as described above
    '''
    
    
#   dictionary for words with the same length 
#   similar to word ladder
    bucket = {}         

#    build a dictionary such that bucket[l]:all words with len(word)=l
    word_dic = {}   
#   initiate an empty graph      
    g = Graph()
    
    print('Loading word list from file',filename)  
    wfile = open(filename, 'r')
 
    
#        read into word_dic
    for line in wfile:
#        load words
        word = line[:-1]    
        length = len(word)

        if length not in word_dic:   
            word_dic[length]=[]
        word_dic[length].append(word)
    
    l_min = min(word_dic)       

    
    
    for length in word_dic:           # 按长度增序添加跨长度Edge或装入桶1
        word_list_now = word_dic[length]

        if length > l_min:
            set_lower = set(word_dic[length-1])
        else:
            set_lower = {}


        for word in word_list_now:
#            similar to word ladder
#            use bucket to identify words in the same length only differ by one letter
            for i in range(length): 
#                create label
                bucket_label = word[:i] + '_' + word[i + 1:]
                if bucket_label in bucket:
                    bucket[bucket_label].append(word)
                else:
                    bucket[bucket_label] = [word]

#               add two-direction edges between two words with different lenght
                word_lower = word[:i] + word[i + 1:]
                if word_lower in set_lower: 
                    g.addEdge(word, word_lower)
                    g.addEdge(word_lower, word)

# add vertices and edges for words in the same bucket
    for bucket_label in bucket:
        for word1 in bucket[bucket_label]:   
            for word2 in bucket[bucket_label]:
                if word1 != word2:
                    g.addEdge(word1, word2)
    
    print('buildGraph Done.')
    return g




def bfs(g, start): 
    count = 1
    start.setColor('grey')

    vertQueue = Queue()
    vertQueue.enqueue(start)
    while vertQueue.size() > 0 :
        currentVert = vertQueue.dequeue()
        for swan in currentVert.getConnections():
#            not searched vertices are white
            if (swan.getColor() == 'white'):
                count += 1
#                if already searched, mark it as grey
                swan.setColor('grey')
                vertQueue.enqueue(swan)
    return count





def count_friends(filename,name_to_search):
    
#   build a friend graph    
    g=buildGraph(filename)
#   find starting vertice of the name    
    start_position=g.getVertex(name_to_search)
    return bfs(g, start_position)

    


def test_count_friends():
    '''
    use the very_small_test and the test case given in the problem to test count_friends

    '''
    print('************test case**************')

    # Test for very_short_test_dictionary
    print('The correct answer for LISTY in very_short_dictionary is 5.')
    print('My answer is',count_friends('very_small_test_dictionary.txt','LISTY'),'.')

    # Test for tests given in the problem
    print('The correct answer for HI in [HI HERE THERE HER HE SHE HEAR HALLOW] is 7.')
    print('My answer is',count_friends('test.txt','HI'),'.')
    print('************test case**************')


test_count_friends()






filename='dictionary.txt'
name_to_search='LISTY'

print('Social network for',name_to_search,'is',count_friends(filename,name_to_search))
