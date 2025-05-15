#linux
Example 1 : _System is slow_

1. start with command top for processes and cpu
2. Check Disk io (iostat), and network (sar) What to do in such a case : Quantify the problem, is it latency etc. Check system resources with methodologies, run through the checklist.

Example 2: Application Latency is higher. USE METHOD:

1. **top** command - Check cpu summary, process/kernel time, cpu utilization (if it is 100 percent or not).
2. CPU utilization again with **vmstat** to see paterns. Check memory, if there is enough left and is not leaninig towards saturation point.
3. **mpstat** to check if maxing out any cpu

```
Utilization and saturation metrics: swapping not too much, enough memory left, cpu are not overloaded, cpu time for kernel/application is not too much, r is not a lot more than cpu present.
CPU saturation/utiliation is flexible in case of linux,  kernel manages/moves things around, interrups threads etc if needed. same is not the case with io. 
```

4. Check Disk IO utiliation. **iostat**. util column: more than 60 percent utilization might the problem.
5. Check Network IO utilization **sar -n DEV 1**.
6. pidstat for process wise usage of.