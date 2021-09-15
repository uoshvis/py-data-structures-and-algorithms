# Memory management

Computer memory is organized into a sequence of **words**, each 
of which typically consists of 4, 8, or 16 bytes (depending on the computer).

The number associated with each memory
word is known as its **memory address**.

Management - to determine what data is stored in what memory cells.

## Memory allocation in Python

All objects are stored in a pool of memory,
a.k.a. the **memory heap** (or Python heap).
Should not be confused with data structure "heap".

The storage available in the memory heap is divided into **blocks**.

Contiguous *“holes”* of available free memory are kept
in a linked list, called the **free list**.

Fragmentation - separation of unused memory into separate holes.

**Internal fragmentation** occurs when a portion of an allocated memory block is unused.

**External fragmentation** occurs when there is a
significant amount of unused memory between several contiguous blocks of allocated memory.

### External fragmentation minimization

The **best-fit** algorithm searches the entire free list to find the hole whose size is closest to the amount of memory being
requested.

The **first-fit** algorithm searches from the beginning of the free list for the first hole that is large enough.

The **next-fit** algorithm is similar, in that it also searches the free list for the first hole that is large enough,
but it begins its search from where it left off previously, viewing the free list as a circularly linked list.

The **worst-fit** algorithm searches the free list to find the largest hole of available memory,
which might be done faster than a search of the entire free list

## Garbage Collection

The process of detecting “stale” objects,
deallocating the space devoted to those objects,
and returning the reclaimed space to the free list is known as **garbage collection**.

**Live objects** object having a direct or indirect reference from a program. 

**Direct reference** to an object is in the form of an identifier in an active namespace.

**Root objects** - objects with direct references.

**An indirect reference** is a reference
that occurs within the state of some other live object.

Live objects should not be deallocated.

**Reference count** integer of how many references to the object exists in the system.

#### Algorithm for garbage collection:

**Mark-sweep algorithm** - reclaims unused space in time proportional to the number of live
objects and their references plus the size of the memory heap.

### Memory used by the Python Interpreter

A running Python program has a private stack, known as the **call stack**
or Python interpreter stack, that is used to keep track of the nested sequence of
currently active (that is, nonterminated) invocations of functions.

**Activation record or frame** - entry of the stack,
storing information about an invocation of a function.

At the top - activation record of the **running call**: 
**running call** - is the function activation that currently has control of the execution.

**Suspended calls** the remaining elements of the stack.

The activation record for a function call also includes a reference to
the function definition itself, and a special variable, known as the **program counter**.


## Memory Hierarchies And Caching

### Memory hierarchy

Size increases --->>

CPU --> Register --> Caches --> Internal memory -->> External Memory --> Network Storage

Speed decreases -->>

### Caching 

Locality of reference:
 - **Temporal locality**
 - **Spatial locality**

Page replacement policies:
 - **Firs-in, first-out (FIFO)**
 - **Least recently used (LRU)**
 - **Random**
