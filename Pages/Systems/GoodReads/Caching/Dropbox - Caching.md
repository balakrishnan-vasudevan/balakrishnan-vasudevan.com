#caching 
tl:dr:
LRU is better

We have a large set of files, and we’d like an algorithm to determine which (k) files to keep at any point. We’re assuming all files have the same size. In fact, Dropbox stores files in 4MB blocks, so this simplification isn’t too far off (we’ll see later how to avoid it). To determine which files to keep, every time we want to use a file, we tell the cache to fetch it for us. If the cache has a file, it will give us its copy; if not, the cache has to fetch the new file, and it might also want to remove a file from its cache to make room for the new file.

Note also that we’re stuck with an on-line algorithm: we can’t predict what files a user will want in the future.

The cache needs to be fast, along two metrics. First, The cache should ensure that as many of the requests for files go to it (cache hit), not over the network (cache miss). Second, the overhead of using a cache should be small: testing membership and deciding when to replace a file should be as fast as possible. Maximizing cache hits is the goal of the first part of this post; quickly implementing the cache will be the topic of the second part.
### Most Recently Used

When we need to get rid of a file, we trash the one we just recently accessed. This algorithm incorporates information about how often a file is accessed in a perverse way – it prefers to keep around old data that is rarely used instead of data that is frequently accessed. But if you use many files, without using the same files over and over again (such as, say, when viewing a photo gallery), this algorithm works very well, since you’re kicking out files you’re unlikely to see again. In effect, browsing through a complete photo gallery can take up only one “slot” in the cache, since each access you kick out the previous photo in that gallery.

### Least Recently Used

When we need to get rid of a file, we get rid of the one we haven’t used in the longest time. This only requires keeping the access order of the files in the cache. By keeping files that we’ve recently accessed, it too tends to keep around files used more often; on the other hand, if a user’s interest changes, the entire cache can relatively quickly become tuned to the new interests. But this cache tends to work poorly if certain files are accessed every once in a while, consistently, while others are accessed very frequently for a short while and never again.

### Least Frequently Used

When we need to get rid of a file, we get rid of the one that is least frequently used. This requires keeping a counter on each file, stating how many times it’s been accessed. If a file is accessed a lot for a while, then is no longer useful, it will stick around, so this algorithm probably does poorly if access patterns change. On the other hand, if usage patterns stay stable, it’ll (we hope) do well.

Our LRU implementation needs to do two things quickly. It needs to access each cached page quickly, and it needs to know which files are most and least recent. The lookup suggests a hash table, maintaining recency suggests a linked list; then each step can be done in constant time. A hash table can point to its file’s node in the list, which we can then go ahead and move around. Here goes.

```
class DoubleLinkedNode:
    def __init__(self, prev, key, item, next):
        self.prev = prev
        self.key = key
        self.item = item
        self.next = next
 
class LRUCache:
    """ An LRU cache of a given size caching calls to a given function """
 
    def __init__(self, size, if_missing):
        """
        Create an LRUCache given a size and a function to call for missing keys
        """
 
        self.size = size
        self.slow_lookup = if_missing
        self.hash = {}
        self.list_front = None
        self.list_end = None
def get(self, key):
    """ Get the value associated with a certain key from the cache """
 
    if key in self.hash:
        return self.from_cache(key)
    else:
        new_item = self.slow_lookup(key)
 
        if len(self.hash) >= self.size:
            self.kick_item()
 
        self.insert(key, new_item)
        return new_item
```

To look up an item that's already in the cache, we just need to move its node in the list to the front of the list.

```
def from_cache(self, key):
    """ Look up a key known to be in the cache. """
 
    node = self.hash[key]
    assert node.key == key, "Node for LRU key has different key"
 
    if node.prev is None:
        # it's already in front
        pass
    else:
        # Link the nodes around it to each other
        node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else: # Node was at the list_end
            self.list_end = node.prev
 
        # Link the node to the front
        node.next = self.list_front
        self.list_front.prev = node
        node.prev = None
        self.list_front = node
 
    return node.item
```

To kick an item, we need only take the node at the end of the list (the one that's least recently used) and remove it.

```
def kick_item(self):
    """ Kick an item from the cache, making room for a new item """
 
    last = self.list_end
    if last is None: # Same error as [].pop()
        raise IndexError("Can't kick item from empty cache")
 
    # Unlink from list
    self.list_end = last.prev
    if last.prev is not None:
        last.prev.next = None
 
    # Delete from hash table
    del self.hash[last.key]
    last.prev = last.next = None # For GC purposes
```

Finally, to add an item, we can just link it to the front of the list and add it to the hash table.

```
def insert_item(self, key, item):
    node = DoublyLinkedNode(None, key, item, None)
 
    # Link node into place
    node.next = self.list_front
    if self.list_front is not None:
        self.list_front.prev = node
    self.list_front = node
 
    # Add to hash table
    self.hash[key] = node
```

There it is, a working, (k)-competitive, LRU cache.



Conclusion:
Caches can be used in front of any slow part of your application -- communication over a network, reads from disk, or time-intensive computation. Caching is especially important in mobile programs, where network communication is often both necessary and costly, so it's good to know the theory and do it right. Luckily, the best solution for caching problems is usually the Least Recently Used algorithm, which is both efficient and simple to implement.
