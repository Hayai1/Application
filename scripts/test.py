def mergeSort(elements):
        if len(elements) > 1:
            mid = len(elements)//2
            left = elements[:mid]
            right = elements[mid:]
            mergeSort(left)
            mergeSort(right)
            i = 0
            j = 0
            k = 0
            while i < len(left) and j < len(right):
                if left[i]['name'] < right[j]['name']:
                    elements[k] = left[i]
                    i += 1
                else:
                    elements[k] = right[j]
                    j += 1
                k += 1
            while i < len(left):
                elements[k] = left[i]
                i += 1
                k += 1
            while j < len(right):
                elements[k] = right[j]
                j += 1
                k += 1
        return elements

arr = [{"name" : "Dylan"},{"name" : "Lizzy"},{"name" : "Erin"},{"name" : "Maxine"},{"name" : "Stephan"},{"name" : "Andrew"}]
print(mergeSort(arr))