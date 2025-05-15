#linux
### **1.1 Basic Steps**

1. **Check Local Hosts File (`/etc/hosts`)**
    
    Linux first checks the local `/etc/hosts` file for a manual mapping of the hostname to an IP address. If a match is found, it uses this entry and skips querying the DNS server.
    
2. **Query DNS Resolver**
    
    If the hostname is not found in `/etc/hosts`, Linux sends the query to the configured DNS resolver (usually specified in `/etc/resolv.conf`).
    
3. **Iterative or Recursive Query**
    
    The DNS resolver queries external DNS servers, using either iterative or recursive methods to resolve the domain name.
    
4. **Cache Results**
    
    The resolved IP address is cached by the system to speed up future queries.
    

---

## **2. Configuration Files Involved in DNS Resolution**

### **2.1 `/etc/hosts`**

- A static file for hostname-to-IP mapping.
    
- Priority is given to entries in this file over DNS queries.
    
- Example format:
    
    ```
    127.0.0.1   localhost
    192.168.1.10 myserver.example.com myserver
    
    ```
    

### **2.2 `/etc/resolv.conf`**

- Specifies the DNS servers to use for queries.
    
- Example:
    
    ```
    nameserver 8.8.8.8
    nameserver 8.8.4.4
    search example.com
    
    ```
    
    - `nameserver`: IP address of a DNS server.
    - `search`: Appends the domain to incomplete queries (e.g., `host` resolves as `host.example.com`).

### **2.3 `/etc/nsswitch.conf`**

- Determines the order of hostname resolution methods (e.g., local files, DNS, NIS).
- Example:

This configuration checks `/etc/hosts` first, then uses DNS.

````
```
hosts: files dns

```
````

---

## **3. DNS Resolver Libraries**

### **3.1 glibc Resolver**

- Linux applications typically use the **glibc** library to perform DNS queries.
- The `getaddrinfo()` function abstracts the DNS lookup process, adhering to the configuration in `/etc/nsswitch.conf`.

### **3.2 `libresolv`**

- Part of the standard library providing low-level functions for DNS lookups, like `res_query()`.

---

## **4. DNS Caching**

### **4.1 Client-Side Caching**

- Linux does not natively cache DNS queries at the kernel level.
- Applications like **`systemd-resolved`**, **dnsmasq**, or third-party tools (e.g., **nscd** or **unbound**) are used for caching.

### **4.2 DNS Cache Benefits**

- Reduces latency by avoiding repeated queries.
- Minimizes DNS server load.

---

## **5. DNS Query Tools**

Linux provides several command-line tools to test and troubleshoot DNS:

### **5.1 `nslookup`**

- Performs DNS queries.
    
- Example:
    
    ```bash
    nslookup example.com
    
    ```
    

### **5.2 `dig`**

- A powerful tool for querying DNS information.
    
- Example:
    
    ```bash
    dig example.com
    
    ```
    

### **5.3 `host`**

- Resolves hostnames and IPs.
    
- Example:
    
    ```bash
    host example.com
    
    ```
    

---

## **6. DNS in Systemd**

In systems using **systemd-resolved**, DNS handling integrates into the system management infrastructure:

### **6.1 Configuration**

- The resolver configuration can be found in `/etc/systemd/resolved.conf`.
    
- Example:
    
    ```
    [Resolve]
    DNS=8.8.8.8 8.8.4.4
    FallbackDNS=1.1.1.1
    
    ```
    

### **6.2 DNS Stub Resolver**

- Applications query the stub resolver at `127.0.0.53`, which then forwards queries to the configured DNS servers.

### **6.3 Interaction with `resolv.conf`**

- **systemd-resolved** may manage `/etc/resolv.conf`, symlinking it to `/run/systemd/resolve/resolv.conf`.

---

## **7. Troubleshooting DNS in Linux**

### **7.1 Common Issues**

- Incorrect DNS server configuration in `/etc/resolv.conf`.
- Network connectivity issues.
- Application misconfiguration.

### **7.2 Diagnostic Steps**

1. **Check DNS Configuration**
    
    ```bash
    cat /etc/resolv.conf
    
    ```
    
2. **Test Network Connectivity**
    
    ```bash
    ping 8.8.8.8
    
    ```
    
3. **Query DNS Servers Directly**
    
    ```bash
    dig @8.8.8.8 example.com
    
    ```
    
4. **Flush DNS Cache** If using a caching service like `systemd-resolved`:
    
    ```bash
    systemctl restart systemd-resolved
    
    ```
    

---

## **8. Advanced Features**

### **8.1 DNS over TLS/HTTPS**

- Linux can use secure DNS protocols via tools like **systemd-resolved** or third-party resolvers (e.g., Cloudflare's `cloudflared`).

### **8.2 Split DNS**

- Configurations that route DNS queries differently based on network conditions, often used in VPNs.

### **8.3 BIND and Custom DNS Servers**

- Linux can host a DNS server using **BIND** or similar tools for advanced DNS management and local caching.

---

Linux’s DNS handling is modular and flexible, allowing it to adapt to various network configurations and application requirements. From simple hostname lookups to advanced DNS configurations, Linux provides the tools and infrastructure to handle DNS efficiently.