import multiprocessing
import concurrent.futures


def square_list(mylist, result, square_sum):
    """
    function to square a given list
    """

    for idx, num in enumerate(mylist):
        result[idx] = num * num

    # square_sum value
    square_sum.value = sum(result)

    # print result Array
    print(f"Result in {multiprocessing.current_process().name}: {result[:]}")

    # print square_sum Value
    print(f"Sum of squares {multiprocessing.current_process().name}: {square_sum.value}")


result = []


def square_list1(mylist):
    """
    function to square a given list
    """
    # append squares of mylist to result array
    for idx, num in enumerate(mylist):
        result[idx] = num * num

    # print result Array
    print(f"Result in {multiprocessing.current_process().name}: {result[:]}")


if __name__ == "__main__":
    # input list
    mylist1 = [1, 2, 3, 4]

    # creating Array of int data type with space for 4 integers
    result = multiprocessing.Array('i', 4)
    # creating Value of int data type
    square_sum = multiprocessing.Value('i')
    # creating new process
    # with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
         # executor.submit(square_list1, mylist1)
         # executor.submit(square_list, mylist1, result, square_sum)

    p1 = multiprocessing.Process(target=square_list, args=(mylist1, result, square_sum))
    p1.start()
    p1.join()

    # print result Array
    print(f"Result in {multiprocessing.current_process().name}: {result[:]}")

    # print square_sum Value
    print(f"Sum of squares {multiprocessing.current_process().name}: {square_sum.value}")

