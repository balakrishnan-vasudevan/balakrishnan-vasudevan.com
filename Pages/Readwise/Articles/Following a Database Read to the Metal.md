# Following a Database Read to the Metal

![rw-book-cover](https://readwise-assets.s3.amazonaws.com/static/images/article3.5c705a01b476.png)

## Metadata
- Author: [[Hussein Nasser]]
- Full Title: Following a Database Read to the Metal
- Category: #articles
- URL: https://medium.com/p/a187541333c2

## Highlights
- There is a database page, an operating system virtual memory page, a file system block, an SSD page, two types of SSD blocks, one called the logical block that maps to the file system and one is the larger unit that is called erase unit which contains multiple pages. All of these units can have different sizes, some match some don’t.
- When you create a table in a database, a file is created on disk and the data are layout out into a fixed-sized database pages. How the data is laid out in the page depends on whether the engine is row-store or column-store. Think of a page as a structure which has a header and data, the data portion is where the rows live.
