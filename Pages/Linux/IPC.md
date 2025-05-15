#linux
Linux's **Interprocess Communication (IPC)** mechanisms allow processes to communicate and synchronize with each other. These are critical for processes to share data, signal events, and coordinate actions. Below is a detailed breakdown of IPC, with a focus on **pipes**, a widely used IPC mechanism in Linux.

---

## **1. Overview of Interprocess Communication (IPC)**

IPC in Linux facilitates:

- **Data sharing**: Processes exchange data without sharing the same address space.
- **Synchronization**: Processes coordinate their execution using signals or shared states.
- **Performance**: Efficient IPC mechanisms reduce overhead and improve responsiveness.

IPC mechanisms in Linux include:

1. **Pipes** (named and unnamed)
2. **Signals**
3. **Message Queues**
4. **Shared Memory**
5. **Semaphores**
6. **Sockets**

---

## **2. Pipes in Linux**

### **2.1 What is a Pipe?**

A **pipe** is a unidirectional data channel used for communication between processes. It is one of the simplest and oldest IPC mechanisms in Linux, enabling one process to write data into the pipe and another to read from it.

### **2.2 Characteristics of Pipes**

- **Unidirectional**: Data flows in a single direction (from writer to reader).
- **Buffer-based**: Pipes use an internal buffer to temporarily hold data.
- **Parent-child communication**: Pipes are often used between processes with a parent-child relationship.
- **Blocking behavior**:
    - A read operation blocks until data is available.
    - A write operation blocks if the pipe’s buffer is full.

---

### **2.3 Types of Pipes**

### **2.3.1 Unnamed Pipes**

- Created with the `pipe()` system call.
- Exist only as long as the processes using them are running.
- Used for communication between related processes (e.g., parent and child).

**Example: Creating an unnamed pipe**

```c
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main() {
    int pipefds[2];
    char write_msg[] = "Hello, pipe!";
    char read_msg[20];

    if (pipe(pipefds) == -1) {
        perror("pipe");
        return 1;
    }

    // Write to pipe
    write(pipefds[1], write_msg, strlen(write_msg) + 1);

    // Read from pipe
    read(pipefds[0], read_msg, sizeof(read_msg));
    printf("Received: %s\\n", read_msg);

    return 0;
}

```

**Explanation:**

- `pipefds[0]`: File descriptor for reading.
- `pipefds[1]`: File descriptor for writing.

---

### **2.3.2 Named Pipes (FIFO)**

- Created using the `mkfifo` command or `mkfifo()` system call.
- Persist in the filesystem as special files.
- Allow communication between unrelated processes.

**Creating and using a named pipe:**

```bash
# Create a named pipe
mkfifo myfifo

# Write data to the pipe in one terminal
echo "Hello from writer" > myfifo

# Read data from the pipe in another terminal
cat myfifo

```

**Key Characteristics of Named Pipes:**

- Persistent until explicitly deleted.
- Identified by a file path.
- Can be used between processes that do not share a parent-child relationship.

---

### **2.4 Pipe Buffering**

Pipes use a buffer for intermediate storage. If:

- The buffer is **full**, the writer process blocks until space becomes available.
- The buffer is **empty**, the reader process blocks until data is written.

The default pipe buffer size is system-dependent and can be queried/modified using `ulimit` or system calls.

---

### **2.5 Limitations of Pipes**

- **Unidirectional**: Data flows in only one direction.
- **Limited scope**:
    - Unnamed pipes work only between related processes.
    - Named pipes are less performant for high-frequency communication.
- **No random access**: Data is read in the order it is written (FIFO - First In, First Out).
- **Fixed buffer size**: Excessive writes may block processes.

---

## **3. Other IPC Mechanisms in Linux**

### **3.1 Signals**

- Used for asynchronous notifications (e.g., `SIGKILL`, `SIGUSR1`).
- Lightweight and fast, but limited in data-passing capability.

### **3.2 Message Queues**

- Allow messages to be sent between processes.
- Provide message prioritization and non-blocking reads.
- System calls: `msgget()`, `msgsnd()`, `msgrcv()`.

### **3.3 Shared Memory**

- Fastest IPC mechanism as it allows direct memory access.
- Processes share a memory region and synchronize via semaphores or mutexes.
- System calls: `shmget()`, `shmat()`, `shmdt()`.

### **3.4 Semaphores**

- Used to synchronize processes.
- Prevents race conditions by ensuring mutual exclusion.
- System calls: `semget()`, `semop()`, `semctl()`.

### **3.5 Sockets**

- Used for communication between processes on the same or different machines.
- Support both TCP/IP and UNIX domain sockets.

---

## **4. Practical Use Cases of Pipes**

### **4.1 Pipelining in Shell**

Pipes are heavily used in shell scripting to pass the output of one command as input to another:

```bash
ls | grep ".txt" | wc -l

```

- `ls`: Lists files.
- `grep ".txt"`: Filters `.txt` files.
- `wc -l`: Counts the number of lines.

### **4.2 Logging and Monitoring**

Processes can write logs to a pipe, and another process can read and process those logs in real time.

### **4.3 Data Streaming**

Pipes are ideal for streaming data between producer and consumer processes without requiring intermediate files.

---

## **5. Pipes vs. Other IPC Mechanisms**

|Feature|Unnamed Pipes|Named Pipes (FIFO)|Shared Memory|Message Queues|Sockets|
|---|---|---|---|---|---|
|**Directionality**|Unidirectional|Unidirectional|Bidirectional|Bidirectional|Bidirectional|
|**Relatedness**|Parent-child only|Unrelated processes|Any|Any|Any|
|**Persistence**|Ephemeral|Persistent|Persistent|Persistent|Persistent|
|**Performance**|Moderate|Moderate|High|High|Moderate|

---

Linux's IPC mechanisms, particularly pipes, offer versatile and efficient solutions for interprocess communication, tailored to the specific needs of different applications and environments.

[[Signals and Signal Handlers]]