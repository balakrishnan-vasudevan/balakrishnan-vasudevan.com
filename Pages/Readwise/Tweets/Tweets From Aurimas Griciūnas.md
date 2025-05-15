# Tweets From Aurimas Griciūnas

![rw-book-cover](https://pbs.twimg.com/profile_images/1725897062296772608/pkRjNV01.jpg)

## Metadata
- Author: [[@Aurimas_Gr on Twitter]]
- Full Title: Tweets From Aurimas Griciūnas
- Category: #tweets
- URL: https://twitter.com/Aurimas_Gr

## Highlights
- Refresher on 𝗥𝗲𝗮𝗱𝗶𝗻𝗴 𝗗𝗮𝘁𝗮 from 𝗞𝗮𝗳𝗸𝗮.
  𝗥𝗲𝗺𝗶𝗻𝗱𝗲𝗿:
  ➡️ Clients writing to Kafka are called 𝗣𝗿𝗼𝗱𝘂𝗰𝗲𝗿𝘀.
  ➡️ Clients reading the Data are called 𝗖𝗼𝗻𝘀𝘂𝗺𝗲𝗿𝘀.
  ➡️ Data is written into 𝗧𝗼𝗽𝗶𝗰𝘀 that can be compared to tables in Databases.
  ➡️ Messages sent to 𝗧𝗼𝗽𝗶𝗰𝘀 are called 𝗥𝗲𝗰𝗼𝗿𝗱𝘀.
  ➡️ 𝗧𝗼𝗽𝗶𝗰𝘀 are composed of 𝗣𝗮𝗿𝘁𝗶𝘁𝗶𝗼𝗻𝘀.
  ➡️ Each 𝗣𝗮𝗿𝘁𝗶𝘁𝗶𝗼𝗻 is a combination of and behaves as a write ahead log.
  ➡️ Data is written to the end of the 𝗣𝗮𝗿𝘁𝗶𝘁𝗶𝗼𝗻.
  ➡️ Each 𝗥𝗲𝗰𝗼𝗿𝗱 has an 𝗢𝗳𝗳𝘀𝗲𝘁 assigned to it which denotes its order in the 𝗣𝗮𝗿𝘁𝗶𝘁𝗶𝗼𝗻.
  ➡️ 𝗢𝗳𝗳𝘀𝗲𝘁𝘀 start at 0 and increment by 1 sequentially.
  𝗥𝗲𝗮𝗱𝗶𝗻𝗴 𝗗𝗮𝘁𝗮:
  ➡️ Data is read sequentially per partition.
  ➡️ 𝗜𝗻𝗶𝘁𝗶𝗮𝗹 𝗥𝗲𝗮𝗱 𝗣𝗼𝘀𝗶𝘁𝗶𝗼𝗻 can be set either to earliest or latest.
  ➡️ Earliest position initiates the consumer at offset 0 or the earliest available due to retention rules of the 𝗧𝗼𝗽𝗶𝗰 (more about this in later episodes).
  ➡️ Latest position initiates the consumer at the end of a 𝗣𝗮𝗿𝘁𝗶𝘁𝗶𝗼𝗻 - no 𝗥𝗲𝗰𝗼𝗿𝗱𝘀 will be read initially and the 𝗖𝗼𝗻𝘀𝘂𝗺𝗲𝗿 will wait for new data to be written.
  ➡️ You could codify your consumers independently, but almost always the preferred way is to use 𝗖𝗼𝗻𝘀𝘂𝗺𝗲𝗿 𝗚𝗿𝗼𝘂𝗽𝘀.
  𝗖𝗼𝗻𝘀𝘂𝗺𝗲𝗿 𝗚𝗿𝗼𝘂𝗽𝘀:
  ➡️ 𝗖𝗼𝗻𝘀𝘂𝗺𝗲𝗿 𝗚𝗿𝗼𝘂𝗽 is a logical collection of clients that read a Kafka Topic and share the state.
  ➡️ Groups of consumers are identified by the 𝗴𝗿𝗼𝘂𝗽_𝗶𝗱 parameter.
  ➡️ 𝗦𝘁𝗮𝘁𝗲 is defined by the offsets that every Partition in the Topic is being consumed at.
  ➡️ State of Consumer Groups is written by the Broker (more about this in later episodes) to an internal Kafka Topic named __𝗰𝗼𝗻𝘀𝘂𝗺𝗲𝗿_𝗼𝗳𝗳𝘀𝗲𝘁𝘀.
  ➡️ There can be multiple Consumer Groups reading the same Kafka Topic having their own independent States.
  ➡️ Only one Consumer per Consumer Group can be reading a Partition at a single point in time.
  𝗖𝗼𝗻𝘀𝘂𝗺𝗲𝗿 𝗚𝗿𝗼𝘂𝗽 𝗧𝗶𝗽𝘀:
  ❗️ If you have a Prime number of Partitions in the Topic  - you will always have at least one Consumer per Consumer Group consuming less Partitions than others unless number of Consumers equals number of Partitions.
  ✅ If you want an odd number of Partitions - set it to a 𝗺𝘂𝗹𝘁𝗶𝗽𝗹𝗲 𝗼𝗳 𝗣𝗿𝗶𝗺𝗲 𝗡𝘂𝗺𝗯𝗲𝗿.
  ❗️ If you have more Consumers in the Consumer Group then there are Partitions in the Topic - some of the Consumers will be Idle.
  ✅ Make your Topics large enough or have less Consumers per Consumer Group.
  --------
  Follow me to upskill in #MLOps, #MachineLearning, #DataEngineering, #DataScience and overall #Data space.
  Also hit 🔔to stay notified about new content.
  𝗗𝗼𝗻’𝘁 𝗳𝗼𝗿𝗴𝗲𝘁 𝘁𝗼 𝗹𝗶𝗸𝗲 💙, 𝘀𝗵𝗮𝗿𝗲 𝗮𝗻𝗱 𝗰𝗼𝗺𝗺𝗲𝗻𝘁!
  Join a growing community of Data Professionals by subscribing to my 𝗡𝗲𝘄𝘀𝗹𝗲𝘁𝘁𝗲𝗿: https://t.co/qgNCnGtF4A ([View Tweet](https://twitter.com/Aurimas_Gr/status/1680580446533439496))
