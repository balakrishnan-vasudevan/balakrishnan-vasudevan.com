#linux

Linux handles networking using a combination of kernel modules, networking protocols, and user-space tools. The process involves receiving, routing, processing, and transmitting packets. This involves the **network stack**, which is layered, modular, and closely follows the OSI and TCP/IP models.

---

### **1. Overview of Linux Networking Stack**

The Linux networking stack comprises the following layers:

1. **Physical Layer:** Involves hardware components like network interfaces (NICs).
2. **Data Link Layer:** Uses drivers and protocols like Ethernet.
3. **Network Layer:** Handles IP addressing and routing (IPv4, IPv6).
4. **Transport Layer:** Provides communication services (TCP, UDP).
5. **Application Layer:** Hosts user-level programs that use sockets (e.g., HTTP, SSH).

Incoming and outgoing packets flow through these layers, with kernel mechanisms ensuring efficient handling.

---

### **2. Handling Incoming Packets**

### **2.1 Packet Reception**

1. **Interrupts and NIC Buffers:**
    - The Network Interface Card (NIC) receives packets and stores them in a **receive buffer**.
    - The NIC signals the CPU via an **interrupt** to notify about incoming packets.
2. **Driver Processing:**
    - The NIC driver transfers packets from the hardware buffer to a **sk_buff** structure in kernel space.
    - The sk_buff is a key data structure that holds metadata and the actual packet data.
3. **Netfilter Hook for Pre-Routing:**
    - The packet passes through the **Netfilter framework**, allowing firewall rules, NAT, or packet filtering to be applied.

### **2.2 Network Layer Processing**

1. **IP Processing:**
    - If the packet is an IP packet (IPv4 or IPv6):
        - The kernel checks its header for errors (checksum verification).
        - It determines the destination by examining the IP address.
    - For local delivery: The packet is passed to the transport layer.
    - For forwarding: The packet is routed to another NIC.
2. **Routing Decision:**
    - The kernel consults the **routing table** to decide the next action.
    - Local packets are flagged for higher-layer processing; others are forwarded.

### **2.3 Transport Layer Processing**

1. **Protocol Demultiplexing:**
    - The kernel identifies the transport protocol (TCP, UDP, ICMP, etc.) using the IP header.
2. **TCP/UDP Processing:**
    - TCP: The kernel processes sequence numbers, acknowledges data, and manages retransmissions.
    - UDP: The kernel processes datagrams without maintaining a connection state.
3. **Socket Layer:**
    - Packets are delivered to the appropriate socket associated with a user-space application.

### **2.4 User-Space Delivery**

1. **Copy to User Space:**
    - The kernel copies packet data to user-space memory using system calls like `recv()` or `read()`.

---

### **3. Handling Outgoing Packets**

### **3.1 Application Layer**

1. **Socket API:**
    - User applications send data using socket APIs (e.g., `send()`, `write()`).
    - The data is passed to the kernel for processing.

### **3.2 Transport Layer**

1. **Protocol Handling:**
    - TCP: The kernel segments data, assigns sequence numbers, and maintains a connection state.
    - UDP: The kernel packages the data into a datagram.
2. **Checksum Calculation:**
    - Transport and network headers include checksums for integrity verification, calculated by the kernel.

### **3.3 Network Layer**

1. **IP Packet Creation:**
    - The kernel encapsulates the transport-layer payload into an IP packet.
    - The IP header includes the source and destination IP addresses, TTL, and other metadata.
2. **Routing Decision:**
    - The kernel consults the routing table to determine the appropriate NIC for packet transmission.

### **3.4 Data Link Layer**

1. **ARP and Neighbor Discovery:**
    - If the destination is within the same subnet:
        - IPv4: The Address Resolution Protocol (ARP) resolves the destination MAC address.
        - IPv6: Neighbor Discovery Protocol (NDP) performs this function.
    - For remote destinations, the packet is routed to the gateway.
2. **Frame Encapsulation:**
    - The kernel wraps the IP packet in a data-link-layer frame (e.g., Ethernet frame) with source and destination MAC addresses.

### **3.5 NIC Transmission**

1. **Packet Transmission:**
    - The kernel sends the frame to the NIC driver.
    - The NIC queues the frame in its transmit buffer and sends it over the physical network.

---

### **4. Kernel Components in Networking**

### **4.1 Netfilter Framework**

- Hooks into the networking stack to allow inspection and modification of packets.
- Commonly used for:
    - Firewall rules (iptables/nftables).
    - NAT (Network Address Translation).

### **4.2 Traffic Control (tc)**

- Manages packet queuing, shaping, and policing.
- Ensures Quality of Service (QoS).

### **4.3 Routing Subsystem**

- Maintains and consults routing tables.
- Supports static routes, dynamic routing protocols (via tools like `quagga` or `bird`), and policy routing.

---

### **5. Key Features of Linux Networking**

### **5.1 Virtual Network Interfaces**

- Loopback (`lo`): Local traffic testing.
- TUN/TAP: For virtual networking (e.g., VPNs).
- Bridge: For connecting multiple interfaces.

### **5.2 Kernel Network Namespaces**

- Isolate networking resources for containers or virtualized environments.

### **5.3 Network Performance Enhancements**

- **SoftIRQ:** Handles high-throughput packet processing efficiently.
- **Receive Side Scaling (RSS):** Distributes incoming traffic across multiple CPUs.
- **TCP Segmentation Offload (TSO) and Large Receive Offload (LRO):** Offloads processing to NICs.

### **5.4 Networking Tools**

- `ip` (from iproute2): Manages interfaces, routing, and tunnels.
- `ethtool`: Configures NICs.
- `tcpdump`: Captures and analyzes packets.
- `nftables/iptables`: Configures firewalls.

---

### **6. Summary of Packet Flow**

### **Incoming Packets**

1. NIC → Driver → sk_buff → Netfilter (PREROUTING) → IP stack.
2. Local packets → Transport layer (TCP/UDP) → Application via socket.

### **Outgoing Packets**

1. Application → Socket → Transport layer → Network layer.
2. IP stack → Routing → ARP/NDP → Driver → NIC.

This layered, modular approach allows Linux to efficiently handle complex networking scenarios and adapt to various hardware and software environments.

https://www.cs.dartmouth.edu/~sergey/netreads/path-of-packet/Lab9_modified.pdf
http://beyond-syntax.com/blog/2011/03/diving-into-linux-networking-i/
https://maxnilz.com/docs/004-network/006-linux-tx/
[[Network queues and optimization]]