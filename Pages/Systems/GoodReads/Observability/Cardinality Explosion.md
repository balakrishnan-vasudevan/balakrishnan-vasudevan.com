

"Cardinality explosion" happens when we associate attributes to metrics and sending them to a time series database without a lot of thought. A unique combination of an attribute with a metric creates a new timeseries.  
The first portion of the image shows the time series of a metrics named "requests", which is a commonly tracked metric.  
The second portion of the image shows the same metric with attribute of "status code" associated with it.  
This creates three new timeseries for each request of a particular status code, since the cardinality of status code is three.  
But imagine if a metric was associated with an attribute like user\_id, then the cardinality could explode exponentially, causing the number of generated time series to explode and causing resource starvation or crashes on your metric backend.  
Regardless of the signal type, attributes are unique to each point or record. Thousands of attributes per span, log, or point would quickly balloon not only memory but also bandwidth, storage, and CPU utilization when telemetry is being created, processed, and exported.

This is cardinality explosion in a nutshell.  
There are several ways to combat this including using o11y views or pipelines OR to filter these attributes as they are emeitted/ collected.

![[Pasted image 20250421102409.png]]