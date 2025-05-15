Source: https://www.youtube.com/watch?v=uWGAUn2ZQnQ&list=PLCmime3ke_98RKjYJ1JBtyU9qJr7KIHEY&index=1&t=511s
- Mean vs Median vs Mode -
    - Mean = Measure of central tendency, the average value
    - Median - In a sorted data set, middle value
    - Mode - Frequently used value in a dataset
- Arithmetic mean - Not the 50% mark. Useful for comparing to previous conditions. In time series, need to calculate consistently to include new data
    - Moving/Block average
- Geometric mean - For things growing exponentially, multiply everything together, and take the nth root.
    - Number of deploys/unit, MTTR, Throughput calculations
- Harmonic mean - performance when there are multiple different systems involved.
    - Great for latency/throughput
    - Great for complex environments.
    - Divide n by the sum of reciprocals = n/(1/x1 + 1/x2 + …..+ 1/xn)
    - Useful for outliers, represents the lowest value the most.
    - Throughput when there is a single system instead of multiple systems
- Arithmetic mean > Geometric Mean > Harmonic Mean
- Harmonic and geometric mean can only be used for non-zero datasets
- Median
    - Always 50% point of a normal curve
    - Mean can be impacted by outlier and doesn’t recover spikes.
    - Response time monitoring, anomaly detection , capacity planning
- Mode
    - Most commonly used value
    - Log Analysis or Security monitoring.
- Probability - the possibility of an event happening
- Statistics - summation of information that has happened.
- Distributions
    - Normal = Data equally distributed.
        - Bell curve, not percent based
        - Lead time measurement, anomaly analysis, SLO/SLI calculation
    - Poisson - Used to model the occurrence of rare events
    - Beta - Success/failure of binomial events
    - Exponential - Time between async events
        - Models the rate (time between events that are unrelated)
        - Network performance, user requests, messaging service, system failures
    - Weibull - Likelihood of failure
        - defined by a shape and a scale parameter
    - Log normal - Values based on many small events
- Descriptive vs Inferential statistics
    - Descriptive uses whole data set to drive statistical conclusions.
        - Used for visualization, can define+extract trends
    - Inferential uses sampled data to draw conclusions.
        - Used for predictions or hypotenuse testing, can also visualize.
        - leads to sampling.
- Monitoring is now becoming a data problem. Observability (signals, metrics, traces, logs) adds to the amounts of data being ingested. This brings a need for sampling.
- Sampling - can give false indications, changes behavior from descriptive to inferential, necessary evil
    - Random sampling
    - Stratified sampling
    - Cluster sampling
    - Systematic sampling
    - Purposive sampling

## Create a summary section at the bottom.

<aside> 💡 Statistics are aggregation and reduction to reveal central tendencies. They do not show individual behavior.

</aside>