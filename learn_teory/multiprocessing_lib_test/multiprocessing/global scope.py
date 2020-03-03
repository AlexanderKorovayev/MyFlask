import multiprocessing 
import threading

# empty list with global scope 
result = [] 


def square_list(mylist):
    """ 
    function to square a given list 
    """

    # append squares of mylist to global list result 
    for num in mylist: 
        result.append(num * num) 
    # print global list result
    print(f"Result in {multiprocessing.current_process().name}: {result}")
  

if __name__ == "__main__":
    # input list 
    mylist = [1, 2, 3, 4]
  
    # creating new process 
    p1 = multiprocessing.Process(target=square_list, args=(mylist,))
    # p1 = threading.Thread(target=square_list, args=(mylist,))
    # starting process 
    p1.start() 
    # wait until process is finished 
    p1.join() 
  
    # print global result list 
    print(f"Result in {multiprocessing.current_process().name}: {result}")
