# Consistent Hashing

Tags: consistent-hashing
Status: Not started
URL: https://www.paperplanes.de/2011/12/9/the-magic-of-consistent-hashing.html

https://abhistrike.hashnode.dev/the-magic-of-consistent-hashing-a-secret-weapon-for-efficient-load-balancing

The simplicity of consistent hashing is pretty mind-blowing. Here you have a number of nodes in a cluster of databases, or in a cluster of web caches. How do you figure out where the data for a particular key goes in that cluster?

You apply a hash function to the key. That’s it? Yeah, that’s the whole deal of consistent hashing. It’s in the name, isn’t it?

The same key will always return the same hash code (hopefully), so once you’ve figured out how you spread out a range of keys across the nodes available, you can always find the right node by looking at the hash code for a key.

![image.png](image%205.png)