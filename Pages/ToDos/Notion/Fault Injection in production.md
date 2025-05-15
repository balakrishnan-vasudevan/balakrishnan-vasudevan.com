Source: https://queue.acm.org/detail.cfm?id=2353017
To confirm its ability to withstand failures gracefully, Etsy put together a list of reasonable scenarios to prepare for, develop against, and test in production, including the following:

- One of the app servers dies (power cable yanked out).
- All of the app servers leave the load-balancing pool.
- One of the app servers gets wiped clean and needs to be fully rebuilt from scratch.
- Database dies (power cable yanked out and/or process is killed ungracefully).
- Database is fully corrupt and needs full restore from backup.
- Offsite database replica is needed to investigate/restore/replay single transactions.
- Connectivity to third-party sites is cut off entirely.

The engineers then put together all of the expectations for how the system would behave if these scenarios occurred in production, and how they could confirm these expectations with logs, graphs, and alerts. Once armed with these scenarios, they worked on how to make these failures either:

- not matter at all (transparently recover and continue on with processing),
- matter only temporarily (gracefully degrade with no data loss and provide constructive feedback to the user),
- or matter only to a minimal subset of users (including an audit log for reconstructing and recovering quickly and possibly automatically).

After these mechanisms were written and tested in development, the time came to test them in production. The Etsy team was cognizant of how much activity the system was seeing; the support and product groups were on hand to help with any necessary communication; and team members went through each of the scenarios, gathering answers to questions such as:

- Were they successful in transparently recovering, through redundancy, replication, queuing, etc.?
- How long did each process take—in the case of rebuilding a node automatically from scratch, recovering a database, etc.?
- Could they confirm that no data was lost during the entire exercise?
- Were there any surprises?