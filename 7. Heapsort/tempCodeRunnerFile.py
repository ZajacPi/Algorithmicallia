    def heapsort(self):
        for i in range(self.heap_size - 1, 0, -1):
            self.heap[0], self.heap[i] = self.heap[i], self.heap[0]  # Swap root with last element
            self.heap_size -= 1
            self.dequeue_repair(0)  # Repair heap from the root