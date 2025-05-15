https://medium.com/@ahmedmansouri/why-you-need-to-pay-attention-to-congestion-algorithms-on-your-linux-server-cf43999717cf#:~:text=TCP%20Cubic%3A%20The%20default%20congestion,growth%20in%20high%2Dbandwidth%20networks.
# Common Congestion Algorithms in Linux

Linux supports several congestion control algorithms, each with unique characteristics and use cases:
- **TCP Reno**: An older algorithm that uses a simple approach to congestion control with a **linear growth function**. It reduces the transmission rate when packet loss is detected, assuming it is due to congestion. [**[Ref]**](https://intronetworks.cs.luc.edu/current/html/reno.html)
- **TCP Cubic**: **The default congestion control algorithm in Linux** since kernel version **2.6.19**. It uses a **cubic function** to grow the congestion window size. This allows for more aggressive window growth in high-bandwidth networks. [**[Ref]**](https://en.wikipedia.org/wiki/CUBIC_TCP)
- **TCP BBR** (Bottleneck Bandwidth and Round-trip propagation time): A newer algorithm developed by Google that aims to maximize network throughput and minimize latency by estimating the available bandwidth and round-trip time. [**[Ref]**](https://cloud.google.com/blog/products/networking/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster)
- **TCP Vegas**: Focuses on packet delay, aiming to detect congestion before packet loss occurs by monitoring changes in round-trip time (RTT), thus maintaining a smooth flow of data. [**[Ref]**](https://en.wikipedia.org/wiki/TCP_Vegas)
- **TCP Westwood**: A sender-side modification of Reno that estimates the available bandwidth to set the window size after a loss. It improves performance over wireless links. [**[Ref]**](https://en.wikipedia.org/wiki/TCP_Westwood)
# Impact on Network Performance
  
  The choice of congestion algorithm can significantly affect network performance in various ways:
- **Throughput**: Algorithms like “**Cubic**” and “**BBR**” can achieve higher throughput compared to traditional algorithms like “**Reno**”, especially in high-bandwidth environments.
- **Latency**: Algorithms that react to delay, such as “**Vegas**”, can maintain lower latency, which is critical for applications like VoIP and online gaming.
- **Fairness**: Congestion control also ensures fair bandwidth distribution among users. Some algorithms prioritize fairness, while others focus on maximizing throughput. “**BBR**”, for instance, has been known to be more aggressive in certain scenarios, potentially leading to unfair bandwidth distribution.
- **Packet Loss Handling**: Algorithms differ in how they respond to packet loss. “**TCP Reno”**, for example, reduces its congestion window more drastically upon detecting loss compared to “**TCP Cubic”**, which can lead to lower performance on networks with occasional packet loss.
- **Network Type Adaptation**: Some algorithms are better suited for specific network conditions. “**TCP Westwood**”, for instance, performs well in wireless networks where packet loss may not always indicate congestion.
# How to Change Congestion Algorithms in Linux
  
  Linux allows users to change the congestion control algorithm to suit their needs. Here’s a simple guide:
- **Check available algorithms**:
  
  ```
  sysctl net.ipv4.tcp_available_congestion_control
  ```
  
  **2. Set a new algorithm**:
  
  To set a new algorithm, such as BBR, use the following command:
  
  ```
  sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
  ```
  
  **3. Verify the change**:
  
  Ensure the change was successful by checking the current algorithm:
  
  ```
  sysctl net.ipv4.tcp_congestion_control
  ```