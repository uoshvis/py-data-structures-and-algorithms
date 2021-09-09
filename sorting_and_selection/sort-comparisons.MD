# Sorting Algorithms

### Running times

| O(n^2) in the avg and worst case                         | O(n log n) | linear time for certain types of keys| 
|----------------------------------------------------------|------------|--------------------------------------|
| insertion-sort                                           | heap-sort  |bucket-sort                           |
| selection-sort                                           | merge-sort |radix-sort                            |
|                                                          | quick-sort |                                      |

### Trade-offs

- Efficiency
- Memory usage
- Stability

#### Insertion sort

- Running time O(m+n), where m - number of inversions
- Excellent for sorting small sequences (< 50)
- Excellent for almost sorted
- O(n^2) time performance makes it a poor choice outside special contexts

#### Selection sort

- Poor choice since the best case is O(n^2)

#### Heap sort

- O(n log n) optimal run time
- Can execute in-place
- Natural choice on small - and medium-sized sequences
when input data can fit into main memory
- Outperformed by both quick-sort and merge-sort on larger sequences
- Does not provide stable sort, because of the swapping elements

#### Merge sort

- Runs O(n log n) time in the worst case
- Difficult to make run in-place for arrays
- Less attractive than in-place implementations of heap-sort and quick-sort
- An excellent algorithm for situations where the input
  is stratified across various levels of computer's memory hierarchy
  (e.g., cache, main memory, external memory)
- The GNU sorting utility relies on a multiway merge-sort variant
- Since 2003, the standard sort method
of Python’s list class has been a hybrid approach named *Tim-sort* (designed by Tim
Peters), which is essentially a **bottom-up merge-sort** that takes advantage of some
initial runs in the data while using **insertion-sort** to build additional runs.
- Tim-sort is the default algorithm for sorting arrays in Java7

#### Quick sort

- O(n^2) worst time performance makes susceptible in real-time applications
- Expected performance O(n log n) outperforms both heap-sort and merge-sort
- Does not provide stable sort, due to swapping of elements during partitioning step
- For decades was the default choice for a general-purpose, in-memnory sorting algorithm (C, Unix, Java 6)

#### Bucket sort and Radix sort

- Excellent choice if an application involves sorting entries with small integer keys, character
strings, or d-tuples of keys from a discrete range
- Runs in O(d(n+N)) time, where [0, N-1] is the range of integer keys (d=1 for bucket sort)
- Thus, if d(n+N) is significantly "below" n log n function, then this
sorting method should run faster than even quick-sort, heap-sort, or merge-sort.
