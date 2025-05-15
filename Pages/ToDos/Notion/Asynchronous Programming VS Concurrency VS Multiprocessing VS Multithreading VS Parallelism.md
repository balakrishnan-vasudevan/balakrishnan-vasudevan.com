- Tags: #programming
  Category: Articles
  Company: general
  Status: Not started
  URL: https://levelup.gitconnected.com/asynchronous-programming-vs-concurrency-vs-multiprocessing-vs-multithreading-aae5a383da30
- ## Async
- ***Definition***: Asynchronous programming allows tasks to execute without waiting for previous tasks to complete, enabling a program to continue with other work while waiting for tasks to finish.
- ***How it Works***: Often uses a single thread and an **event loop** to manage tasks. Functions are scheduled, and the program “awaits” certain tasks without blocking other operations.
- ***Use Cases***: Networking (e.g., web requests), file I/O, and any task that involves waiting for an external resource.
- ***Example Libraries***: `asyncio `and `async/await` in Python, JavaScript’s `async/await` syntax.
- ```import asyncio
  import aiohttp
  
  async def fetch_data(url):
      async with aiohttp.ClientSession() as session:
          async with session.get(url) as response:
              return await response.text()
  
  async def main():
      print("Fetching data...")
      data = await fetch_data("https://jsonplaceholder.typicode.com/todos/1")
      print("Data fetched:", data)
  
  asyncio.run(main())
  ```
-
-