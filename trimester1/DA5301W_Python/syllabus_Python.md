# Syllabus (Python)

Copied from "Course Plan" in 1st intro lecture PDF.

- [x] Python Foundations
- [x] Working Environments & Dependencies
- [x] Algorithm Complexity, Core Data Structures & Object-Oriented Programming
- [x] Git Fundamentals
- [ ] Numpy Essentials for Data Science
- [ ] Pandas Essentials for Data Science
- [ ] Visualisation in Python: Matplotlib, Plotly, Seaborn
- [ ] Graphs & Traversals: `networkx` library
- [ ] Sorting, Searching and Queues
- [ ] Debugging and Testing
- [x] AI Assisted Coding

## Study Plan

- [x] READ rem lectures of Module 10: merge sort, insertion sort, tim sort, heap & priority queue
- [ ] READ all notebooks (quickly, dont think any online extra info is required)
    - [x] Debugging & Testing (includes `pytest`, `pydantic`, `pandera` for df schema validate)
    - [x] CustomExceptionsExample
    - [x] Logging
    - [ ] NetworkX - WIP
    - [x] Visualization: `matplotlib`, `plotly`, `seaborn`
    - [x] SortBisectHeapq `bisect` module: 
        * `bisect(list, elem)` & `bisect_left()`: find insertion point from right, left;
        * `insort(list, elem)` & `insort_left()`: insert elem from right, left
    - [x] SortBisectHeapq `heapq` module: `heapify` O(n), `heappush`, `heappop`, `nlargest`, `nsmallest`
        * by default min-heap, negate all elems to get max-heap
        * new python has methods for max variant
    - [ ] Numpy: `np.linspace(start,stop,num_elems)`
    - [ ] Pandas: `df.select_dtypes("number")` select only numeric columns ; `df.corr()` correlation
- [x] READ complexity formulae (of all sort & graph, tree algos)
- [ ] CODE (spend most time here!) - before impl, READ algo impls in lecture slides!!:
    - [ ] REVISE `logging` as Prof Jayadev said coding questions can come
    - [ ] sort: selection, insert (with & without `bisect`), merge (with & without `heapq.merge()`)
    - [ ] heap & priority queue with `heapq`
    - [ ] binary search (with & without`bisect`)
    - [ ] graph algos: BFS (use `collections.dequeue`), DFS, Dijkstra etc.
- [ ] ASSIGNMENT Python Assignment Q4 revise (do with DFS or BFS)
- [ ] REVISE `numpy`, `pandas`
- [x] REVISE all theory
- [ ] REVISE all assignment questions