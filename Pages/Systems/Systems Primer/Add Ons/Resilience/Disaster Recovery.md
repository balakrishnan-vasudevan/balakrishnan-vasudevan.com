This is from AWS

**Table of Contents**

- [Backup and Restore](#Backup%20and%20Restore)
- [Pilot Light](#Pilot%20Light)
- [Warm Standby](#Warm%20Standby)
- [Multi-site active/active](#Multi-site%20active/active)


![Graph showing disaster recovery strategies and highlights of each strategy.](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/disaster-recovery-strategies.png)

_Figure 6 - Disaster recovery strategies_

# Backup and Restore

![Architecture diagram showing backup and restore architecture](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/backup-restore-architecture.png)

_Figure 7 - Backup and restore architecture_
Backup with point-in-time recovery is available through the following services and resources:

- [Amazon Elastic Block Store (Amazon EBS) snapshot](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html)
- [Amazon DynamoDB backup](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery.html)
- [Amazon RDS snapshot](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html)
- [Amazon Aurora DB snapshot](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_CreateSnapshotCluster.html)
- [Amazon EFS backup](https://docs.aws.amazon.com/efs/latest/ug/awsbackup.html) (when using AWS Backup)
- [Amazon Redshift snapshot](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-snapshots.html) 
- [Amazon Neptune snapshot](https://docs.aws.amazon.com/neptune/latest/userguide/backup-restore-overview.html)
- [Amazon DocumentDB](https://docs.aws.amazon.com/documentdb/latest/developerguide/backup_restore.html)
- [Amazon FSx for Windows File Server](https://docs.aws.amazon.com/fsx/latest/WindowsGuide/using-backups.html), [Amazon FSx for Lustre](https://docs.aws.amazon.com/fsx/latest/LustreGuide/using-backups-fsx.html), [Amazon FSx for NetApp ONTAP](https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/using-backups.html), and [Amazon FSx for OpenZFS](https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/using-backups.html)


![Diagram showing workflow of restoring and testing backups.](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/restore-test-backups.png)

_Figure 8 - Restoring and testing backups_

# Pilot Light

With the _pilot light_ approach, you replicate your data from one Region to another and provision a copy of your core workload infrastructure. Resources required to support data replication and backup, such as databases and object storage, are always on. Other elements, such as application servers, are loaded with application code and configurations, but are "switched off" and are only used during testing or when disaster recovery failover is invoked. In the cloud, you have the flexibility to deprovision resources when you do not need them, and provision them when you do. A best practice for “switched off” is to not deploy the resource, and then create the configuration and capabilities to deploy it (“switch on”) when needed. Unlike the backup and restore approach, your core infrastructure is always available and you always have the option to quickly provision a full scale production environment by switching on and scaling out your application servers.

![Reference architecture diagram for pilot light architecture](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/pilot-light-architecture.png)

_Figure 9 - Pilot light architecture_

For pilot light, continuous data replication to live databases and data stores in the DR region is the best approach for low RPO (when used in addition to the point-in-time backups discussed previously). AWS provides continuous, cross-region, asynchronous data replication for data using the following services and resources:

- [Amazon Simple Storage Service (Amazon S3) Replication](http://aws.amazon.com/s3/features/replication/)
- [Amazon RDS read replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html#USER_ReadRepl.XRgn.Cnsdr)
- [Amazon Aurora global databases](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html)
- [Amazon DynamoDB global tables](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html)
- [Amazon DocumentDB global clusters](https://docs.aws.amazon.com/documentdb/latest/developerguide/global-clusters.html)
- [Global Datastore for Amazon ElastiCache for Redis](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Redis-Global-Datastore.html)
    
With continuous replication, versions of your data are available almost immediately in your DR Region. Actual replication times can be monitored using service features like [S3 Replication Time Control (S3 RTC)](https://docs.aws.amazon.com/AmazonS3/latest/dev/replication-time-control.html) for S3 objects and [management features of Amazon Aurora global databases](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database-managing.html).

### AWS Elastic Disaster Recovery

[AWS Elastic Disaster Recovery](http://aws.amazon.com/disaster-recovery/) (DRS) continuously replicates server-hosted applications and server- hosted databases from any source into AWS using block-level replication of the underlying server. Elastic Disaster Recovery enables you to use a Region in AWS Cloud as a disaster recovery target for a workload hosted on-premises or on another cloud provider, and its environment. It can also be used for disaster recovery of AWS hosted workloads if they consist only of applications and databases hosted on EC2 (that is, not RDS). Elastic Disaster Recovery uses the Pilot Light strategy, maintaining a copy of data and “switched-off” resources in an [Amazon Virtual Private Cloud (Amazon VPC)](http://aws.amazon.com/vpc/) used as a staging area. When a failover event is triggered, the staged resources are used to automatically create a full-capacity deployment in the target Amazon VPC used as the recovery location.

![Architecture diagram showing AWS Elastic Disaster Recovery architecture.](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/disaster-recovery-architecture.png)

_Figure 10 - AWS Elastic Disaster Recovery architecture_

# Warm Standby
The _warm standby_ approach involves ensuring that there is a scaled down, but fully functional, copy of your production environment in another Region. This approach extends the pilot light concept and decreases the time to recovery because your workload is always-on in another Region. This approach also allows you to more easily perform testing or implement continuous testing to increase confidence in your ability to recover from a disaster.

![Architecture diagram showing warm standby architecture.](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/warm-standby-architecture.png)

_Figure 11 - Warm standby architecture_

# Multi-site active/active

You can run your workload simultaneously in multiple Regions as part of a _multi-site active/active_ or _hot standby active/passive_ strategy. Multi-site active/active serves traffic from all regions to which it is deployed, whereas hot standby serves traffic only from a single region, and the other Region(s) are only used for disaster recovery. With a multi-site active/active approach, users are able to access your workload in any of the Regions in which it is deployed. This approach is the most complex and costly approach to disaster recovery, but it can reduce your recovery time to near zero for most disasters with the correct technology choices and implementation (however data corruption may need to rely on backups, which usually results in a non-zero recovery point). Hot standby uses an active/passive configuration where users are only directed to a single region and DR regions do not take traffic. Most customers find that if they are going to stand up a full environment in the second Region, it makes sense to use it active/active. Alternatively, if you do not want to use both Regions to handle user traffic, then Warm Standby offers a more economical and operationally less complex approach.

![[Pasted image 20231218074102.png]]


With multi-site active/active, because the workload is running in more than one Region, there is no such thing as failover in this scenario. Disaster recovery testing in this case would focus on how the workload reacts to loss of a Region: Is traffic routed away from the failed Region? Can the other Region(s) handle all the traffic? Testing for a data disaster is also required. Backup and recovery are still required and should be tested regularly. It should also be noted that recovery times for a data disaster involving data corruption, deletion, or obfuscation will always be greater than zero and the recovery point will always be at some point before the disaster was discovered. If the additional complexity and cost of a multi-site active/active (or hot standby) approach is required to maintain near zero recovery times, then additional efforts should be made to maintain security and to prevent human error to mitigate against human disasters.