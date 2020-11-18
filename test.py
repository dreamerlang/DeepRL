import os
if __name__ == '__main__':
    list1=[4,4]
    list2 = [5, 4]
    list3 = [1, 3]
    list4 = [2, 5]
    list5 = [2, 1]
    lists=[]
    lists.append(list1)
    lists.append(list2)
    lists.append(list3)
    lists.append(list4)
    lists.append(list5)
    print(lists)
    lists.sort()
    print(lists)
    print(lists[1])