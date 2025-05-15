#scaling 
Source: https://www.levels.fyi/blog/scaling-to-millions-with-google-sheets.html?

Initial iteration of site did not have a backend.

The backend is responsible for processing, storing & delivering the dynamic content. If we take the backend for any site out of the equation then it’s mainly a static site.

Building a static site is not super challenging because you don’t have to think about maintaining a server for APIs and a database for data storage.

To build a static site you only need the left part and a dynamic site requires both.

![https://www.levels.fyi/blog/img/post_images/scaling-to-millions-with-google-sheets/Untitled.png](https://www.levels.fyi/blog/img/post_images/scaling-to-millions-with-google-sheets/Untitled.png)

The user interface can be replaced by Google Forms. The database can be replaced by Google Sheets. And the API server can be replaced by AWS API Gateway + AWS Lambda.

Google Forms, Google Sheets & API Gateway are _no-code_ tools and they require zero amount of operational maintenance. It’s Google’s & AWS’s job to keep them up and running 24x7.

Progression:
![[Pasted image 20231110103015.png]]
![[Pasted image 20231110103039.png]]
Read flow:
![[Pasted image 20231110103100.png]]
1. Process data from Google Sheet and create a JSON file
2. Use AWS Lambda for processing and creating new JSON files
3. Upsert JSON files on S3
4. Cache JSON files using a CDN like AWS Cloudfront

Caching strategy
![[Pasted image 20231110103115.png]]
Issues/Drawbacks:

1. The size of json files grew to several **MBs**, every cache miss was a massive penalty for the user and also for the initial page load time
2. Our lambda functions started timing out due to the amount of data that needed to be processed in a single instance of execution
3. We lacked any SQL based data analysis which became problematic to make data driven decisions
4. Google Sheets API rate limiting is pretty strict for write paths. Our writes were scaling past those limits
5. Since our data was downloaded as json files it was easy to scrape and plagiarise

Migration:

1. Get rid of all JSON files
2. Use APIs for all read/write paths

Started splitting JSON files into smaller chunks and deprecating each chunk by a new read API

![4F2272E1-A097-4253-B0DB-C2B442BF7B00.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/34ffa87a-1487-49a6-8c3b-29248d546897/4F2272E1-A097-4253-B0DB-C2B442BF7B00.png)

Move all read/write paths to the API

![C538418B-F3B2-41EE-9586-122B5E0F6C15.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/28129cb6-52ed-4c61-a4e4-d73c4ca80a33/C538418B-F3B2-41EE-9586-122B5E0F6C15.png)

Our backend today is more sophisticated but our philosophy to scaling is simple, **avoiding premature optimization**

Even now, one of our most trafficked services today still has a single node.js instance serving **60K requests per hour**