def merge_k_sorted_linked_lists(lists):
    import heapq
    
    class ListNode:
        def __init__(self, val=0, next=None):
            self.val = val
            self.next = next
            
        def __lt__(self, other):
            return self.val < other.val
    
    min_heap = []
    
    # Initialize the heap with the head of each linked list
    for l in lists:
        if l:
            heapq.heappush(min_heap, l)
    
    # Dummy node to help build the result linked list
    dummy = ListNode(0)
    current = dummy
    
    while min_heap:
        # Get the smallest node from the heap
        smallest_node = heapq.heappop(min_heap)
        current.next = smallest_node
        current = current.next
        
        # If there is a next node, push it into the heap
        if smallest_node.next:
            heapq.heappush(min_heap, smallest_node.next)
    
    return dummy.next

# Unit tests
def test_merge_k_sorted_linked_lists():
    class ListNode:
        def __init__(self, val=0, next=None):
            self.val = val
            self.next = next
            
        def __lt__(self, other):
            return self.val < other.val
    
    # Helper function to create a linked list from a list
    def create_linked_list(arr):
        dummy = ListNode(0)
        current = dummy
        for value in arr:
            current.next = ListNode(value)
            current = current.next
        return dummy.next
    
    # Helper function to convert linked list to a python list
    def linked_list_to_list(node):
        result = []
        while node:
            result.append(node.val)
            node = node.next
        return result

    # Test cases
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([]), create_linked_list([])])) == []
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([1]), create_linked_list([2]), create_linked_list([3])])) == [1, 2, 3]
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([1, 4, 5]), create_linked_list([1, 3, 4]), create_linked_list([2, 6])])) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([1, 2, 3]), create_linked_list([4, 5]), create_linked_list([6, 7, 8])])) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([5, 10]), create_linked_list([1, 2, 3]), create_linked_list([])])) == [1, 2, 3, 5, 10]
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([1]), create_linked_list([1]), create_linked_list([2]), create_linked_list([2])])) == [1, 1, 2, 2]
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([1, 3]), create_linked_list([2, 4]), create_linked_list([5, 6])])) == [1, 2, 3, 4, 5, 6]
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([0, 1]), create_linked_list([1]), create_linked_list([-1])])) == [-1, 0, 1, 1]
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([1, 4, 5]), create_linked_list([1, 3, 4]), create_linked_list([2, 6]), create_linked_list([])])) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([]), create_linked_list([]), create_linked_list([])])) == []
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([1]), create_linked_list([0]), create_linked_list([-1])])) == [-1, 0, 1]
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([1, 2, 3]), create_linked_list([1, 2, 3]), create_linked_list([1, 2, 3])])) == [1, 1, 1, 2, 2, 2, 3, 3, 3]
    assert linked_list_to_list(merge_k_sorted_linked_lists([create_linked_list([1, 3, 5]), create_linked_list([2, 4, 6]), create_linked_list([0, 7, 8])])) == [0, 1, 2, 3, 4, 5, 6, 7, 8]

test_merge_k_sorted_linked_lists()
