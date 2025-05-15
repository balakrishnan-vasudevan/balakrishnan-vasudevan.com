# Content Drive — How we organize and share billions of files in Netflix studio

Tags: metadata-storage, storage
Category: Articles
Company: Netflix
Status: Not started
URL: https://netflixtechblog.medium.com/content-drive-919938544e4b

Starting at the point of ingestion where data is produced out of the camera, it goes through many stages, some of which are shown below. The media undergoes comprehensive backup routines at every stage and phase of this process with frequent uploads and downloads. In order to support these processes and studio applications, we need to provide a distributed, scalable, and performant media cloud storage infrastructure.

![image.png](image.png)

all these media files are securely delivered and stored within Amazon Simple Storage Service (S3) . Netflix maintains an identity of all these objects to be addressed by storage infrastructure layers along with other essential metadata about these objects.

They needed a system that could provide the ability to store, manage, and track billions of these media objects while keeping a familiar file/folder interface that lets users upload freeform files and provide management capabilities such as create, update, move, copy, delete, download, share, and fetch arbitrary tree structures.

**highly scalable metadata storage service — *Content Drive -***  Content Drive (or CDrive) is a cloud storage solution that provides file/folder interfaces for storing, managing, and accessing the directory structure of Netflix’s media assets in a scalable and secure way. It empowers applications such as Content Hub UI to import media content (upload to S3), manage its metadata, apply lifecycle policies, and provide access control for content sharing.

What can it do?

- Storing, managing and tracking billions of files and folders while retaining folder structure. Provide a familiar Google Drive-like interface which lets users upload freeform files and provide management capabilities such as create, update, move, copy, delete, download, share, and fetch arbitrary tree structures.
- Provide access control for viewing, uploads and downloads of files and folders.
- Collaboration/Sharing — share work-in-progress files.
- Data transfer manifest and token generation — Generate download manifest and tokens for requested files/folders after verifying authorization.
- Files/folders notifications — Provide change notifications for files/folders. This enables live sharing and collaboration use cases in addition to supporting dependent backend applications to complete their business workflows around data ingestion.

Architecture:

![image.png](image%201.png)

- REST API and DGS (GraphQL) layer that provides endpoints to create/manage files/folders, manage shares for files/folders, and get authorization tokens for files/folders upload/download.
- CDrive service layer that does the actual work of creating and managing tree structure (implements operations such as create, update, copy, move, rename, delete, checksum validation, etc on files/folder structures).
- Access control layer that provides user and application-based authorization for files/folders managed in CDrive.
- Data Transfer layer that proxies requests to other services for transfer tracking and transfer token generation after authorization.
- Persistence layer that performs the metadata reads and updates in transactions for files/folders managed in CDrive.
- Event Handler that produces event notifications for users and applications to consume and take action. For example, CDrive generates an event on upload completion for a folder.