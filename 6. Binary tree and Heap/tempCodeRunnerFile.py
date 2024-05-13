
    def dequeue_repair(self, i):
        left = self.left(i)
        right = self.right(i)
        #jak doszliśmy tak głęboko że szukamy indeksów które nie istnieją musimy przerwać
        if right > self.heap_size-1 or left > self.heap_size-1:
            return
        swapp = self.heap[i]
        if swapp < self.heap[left]:
            if swapp < self.heap[right]:
                #zamieniam z WIĘKSZYM z tej dwójki
                if self.heap[left] < self.heap[right]:
                    temp = self.heap[right]
                    self.heap[right] = self.heap[i]
                    self.heap[i] = temp
                    return self.dequeue_repair(right)       
            temp = self.heap[left]
            self.heap[left] = swapp
            self.heap[i] = temp
            return self.dequeue_repair(left)

        #dzieci są mniejsze, zwracam none
        else:
            return None 
