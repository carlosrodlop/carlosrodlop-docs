# AWS Solution Architect

![badge](https://images.credly.com/size/340x340/images/0e284c3f-5164-4b21-8660-0d84737941bc/image.png)

## Index

1. [Global](#global)
2. [Security](#security)
3. [Compute](#compute)
4. [Containers](#containers)
5. [Application Integration](#application_integration)
6. [Storage](#storage)
7. [Database](#database)
8. [Migration](#migration)
9. [Networking](#networking)
10. [Management_and_Governance](#management_and_governance)
11. [References](#references)

## Global

Go to [Index](#index)

### [Global Infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/)

- In June 2023
  - [31 Regions with 99 Availability Zones](http://clusterfrak.com/notes/certs/aws_saa_notes/#security-and-identity).
  - +400 Edge locations are CDN endpoints for CloudFront. 13 Regional Edge Caches.

#### AWS Region

- AWS regions are physical locations around the world having cluster of data centers
- For Regional AWS Services (EC2, ELB, S3, Lambda, etc.), the region needs to be selected before its creation.
- You can **not select region for Global AWS services** such as IAM, AWS Organizations, Route 53, CloudFront, WAF, etc.

Exam Tip: Multi-Region Architecture => Disaster Recovery

#### AWS AZ (Availability zones)

- Each AWS Region consists of multiple, isolated, and physically separate AZs (Availability Zones) within a geographic area.
- An AZ is one or more discrete data centers with redundant power, networking, and connectivity
- All AZs in an AWS Region are interconnected with high-bandwidth, **low-latency networking**.
- AZs in a region are usually 3, min is 2 and max is 6 for e.g. 3 AZs in Ohio are us-east-2a, us-east-2b, and us-east-2c.

Exam Tip: Multi-Az Architecture => HA & Fault Tolerant

### Tags

- Key/Value pairs attached to AWS resources with Metadata (data about data)
- Sometimes can be inherited (Auto-scaling, CloudFormation, Elastic Beanstalk can create other resources)
- `Resource Groups` make it easy to group your resources using the tags that are assigned to them
  - You can group resources that share one or more tags
  - Resource groups contain info such as region, name, health checks

### Amazon Resource Name (ARN)

- Identifier (ID) for any AWS resource. They are globally unique
- begin with `arn:<partition>:<service>:<region>:<account_id>` and end with: `resource`
  `resource_type/resource`, `resource_type/resource/qualifier`, `resource_type/resource:qualifier`, `resource_type:resource` and `resource_type:resource:qualifier`
- Examples:
  - `arn:aws:iam::123456789012:user/sri` <-- :: region is omitted because IAM is global
  - `arn:aws:s3:::my_awesome_bucket/image.png` <-- ::: - no region, no account id needed to identify an object in S3. all objects in S3 are globally unique
  - `arn:aws:dynamodb:us-east-1:123456789012:table/orders`
  - `arn:aws:ec2:us-east-1:123456789012:instance/*` - wildcard. EC2 is a regional service

### Best Practices

- Business Benefits of Cloud:

  - Almost 0 upfront infrastructure investment
  - Just in time Infrastructure
  - More efficient resource utilization
  - Usage based costing
  - Reduced time to market

- Technical Benefits of Cloud:

  - Automation - Scriptable infrastructure
  - Auto-Scaling
  - Proactive Scaling
  - More efficient development life cycle
  - Improved testability
  - DR and Business Continuity
  - Overflow the traffic to the cloud

- Design for Failure

  - Rule of thumb: Be a pessimist when designing architectures in the cloud
  - Assume things will fail, always design implement and deploy for automated recovery from failure
  - Assume your hardware will fail
  - Assume outages will occur
  - Assume that some disaster will strike your application
  - Assume that you will be slammed with more than the expected number of requests per second
  - Assume that with time your application software will fail too

- Decouple your components:

  - Build components that do not have tight dependencies on each other so that if one component dies, fails, sleeps, or becomes busy, the other components are built so they can continue to work as if no failure is happening. Build each component as a `black box`. For exmaple: Think on SQS

### [Service Quotas](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html) (known before as Service Limits)

- Your AWS account has default quotas, formerly referred to as limits, for each AWS service. Unless otherwise noted, each quota is **Region-specific**. You can request increases for some quotas, and other quotas cannot be increased.

### Types of Cloud Computing

#### Services Models

- Platform as a Service - **PaaS** (Examples: Elastic Beanstalk, Fargate)

  - Platforms as a service remove the need for organizations to manage the underlying infrastructure (usually hardware and operating systems).
  - This helps you be more efficient as you don’t need to worry about resource procurement, capacity planning, software maintenance, patching, or any of the other undifferentiated heavy lifting involved in running your application.

- Infrastructure as a Service - **IaaS** (Examples: EC2, ELB, VPC, EBS, EFS)

  - Basic building blocks for cloud IT and typically provide access to networking features, computers (virtual or on dedicated hardware), and data storage space.
  - Highest level of flexibility and management control over your IT resources.

- Software as a Service - **SaaS** (Examples: ECS, Aurora, ECR)

  - It is completed product that is run and managed by the service provider ("end-user applications").
  - You do not not only need to think about how the underlying infrastructure is managed (PaaS) but also how the service is maintained; you only need to think about how you will use that particular piece of software.

#### Deployment Models

- Public Cloud: All services of the System run in the Public cloud.

- [Hybrid](https://aws.amazon.com/hybrid/): A hybrid deployment is a way to connect infrastructure and applications between the public cloud resources and existing resources from the private one.
  - Use Case: It helps to extend, and grow, an organization's infrastructure into the public cloud while connecting cloud resources to internal system.

- On-Premises (Private Cloud): All services of the System run in on-premises, using virtualization and resource management tools.
  - Disadventage: It does not provide many of the benefits of cloud computing. There is liit number of resources in the Data Center.

## Events/Operations: Data Plane vs Control Plane

### Data Plane Operations

- Data Plane Operations (or Data Events) provide visibility into the resource operations performed on or **within a resource**
- They are often high-volume activities
- Example of data events include:
  - Amazon S3 object-level API activity (for example, GetObject, DeleteObject, and PutObject API operations).
  - AWS Lambda function execution activity (the Invoke API).

### Control Plane Operations

- Control Plane Operations (or Management Events) provide visibility into management operations that are performed **on resources in your AWS account**.
- Example management events include:
  - Configuring security (for example, IAM AttachRolePolicy API operations)
  - Registering devices (for example, Amazon EC2 CreateDefaultVpc API operations)

### Disaster recovery options in the Cloud

![DR options](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/disaster-recovery-strategies.png)

- `Backup and Restore`: Backup and restore is the approach for **mitigating against data loss or corruption. It can be also extend to mitigate against a regional disaster by replicating data to other AWS Regions**. In addition to data, **you must redeploy the infrastructure (with IaC), configuration, and application code in the recovery Region**.
- `Pilot light`: A **minimal version of the Primary Region** is always running in the Diaster Recovery. Data is replicated from one Region to another and provision a copy of your core workload infrastructure. Resources required to support data replication and backup, such as databases and object storage, are always on. Other elements, such as application servers, are loaded with application code and configurations, but are **"switched off"** and are only used during testing or when disaster recovery failover is invoked.
- `Warm standby`: A **scaled-down** but **fully functional environment** version of your Primary Region running in the DR Zone. This approach extends the pilot light concept and decreases the RTO because your workload is always-on in another Region (ready to accept traffic). When a disaster occurs, you can redirect to this environment and **scale it up to full capacity**.
- `Multi-site solution`: You can run your workload simultaneously in multiple Regions as part of a multi-site active/active or hot standby active/passive strategy. A fully functional version of your environment runs in a Second Region (user can access to it). **Data is replicated synchronously**.

## Security

Go to [Index](#index)

### IAM (Global Service)

- Keywords: Permissions (Policies), Roles, Users, Groups, MFA, Federation

- AWS Identity and Access Management Service (AWS IAM) is used to securely control **individual and group access to AWS resources**.

![IAM](https://d1.awsstatic.com/product-marketing/IAM/iam-how-it-works-diagram.04a2c4e4a1e8848155840676fa97ff2146d19012.png)

- IAM is global (so region isn’t a factor)
- It offers centralized control over your AWS account, enabling shared access to your AWS account (e.g. 1 account - multiple users)
- Granular Permissions (can set different permissions for different people/different resources)
- It allows configuration of temporary access for users, devices and services
- Includes Federation Integration which taps into Active Directory, Facebook, Linkedin, etc. for authentication
- Multi-factor authentication support
- It supports `PCI DSS compliance`: security compliant framework for taking credit card details.
- IAM entities:
  - `Users` End users such as people or employees of an organisation.
    - IAM users are individuals who have been granted access to an AWS account.
    - New Users
      - They have **NO permissions when first created** (they can only login to the AWS console) ==> Permissions must be explicitly granted to allow an user to access an AWS service.
      - They are assigned **Access Key ID & Secret Access Keys** when first created => You can get to view these once. If you lose them, you have to regenerate them.
      - In order for a new IAM user to be able to log into the console, the user must have a password set
  - `Groups` are a collection of users, and cannot contains other groups. Groups allow you to define permissions for all the users within it.
    - IMPORTANT: You cannot identify a user group as a `Principal` in a resource-based policy because groups relate to permissions, not authentication, and principals are authenticated IAM entities
  - `Roles`
    - Types of Roles
      - `Service Roles` (To assign permission to AWS Resources), specifying what the resource (such as EC2) is allowed to access on another resource (S3).
        - Roles can be assigned to an EC2 instance after it is created using both the console & command line. (`Instance Profile` ==> Service Roles assigned to EC2 instances).
      - `Cross account access roles`: Used when you have multiple AWS accounts and another AWS account must interact with the current AWS account
      - `Identity provider access roles`: Identity Federation (including AD, Facebook etc) can be configured to allow secure access to resources in an AWS account without creating an IAM user account.
    - Adventanges
      - More secure than storing your access key and secret access key on individual EC2 instances.
      - Easier to manage.
- `Policies` JSON Document that defines permissions (`Allow` or `Deny` access to an action that can be performed on AWS resources) for Access Entities (user, group or role)
  - If a resource has multiple policies — AWS joins them ==> **IAM Policy Evaluation Logic** ➔ Explicit Deny ➯ Organization SCPs ➯ Resource-based Policies (optional) ➯ IAM Permission Boundaries ➯ Identity-based Policies.
    - Anything that is not explicitly allowed is implicitly denied
    - [`Service control policies (SCPs)`](#scp) are a type of **Organization policy** that you can use to manage permissions in your organization.
      - It offers central control over the maximum available permissions for all accounts in your organization.
      - It helps you to ensure your accounts stay within your organization’s access control guidelines.
    - `IAM Permission Boundaries` to set at individual user or role for maximum allowed permissions. When you use a policy to set the permissions boundary for a user, it limits the user's permissions but does not provide permissions on its own.
  - Types of policies
    - `Identity-based policies` are attached to an IAM identity (a user, group, or role). You can use these policies to grant permissions to perform specific actions on resources. In those cases, the principal is implicitly the identity where the policy is attached.
    - `Resource-based policies` are attached to a resource. For example, you can attach resource-based policies to S3 buckets, SQS queues, VPC endpoints, and KMS encryption keys. Use `Principal` section.

![Identity-based vs Resource-based policies](https://cloudiofy.com/wp-content/uploads/2022/08/aws-resource-permission-types.png)

  - Sections:
    - `Version` policy language version. `2012-10-17` is the latest version.
    - `Statement` container for one or more policy statements
    - `Sid` (optional) a way of labeling your policy statement
    - `Effect` set whether the policy **Allows or Deny**
    - `Principal` (WHO, **Only for Resource-based policies**) to specify the principal that is allowed or denied access to a resource (AWS account and root user, IAM roles, Role sessions, IAM users, Federated user sessions, AWS services, All principals)
    - `Action` (WHAT) one or more actions that can be performed on AWS resources
    - `Resource` (WHERE) one or more AWS resources to which actions apply
    - `Condition` (optional) one or more conditions to satisfy for policy to be applicable, otherwise ignore the policy.
      -  `aws:PrincipalOrgID` condition key lets you specify the AWS organization ID of the principal entity (root user, IAM user, or IAM role) making the request.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Deny-Barclay-S3-Access",
      "Effect": "Deny",
      "Principal": { "AWS": ["arn:aws:iam:123456789012:barclay"] },
      "Action": ["s3:GetObject", "s3:PutObject", "s3:List*"],
      "Resource": ["arn:aws:s3:::mybucket/*"]
    },
    {
      "Effect": "Allow",
      "Action": "iam:CreateServiceLinkedRole",
      "Resource": "*",
      "Condition": {
        "StringLike": {
          "iam:AWSServiceName": [
            "rds.amazonaws.com",
            "rds.application-autoscaling.amazonaws.com"
          ]
        }
      }
    }
  ]
}
```

- `Root account` is created by default with full administration powers. Root account is email address that you used to register your account
  - Best practices
    - Not to use the root account for anything other than billing (not login)
    - Always setup Multifactor Authentication on your root account.
- `Power user access` → Access to all AWS services except the management of groups and users within IAM
- Use Case:
  1. An application running on an Amazon ECS container instance needs permissions to write data to Amazon DynamoDB. How can you assign these permissions only to the specific ECS task that is running the application? ==> To specify permissions for a specific task on Amazon ECS you should use IAM Roles for Tasks. The permissions policy can be applied to tasks when creating the task definition, or by using an IAM task role override using the AWS CLI or SDKs. The taskRoleArn parameter is used to specify the policy.
  2. A company requires that all AWS IAM user accounts have specific complexity requirements and minimum password length. How to accomplish this? ==> Update the password policy that applies to the entire AWS account.
  3. To accelerate experimentation and agility, a company allows developers to apply existing IAM policies to existing IAM roles. Nevertheless, the security operations team is concerned that the developers could attach the existing administrator policy, circumventing any other security policies ==> Use Permisssion Boundaries.

### Access AWS

- Types of Access
  - IAM Users
  - None IAM Users

#### IAM Users: Access Key

- Ways to Autheticate Request on AWS
  - AWS Management Console - Use Password (+ MFA - best practice)
  - AWS CLI or SDK - Use Access Keys
  - AWS CloudShell - CLI tool from AWS browser console (Require login to AWS)
- Access keys consist of two parts: an `Access key ID` and a `Secret access key`. You must use both to authenticate your requests.
- When creating new IAM Users from an AWS account
  - User's password: Once the users have been created, you can opt to create a generated or custom password.
    - If generated, there is an option to force the user to set a custom password on next login.
    - Once a generated password has been issued, you can see the password (which is the same as the access keys). Its shown once only.
  - User's credentials, you can only see/download the credentials at the time of creation not after.
  - Access Keys can be retired, and new ones can be created in the event that secret access keys are lost.

#### None IAM Users

- Non-IAM user first authenticates from Identity Federation ==> Then provide a **temporary token with an IAM Role attached** generated by calling a AssumeRole API of `STS (Security Token Service)`
  - AWS Security Token Service (AWS STS) as a web service that enables you to request temporary, limited-privilege credentials for AWS Identity and Access Management (IAM) users or for users you authenticate (federated users)

##### Identity Federation

- SAML 2.0 (old) to integrate Active Directory/ADFS, use `AssumeRoleWithSAML` STS API.
- Custom Identity Broker used when identity provider is not compatible to SAML 2.0, use `AssumeRole` or `GetFederationToken` STS API.
- Web Identity Federation is used to sign in using well-known external identity provider (IdP): Facebook, Google, or any OpenID Connect (OIDC)-compatible IdP. Get the ID token from IdP, use AWS Cognito api to exchange ID token with cognito token, use AssumeRoleWithWebIdentity STS API to get temp security credential to access AWS resources.
- AWS Cognito (`Amazon Cognito Federated Identities`) is recommended identity provider by Amazon.
- Amazon Single Sign On gives single sign on token to access AWS, no need to call STS API.

##### AWS Directory Service

- Directories store information about users, groups, and devices, and administrators use them to manage access to information and resources. **Hierarchical database of users, groups, computers - trees and forests**.

###### Compatible with Microsoft Active Directory

- `Managed Microsoft Active Directory`

  - It is managed Microsoft Windows Server AD with **trust connection to on-premise Microsoft AD**.
  - Best choice when you need all AD features to support AWS applications or Windows workloads.
  - Easily migrate on-premise workloads as it is built on actual Microsoft AD, so does not require any replication of existing directory to the cloud.
  - Highly available as directories are deployed across multiple Availability Zones and failovers are detected automatically.
  - Use case: Extend your on-premise using AD Trust with AWS Managed Microsoft AD so that both your on-premises and cloud directories remain separated, but it allows your users access AWS as needed.

- `Simple AD`

  - Use Simple AD in standalone AWS managed compatible AD powered by `Samba 4` with basic directory features (Enables a subset of the features Managed Microsoft AD).
  - You cannot connect it to on-premise AD.
  - Best choice for basic directory features.
  - Can be used for Linux workloads that need LDAP.

- `AD Connector`

  - It is proxy service to redirect requests to on-premise Microsoft AD, without caching information in the cloud.
  - Best choice to use existing on-premise AD with compatible AWS services.
  - Can use multiple AD Connectors to spread the load to match performance needs.
  - Cannot be used across different AWS accounts.

###### No Compatible with Microsft Active Directory

- `Cloud Directory`

  - Cloud-native directories for organizing Hierarchies of data along **multiple dimensions** fully managed by AWS
  - Can have multiple hierarchies with hundreds/millions of objects.
  - Some common use cases include: directories for organisational charts, course catalogs, and device registries.

- `Amazon Cognito`

  - It controls use authentication (sign-up and sign-in) + access (premissions) for **mobile and web applications**. Supports guest users.
  - The two main components of Amazon Cognito are:

Steps: You first authenticate user using `Cognito User Pools` and then exchange token with `Cognito Identity Pools` which further use `AWS STS` to generate temporary AWS credentials to access AWS Resources.

a. `User pools`: User directory for Application (web and mobile) authentication and authorization. For the perspective of the Applications, it acts as OpenID Connect (OIDC) identity provider (IdP). You can combine the Amazon Cognito directory with an external identity provider.

![Amazon Cognito, User pools](https://docs.aws.amazon.com/images/cognito/latest/developerguide/images/scenario-authentication-cup.png)

b. `Identity pools`: It grants to Federated users temporary credentials to other AWS services (e.g., Amazon S3 and DynamoDB).

**Exam Tip :** To make it easier to remember the different between User Pools and Identity Pools, think of Users Pools as being like IAM Users or Active Directory and an Identity Pools as being like an IAM Role.

### AWS Key Management Service (KMS)

- Keywords: AWS managed Keystore for encryption, Key rotation

![AWS Key Management Service (KMS)](https://d1.awsstatic.com/Security/aws-kms/Group%2017aws-kms.6dc3dbbbe5b75b46c4f62218d0531e5bed7276ce.png)

- AWS managed **centralized key management** service to create, manage and rotate `Customer Master Keys (CMKs)` for **encryption at REST**.
- Can integrate with most other AWS services to increase security and make it easier to encrypt your data.
- You can enable automatic master key rotation once per year. Service keeps the older version of master key to decrypt old encrypted data.
- Allows you to control access to the keys using things like IAM policies or key policies.
- Encrypt/decrypt up to 4KB.
- Pay per API call.
- Validated under `FIPS 140–2 (Level 2)` security standard.
- Types of `Customer Master Keys` (CMKs)
  - `Customer Managed` CMKs (Dedicated to my account) → Keys that you have created in AWS, that you own and manage. You are responsible for managing their **key policies (who can access), rotating them and enabling/disabling them**.
    - It can be created for encyption for client and server side.
    - You can create customer-managed `Symmetric` (single key for both encrypt and decrypt operations) or `Asymmetric` (public/private key pair for encrypt/decrypt or sign/verify operations) master keys.
    - Symmetric CMKs
      - With symmetric keys, the same key is used to encrypt and decrypt
      - The key never leaves AWS unencrypted
      - Must call the KMS API to use a symmetric key
      - **The AWS services that integrate with KMS use symmetric CMKs**
    - Asymmetric CMKs
      - Asymmetric keys are mathematically related public and private key pairs.
      - The private key never leaves AWS unencrypted.
      - You can call the KMS API with the public key, which can be downloaded and used outside of AWS.
      - AWS services that integrate with KMS DO NOT support asymmetric keys.
  - `AWS Managed` CMKs (Dedicated to my account) → These are **free** and are created by an AWS service on your behalf and are managed for you. However, only that service can use them. Used by default if you pick encryption in most AWS services. Only for server side Encryption.
  - `AWS Owned` CMKs (No Dedicated to my account) → owned and managed by AWS and shared across many accounts.

**Exam Tip :** Encryption keys are regional.

- Use Case: A company is planning to use Amazon S3 to store documents uploaded by its customers. The images must be encrypted at rest in Amazon S3. The company does not want to spend time managing and rotating the keys, but it does want to control who can access those keys.
  - Customer managed CMK (not AWS Managed) because you want to control who can access the keys (policies).

### AWS CloudHSM

- Keywords: Own Encription Keystore hosted in AWS

![AWS CloudHSM](https://d1.awsstatic.com/whiteboard-graphics/products/CloudHSM/product-page-diagram_AWS-CloudHSM_HIW.76ce14889e22d8861a6a9fff0b5664516ed1bddd.png)

- Dedicated cloud-based Hardware Security Module (HSM) for creating, using and managing **your own encryption keys (cryptographic keys) in AWS**
  - Integrate with your application using industry-standard APIs (No AWS APIs), such as PKCS#11, Java Cryptography Extensions (JCE), and Microsoft CryptoNG (CNG) libraries (there are no AWS APIs for HSM)
- No access to the AWS managed component and AWS does not have visibility or access to your keys.
- Conforms to `FIPS 140–2 (Level 3)` security standard
- It runs within a VPC in your account
  - It will operate inside its own VPC dedicated to CloudHSM
  - It will project to ENI of customer VPC
- Keys are irretrievable if lost and can not be recovered
- Use case: Use KMS to create a CMKs in a custom key store and store non-extractable key material in AWS CloudHSM to get a full control on encryption keys
- Difference between KMS and CloudHSM
  - FIPS 140–2 KMS (Level 2) vs CloudHSM (Level 3)
  - KMS (Multi Tenant) and CloudHSM (Single Tenant, dedicate h/w, Mutli-AZ cluster)
  - KMS (AWS managed) and CloudHSM (Self-managed)

### AWS Systems Manager

- Keywords: Configuration and Secrets store

![AWS Systems Manager](https://d1.awsstatic.com/AWS%20Systems%20Manager/Product-Page-Diagram_AWS-Systems-Manager.9184df66edfbc48285d16c810c3f2d670e210479.png)

- `Parameter Store` is Secure and centralized serverless **storage of configuration and secrets**: passwords, database details, and license code, API Keys
  - Use case: Centralized configuration for dev/uat/prod environment to be used by CLI, SDK, and Lambda function
- `Run Command` allows you to automate common administrative tasks and perform one-time configuration changes on EC2 instances at scale
- `Session Manager` replaces the need for Bastions to access instances in private subnet

### AWS Secrets Manager

- Keywords: Secrets store

![AWS Secrets Manager](https://d1.awsstatic.com/diagrams/Secrets-HIW.e84b6533ffb6bd688dad66cfca36622c2fa7c984.png)

- Secret Manager is mainly used to store, manage, and rotate **secrets (passwords)** such as database credentials, API keys, and OAuth tokens.
- Generate random secrets: Apply the new key/passwords in RDS for you.
- Secret rotation
  - It has **native support to rotate database credentials of RDS databases** - MySQL, PostgreSQL and Amazon Aurora. Automatically rotate secrets.
  - For other secrets such as API keys or tokens, you need to use the **lambda for customized rotation function**.
- Differences with AWS Systems Manager - Parameter Store
  - Secrets Manager is specifically for secrets, whereas Parameter Store is for generic strings.
  - Secrets Manager has built-in password generation, rotatoion.
  - Secrets Manager counts with Crosss Account
  - Secrets Manager comes with additional cost. Parameter Store is free for standard parameters.

### AWS License Manager

- It makes it easier to manage your software licenses from vendors such as Microsoft, SAP, Oracle, and IBM **across AWS and on-premises environments**.
- It lets administrators create customized licensing rules that mirror the terms of their licensing agreements.

![](https://d1.awsstatic.com/License%20Manager%20HIW.7164c190e6a7f13d789f67be1df35005031cb73a.png)

### AWS Shield

- Keywords: DDoS attacks, Layers 3,4 and 7

![AWS Shield](https://d1.awsstatic.com/AWS%20Shield%402x.1d111b296bfd0dd864664b682217bc7610453808.png)

- AWS Shield provide protections against **Distributed Denial of Service (DDoS) attacks** for AWS resources at the network and transport layers (**layer 3 and 4**) and the application layer (**layer 7**)
  - Denial-of-service attack (DoS attack) is a cyber-attack in which the perpetrator seeks to make a machine or network resource unavailable to its intended users by temporarily or indefinitely disrupting services of a host connected to a network. Denial of service is typically accomplished by flooding the targeted machine or resource with superfluous requests in an attempt to overload systems and prevent some or all legitimate requests from being fulfilled
- Types
  - `AWS Shield Standard` is automatic and free DDoS protection service for all AWS customers for CloudFront and Route 53 resources.
  - `AWS Shield Advanced` is paid service ($3K per month per org) for enhanced DDoS protection for EC2, ELB, CloudFront, and Route 53 resources.

### AWS WAF

- Keywords: SQL injection, Cross-site scripting (XSS), Layers 7 (HTTPs), IP restrictions

![AWS WAF](https://d1.awsstatic.com/Product-Page-Diagram_AWS-Web-Application-Firewall%402x.5f24d1b519ed1a88b7278c5d4cf7e4eeaf9b75cf.png)

- **Web Application Firewall** protect against **Layer 7** (HTTP & HTTPS) attacks, adding protection to your web applications or APIs against web attacks from common exploits, such as SQL injection or Cross-site scripting (XSS).
  - SQL injection is a code injection technique used to attack data-driven applications, in which malicious SQL statements are inserted into an entry field for execution (e.g. to dump the database contents to the attacker).
  - Cross-site scripting (XSS) attacks enable attackers to inject client-side scripts into web pages viewed by other users. A cross-site scripting vulnerability may be used by attackers to bypass access controls such as the same-origin policy.
- You can deploy WAF on:
  - CloudFront
  - **Application Load Balancer** (not in ELB or NLB) - Exat Tip
  - API Gateway
  - AWS AppSync
- How? => AWS WAF lets you create **Rules** to **filter web traffic** based on **conditions that include IP addresses, HTTP headers and body, or custom URIs**.
  - Those rules can **allow or block** what you specify. It also allows to count the requests that match a certain pattern.
  - It offers a set of pre-configured managed rules that you can use to get started quickly. They cover things like the OWASP Top 10 Security risks.
  - Conditions are used in WAFs to specify when you want to allow/block requests. Below are some examples of conditions that you might:
    - Values on the request header
    - The country a request comes from
    - Specific IP addresses
    - Strings that appear in requests
    - Length of the request
    - Presence of SQL code
    - Presence of a script
- Pay for what you use, based on the number of rules you have and requests your applications receive.
- Use Case:
  1. A website runs on Amazon EC2 instances behind an Application Load Balancer (ALB) which serves as an origin for an Amazon CloudFront distribution. An AWS WAF is being used to protect against SQL injection attacks. A review of security logs revealed an external malicious IP that needs to be blocked from accessing the website. How to protect the application? ==> Create a Rule to block request based on the malicious IP addresses.

### AWS Network Firewall

- Keywords: VPC level, Layer 3-7

- With AWS Network Firewall, you can define **firewall rules** that provide fine-grained control over network traffic. Network Firewall works together with AWS Firewall Manager so you can build policies based on Network Firewall rules and then centrally apply those policies across your **virtual private clouds (VPCs) and accounts**.
- Its primary objective is to separate a secured zone from a less secure zone and control communications between the two. Without it, any computer with a public Internet Protocol (IP) address is accessible outside the network and potentially at risk of attack.

![AWS Network Firewall](https://d1.awsstatic.com/Product-Page-Diagram_AWS-Network-Firewall%402x.68dc577022a7624450c24747789d214ccf0f1178.png)

- Use Case: An Amazon EC2 instance runs in a VPC network, and the network must be secured. The EC2 instances contain highly sensitive data and have been launched in private subnets. Company policy restricts EC2 instances that run in the VPC from accessing the internet. The instances need to access the software repositories using a third-party URL to download and install software product updates. All other internet traffic must be blocked, with no exceptions.
  - The AWS Network Firewall is a managed service that makes it easy to deploy essential network protections for all your Amazon Virtual Private Clouds, and you can then use domain list rules to block HTTP or HTTPS traffic to domains identified as low-reputation, or that are known or suspected to be associated with malware or botnets.

#### AWS Network Firewall vs WAF vs Security Groups vs NACLs

![AWS Network Firewall vs WAF vs Security Groups vs NACLs](https://jayendrapatil.com/wp-content/uploads/2022/08/AWS-Security-Groups-vs-NACLs-vs-WAF-vs-Network-Firewall.jpg)

### AWS Firewall Manager

![AWS Firewall Manager](https://d1.awsstatic.com/products/firewall-manager/product-page-diagram_AWS-Firewall-Manager%402x%20(1)1.ad6bf5281dc2c33c0493e9988e3504dd1590eaa2.png)

- Use AWS Firewall Manager to **centrally configure and manage Firewall Rules across an Organization**: AWS WAF rules, AWS Shield Advanced, Network Firewall rules, and Route 53 DNS Firewall Rules
- Use case: Meet Gov regulations to deploy AWS WAF rule to block traffic from embargoed countries across accounts and resources

### AWS GuardDuty

- Keywords: **Anomalous Behaviour**, Exiting Treat Exploided, Compromised, Detect and Remediate

![AWS GuardDuty](https://d1.awsstatic.com/Security/Amazon-GuardDuty/Amazon-GuardDuty_HIW.057a144483974cb73ab5f3f87a50c7c79f6521fb.png)

- A **treat detection** service that applys **machine learning** that monitors for compromised **AWS Accounts** (Multiple EC2 services), anomalous baheviour and malware (**"vulnerability that was exploited"**)
- The primary detection categories include reconnaissance, instance compromise, account compromise, and bucket compromise.
- Once it is activated, it monitors continously: VPC Flow Logs, DNS Logs, and CloudTrail events. And based on its findings you can setup **automated preventive actions or remediation’s**. For example, you can automate the response workflow by using CloudWatch Events as an event source to trigger an AWS Lambda function.
- Use case: CryptoCurrency attacks protection.

![AWS GuardDuty -2](https://cloudkatha.com/ezoimgfmt/i0.wp.com/cloudkatha.com/wp-content/uploads/2022/02/TempCK-Amazon-GuardDuty.jpg?w=829&ssl=1&ezimgfmt=ng:webp/ngcb2)

### Amazon Inspector

- Keywords: Workload, Software Vulnerabilities, Network Exposure, Agent, Prevention, Only detects

![Amazon Inspector](https://d1.awsstatic.com/reInvent/re21-pdp-tier1/amazon-inspector/Amazon-Inspector_HIW%402x.c26d455cb7e4e947c5cb2f9a5e0ab0238a445227.png)

- It is and **Agent based** vulnerability **scanning** tool that you can use to identify potential security issues **within your EC2 worloads (EC2, ECS, EKS)**
- It detects vulnerabilities and insecure configurations in your applications (software vulnerabilities) and network (uninteded network exposure), **event if it was not exploited yet** (preventation).

![Amazon Inspector -2](https://cloudkatha.com/ezoimgfmt/i0.wp.com/cloudkatha.com/wp-content/uploads/2022/02/Amazon-GuardDuty-Vs-Inspector.png?w=739&ssl=1&ezimgfmt=ng:webp/ngcb2)

### Amazon Macie

- Keywords: **sensitive data**

![Amazon Macie](https://d1.awsstatic.com/reInvent/reinvent-2022/macie/Product-Page-Diagram_Amazon-Macie.a51550cca0a731ba2e4a26e8463ed5f5a81202e3.png)

- Managed service to discover and protect your **sensitive data** in AWS s3.
- Can automatically discover **Personally Identifiable Information (PII)** in your data and can alert you once identified (e.g. selected S3 buckets)
- Can produce dashboards, reporting and alerts
- Benefits of Macie
  - Cost efficiently discovers sensitive data at scale
  - Constant visibility of data security/privacy through alerts and dashboards
  - Can use used across AWS accounts through AWS Organisations.
  - Can help you meet regulatory compliance
  - Great for PCI-DSS(credit card payments) and preventing theft

### AWS Config

- Keywords: Security Governance, Audit Changes, Configuration History

![AWS Config](https://d1.awsstatic.com/config-diagram-092122.974fe2a4cb6aae1fe564fdbbe30ab55841a9858e.png)

- Managed service that provides you with an AWS resource inventory, configuration history, and configuration change notifications to enable **security and governance**. **Assess, audit, and evaluate configurations of your AWS resources** in multi-region, multi-account
- `Config Rules` to confirm that resources are configured in compliance with policies
- You are notified via SNS for any configuration change
- Integrated with CloudTrail, provide resource configuration history
- Use cases:
  1. Customers need to comply with standards like PCI-DSS (Payment Card Industry Data Security Standard) or HIPAA (U.S. Health Insurance Portability and Accountability Act) can use this service to assess compliance of AWS infra configurations
  2. A company requires that IAM users must rotate their access keys every 60 days. If an access key is found to older it must be removed. How to create an automated solution that checks the age of access keys and removes any keys that exceed the maximum age defined ==> Create an AWS Config rule to check for the key age. Define an Amazon EventBridge rule to execute an AWS Lambda function that removes the key

## Compute

Go to [Index](#index)

### EC2

- Infrastructure as a Service (IaaS) - Re-sizable (elastic) and secure virtual machine on the cloud.
  - Amazon EC2 reduces the time required to obtain and boot new server instances to minutes, allowing you to quickly scale capacity, both up and down, as your computing requirements change.
  - Gives you complete control of your computing resources including choice of storage, processor, networking and operating system.
- When you restart an EC2 instance, its public IP can change. Use `Elastic IP` to assign a fixed public IPv4 to your EC2 instance.
  - By default, all AWS accounts are limited to five (5) Elastic IP addresses per Region.
- The EC2 Root volume is a virtual disk where the OS is installed, it can only be launched on SSD or Magnetic.
- Bootstrap scripts are code that gets ran as soon as your EC2 instance first boots up.
- EC2 Information Endpoints (can be obteined via `curl`):
  - `http://169.254.169.254/latest/meta-data` ==> Metadata Private & public IP
  - `http://169.254.169.254/latest/user-data` ==> user-defined data
- Use **VM Import/Export** to import virtual machine image and convert to `Amazon EC2 AMI` to launch EC2 instances
- Termination State ==> Destroy EC2
  - There is optional protection (it is turned off by default)
  - On an EBS-backed instance, the default action once a EC2 instance moves to Terminate State:
    - **Root EBS volume to be deleted**.
    - Additional EBS volumes mounts won't be deleted.
- Encryption
  - Asymmetric encryption (key pair — public & private)
  - Root device volumes can be encrypted. You can also use a third party tool (such as bit locker etc) to encrypt the root volume, or this can be done when creating AMI's in the AWS console or using the API.
  - Additional volumes can be encrypted as well.

Exam tip: You can stop and start an EC2 instance to move it to a different physical host if EC2 status checks are failing or there is planned maintenance on the current physical host.

#### EC2 Fleet

- It contains the **configuration information** to launch a fleet or **group of instances**. In a single API call, can include multiple instance types across multiple Availability Zones, using the On-Demand Instance, Reserved Instance, and Spot Instance purchasing options together. Using EC2 Fleet, you can:
  - Define separate On-Demand and Spot capacity targets and the maximum amount you’re willing to pay per hour
  - Specify the instance types that work best for your applications
  - Specify how Amazon EC2 should distribute your fleet capacity within each purchasing option

#### EC2 Hibernate

- Hibernation saves the contents from the instance memory (RAM) to your Amazon Elastic Block Store (Amazon EBS) root volume. Amazon EC2 persists the instance's EBS root volume and any attached EBS data volumes. When you start your instance:
  - The EBS root volume is restored to its previous state
  - The RAM contents are reloaded
  - The processes that were previously running on the instance are resumed
  - Previously attached data volumes are reattached to the instance
- **In comparison with EBS snapshot restore ==> Boots up a lot faster after hibernation as it does not need to reload the operating system**.
- You can hibernate an instance only if it’s enabled for hibernation and it meets the hibernation prerequisites.
  - Can’t hibernate for more than 60 days.
- Once in hibernation mode there is no hourly charge — you only pay for the elastic IP Address & other attached volumes.
- Use case: For long running services and services that take long to boot. You can stop them and pick back up where you left off again.

#### EC2 Instance Types

You can choose EC2 instance type based on requirement for e.g. `m5.2xlarge` has Linux OS, 8 vCPU, 32GB RAM, EBS-Only Storage, Up to 10 Gbps Network bandwidth, Up to 4,750 Mbps IO Operations.

| Instance Class | Usage Type            | Usage Example                                                                                                            |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| T, M           | General Purpose       | Web Server, Code Repo, Microservice, Small Database, Virtual Desktop, Dev Environment                                    |
| C              | Compute Optimized     | High Performance Computing (HPC), Batch Processing, Gaming Server, Scientific Modelling, CPU-based machine learning      |
| R, X, Z        | Memory Optimized      | In-memory Cache, High Performance Database, Real-time big data analytics                                                 |
| F, G, P        | Accelerated Computing | High GPU, Graphics Intensive Applications, Machine Learning, Speech Recognition                                          |
| D, H, I        | Storage Optimized     | EC2 Instance Storage, High I/O Performance, HDFS, MapReduce File Systems, Spark, Hadoop, Redshift, Kafka, Elastic Search |

- You must provision nitro-based EC2 instance to achieve 64000 EBS IOPS. Max 32000 EBS IOPS with Non-Nitro EC2.

#### EC2 Pricing Types

- `On-Demand` - Pay a fixed rate by the hour (or by the second) with no commitment. **Pay as you use, costly**.
  - Use Cases:
    - **Non-Production Enviroment**
      - Applications being developed or tested on Amazon EC2 for the first time.
      - Applications with short term, spiky or unpredictable workloads that cannot be interrupted.
    - Users that want the low cost and flexibility of Amazon EC2 without any up-front payment for long-term commitment.
- `On-Demand Capacity Reservation` - Billing discont. Reserve compute capacity for your Amazon EC2 instances in a specific Availability Zone **for any duration**. When you no longer need the capacity assurance, cancel the Capacity Reservation to release the capacity and to stop incurring charges
  - Use Cases: Useful for predictable workloads that are not interrupte: Disaster recovery, Regulatory requirements, Events.
- `Reserved` - Provides you with a Capacity Reservation and **offer discount on the hourly charge** for an instance, but it requires to have a **Contracts for 1 - 3 year terms**. Higher discount with upfront payments and longer contracts. However, you can't move between regions.
  - Uses Cases:
    - **Production Environment**
      - Applications with steady or **predictable** usage (Example: An application runs constatly with a a predictable traffic increase every two weeks)
      - Applications that require reserved capacity.
    - Users able to make upfront payments to reduce their total computing costs even further.
  - Types:
    - `Standard Reserved Instances` Provides the **most discount** (up to 75% off). Can't be exchanged. Unused instanced can be sold in AWS reserved instance marketplace.
    - `Convertible Reserved Instances` up to 54% off. It can be exchanged during the term for another Convertible Reserved Instance with new attributes, including instance family, instance type, platform, scope, or tenancy.
  - Exam Question: A company runs a large batch processing job at the end of every quarter. The processing job runs for 5 days and uses 15 Amazon EC2 instances. The processing must run uninterrupted for 5 hours per day. The company is investigating ways to reduce the cost of the batch processing job. Which pricing model should the company choose?
    - This is time duration is insufficient to warrant `Reserved` instances as these require a commitment of a minimum of 1 year ==> If they dates are known (predictable) they can use `On-Demand Capacity Reservation`, otherwise `On-Demand` without any reduction on cost.
- `Spot Instances` - You can set the price you are willing to pay ("budget") and it will run when its below or at that price — if it goes above that price you lose it without any acknowledgement.
  - It provides up to **90% discount** and typically used for apps with flexible start/end times. But **don’t use for anything critical that needs to be online all the time**. It can handle interruptions and recover gracefully.
  - Imp Note: If the spot instance is terminated by Amazon EC2, you will not be charged for a partial hour of usage. However, if you terminate the instance yourself, you will be charged for any hour in which the instance ran.
  - Uses Cases
    - Applications that have flexible start and end times.
    - Applications that are only feasible at very low compute prices.
    - Users with urgent computing needs for large amounts of additional capacity.
  - Types
    - `Spot Blocks` can also be **launched with a required duration**, which are not interrupted due to changes in the Spot price.
    - `Spot Fleet`
      - Collection of spot instances and optionally on-demand instances. Attempts to **launch a number of them together to meet a certain capacity within your price budget**.
      - The allocation of spot instances depends on how they fulfil your spot fleet request from the possible pool of instances.
      - Strategies:
        - Lowest Price → This is the default strategy. Chooses the fleet pool with the lowest price.
        - Diversified → Distributed across all pools.
        - Capacity Optimised → Pool for optimal capacity for the number of instances launching.
        - InstancePoolsToUseCount → Distributed across the number of pools you specify — this can only be used with the lowest price option.
- `Dedicated Instance` - Your instance runs on a **dedicated hardware provide physical isolation**, single-tenant
- `Dedicated Hosts` - Your instances run on a **dedicated physical server**. More visibility how instances are placed on server. Dedicated Hosts can help reduce costs by letting you use existing server-bound software licenses and address **corporate compliance and regulatory requirements**.
  - Can be purchased On-Demand (hourly)
  - Can be purchased as a Reservation for up to 70% off the On-Demand price.
  - Uses Cases
    - Useful for regulatory requirements that may not support multi-tenant virtualisation.
    - Great for licensing which doesn't support multi-tenancy or cloud.

#### Security Groups

- A security group acts as a **virtual firewall for your EC2 instances** to control incoming and outgoing traffic.
- If you don't specify a Security Group, the EC2 instance is linked to the default Security Group.
- Changes to a security groups rules take effect immediately and are automatically applied to all instances associated with that group.
- When you create a New Security Group
  - **All inbound traffic is blocked by default** - so we enable some IP and ports using Security Groups.
    - To let All IPs in `0.0.0.0/0`. To let a single IP address in `X.X.X.X/32` (32 means this ip address)
    - Common Ports: Linux (port 22) and Microsoft - RDP (port 3389)
  - **All outbound traffic is allowed**.
    - Common Ports: HTTP (80) and HTTPS (443)
- Cardinality: N Security Group <-> N EC2 Instance
  - You can have any number of EC2 instances within a security group.
  - You can have multiple Security Groups attached/assigned to EC2 instances.
- Security Groups vs ACL
  - **Security Groups are STATEFUL, when you create an inbound rule and an outbound rule is automatically created**. However, NACL's are STATELESS, when you create an inbound rule and an outbound rule is not automatically created.
  - **Security Groups are only permisse**, you can specify allows rule, but **not deny rules**. You CANNOT block specific IP's/Port's using Security Groups instead use Network Access Control Lists.

#### EC2 Enhanced Networking

- Elastic Network Interface (ENI) is a virtual network card, which you attach to EC2 instance in same AZ which is used to **ensure a good network performance**.
  - It provides higher bandwidth, higher packets per second performance consistently lower it into instance latencies, and there's no additional charge for using.
- Types:
  - `Elastic Network Adapter (ENA)` for C4, D2, and M4 EC2 instances, Upto 100 Gbps network speed.
  - `Intel 82599 Virtual Function (VF)` Interface for C3, C4, D2, I2, M4, and R3 EC2 instances, Upto 10 Gbps network speed. Old instance types.
  - `Elastic Fabric Adapter (EFA)` is ENA with additional OS-bypass functionality, which enables **tightly-coupled High Performance Computing (HPC) and Machine Learning** applications to bypass the operating system kernel and communicate directly with EFA device resulting in very high performance and low latency. for M5, C5, R5, I3, G4, metal EC2 instances.

#### EC2 Placement Groups Strategy

- A way of **placing EC2 Instances** so that instances are spread **across the underlying hardware to minimise failures**
- Placement group names need to be unique within your account
- Only certain types of instances can be launched in a placement group (Compute Optimised, GPU, Memory Optimised, Storage Optimised)
- You can’t merge placement groups, but you can move an existing instance into a placement group (the instance must be in the stopped state before moving it)
  - Move or remove can only be done via AWS Console (an instance using the AWS CLI or AWS SDK).
- There is no charge associated with creating placement groups
- Types (A clustered placement group can't span multiple AZ's, others can)
  - **Cluster** - Grouping instances close together within a **single Availability Zone, Same Rack**. It is used to achieve **low Network latency & high throughput, High Performance Computing (HPC)**.
    - AWS recommend homogeneous instances within clustered placement groups.
  - **Spread** - Opposite to clustered placement group. Instance are placed on **Different AZ, Distinct Rack**. It used for Critical Applications that requires to be seperated on each other to ensure **High Availability** in case of failure. Spread placement groups can span multiple Availability Zones.
  - **Partition** - EC2 creates partitions by dividing each group into logical segments. Each partition has its own set of racks, network and power source to help isolate the impact of a hardware failure. Same or Different AZ, Different Rack (or Partition), Distributed Applications like Hadoop, Cassandra, Kafka, etc.

#### AMI (Amazon Machine Image)

- **Customized image of an EC2 instance**, having built-in OS, softwares, configurations, etc.
- AMI's can be created **from both Volumes and Snapshots**.
  - You can create an AMI from EC2 instance and launch a new EC2 instance from AMI.
- AMI **are built for a specific region and can be copied across regions** (Important for Disaster Recovery)
- Use Case:
  1. A company's application is running on Amazon EC2 instances in a single Region. In the event of a disaster, how do you ensure that the resources can also be deployed to a second Region?
     - Copy an Amazon Machine Image (AMI) of an EC2 instance and specify the second Region for the destination
     - Launch a new EC2 instance from an Amazon Machine Image (AMI) in the second Region
  2. An application has been migrated to Amazon EC2 Linux instances. The EC2 instances run several 1-hour tasks on a schedule. There is no common programming language among these tasks, as they were written by different teams. Currently, these tasks run on a single instance, which raises concerns about performance and scalability. Which solution will meet these requirements with the LEAST Operational overhead?
     - The best solution is to create an AMI of the EC2 instance, and then use it as a template for which to launch additional instances using an Auto Scaling Group, allowing the EC2 instances to automatically scale and be launched across multiple Availability Zones.
     - Lambda is not the best solution because it is not designed to run for 1 hour (mx 15 min)

### Elastic Load Balancing (ELB)

- Designed to help **balance the load of incoming traffic** by distributing it across multiple targets/destinations.
  - Target group (ALB o CLB) can have one or more EC2 instances, IP Addresses, lambda functions.
- It makes the **traffic Scale and Fault Tolerant** (It can balance load **across one or more Availability Zones**)
- Internal Load Balancers are load balancers that are inside private subnets
- Load Balancers have their own **static DNS name** (e.g. <http://myalb-123456789.us-east-1.elb.amazonaws.com>) — you will NEVER be given an IP address
  - If you need the IPv4 address of your end user, look for the `X-Forwarded-For` header.
- `Health Checks`
  - Instances monitored by ELB are reported as; InService, or OutofService
  - Health Checks checks the instance health by talking to it.
  - `504 Error` means that the gateway has timed out. This means that the application not responding within the idle timeout period.
- Advanced Load Balancers Theory
  - `Stickiness` (a.k.a. Session Affinity, Sticky Sessions):
    - Allows you to **bind a users session to a specific instance**, ensuring all requests in that specific session are sent to the same instance.
    - Use Cases: If you have got an EC2 instance or an application, where you're writing to an EC2 instance like local disk, then of course you would want to enable Sticky.
    - Exam Question: A user trying to visit a website behind a classic load balancer and essentially what's happening is it's just sending all the traffic to one EC2 instance. Answer: Disable Sticky session.
    - It works in CLB and ALB. (It doesn’t work with NLB)
  - `Cross Zone load Balancing`
    - It enables **EC2 instances to get equal share of traffic/load across multiple AZs**
    - Use Cases: Route 53 is used for DNS, and it is splitting of our traffic 50/50 and sending the requests to EC2's in two diff AZ's. Each AZ has a Load Balancer, The first AZ (US-EAST-1A) has 4 EC2 instances and the second (US-EAST-1B) has only one EC2 instance. As result first AZ will split 50% to 4 instances and the second AZ receives 50% on 1 instance.
      - When we enable Cross Zone Load Balancing: The Load balancer will distribute the load evenly among instances on both AZ's.
  - `Path Patterns` (path-based routing) → can **direct traffic to different EC2 instances based on request URL (path)**.
    - Use Case: We got a user and we are using Route 53 for our DNS, enabling Path Patterns we could send request to `www.myurl.com` to AZ1 and `www.myurl.com/images` to instances in AZ2.

- Types of ELB

| Type                        | Protocol                                                   | OSI Layer                   |
| --------------------------- | ---------------------------------------------------------- | --------------------------- |
| Application Load Balancer   | HTTP, HTTPS, WebSocket                                     | Layer 7 (Application layer) |
| Network Load Balancer       | TCP, UDP, TLS                                              | Layer 4 (Transport layer)   |
| Gateway Load Balancer       | Thirdparty appliances, virtual applications e.g. firewalls | Layer 3                     |
| Classic Load Balancer (old) | HTTP, HTTPS, TCP                                           | Both Layer 7 and Layer 4    |

- Use Cases:
  1. An application has been deployed on multiple Amazon EC2 instances across **three private subnets**. How do make accesible the application to internet-based clients with the least amount of administrative effort ==> Placing them application instances behind an internet-facing Elastic Load Balancer. The way you add instances in private subnets to a public facing ELB is adding NAT Gateway/Instance in the public subnets in the same AZs as the private subnets to the ELB.
  2. A company has deployed a third-party virtual firewall appliance from the AWS Marketplace in an inspection VPC. How to integrate a web application (deployed in a public Sunet) with the appliance to inspect all traffic to the application before the traffic reaches the web server ==> Gateway Load Balancers enable you to manage virtual appliances, such as firewalls, intrusion detection and prevention systems, and deep packet inspection systems. It combines a transparent network gateway (that is, a single entry and exit point for all traffic) and distributes traffic while scaling your virtual appliances with the demand.

![elb diagram](https://img-c.udemycdn.com/redactor/raw/test_question_description/2021-02-25_10-09-08-4d552faa7e6a02f1057665490b64d36b.jpg)

#### Application Load Balancer (ALB)

![Application Load Balancer](https://d1.awsstatic.com/Digital%20Marketing/House/1up/products/elb/Product-Page-Diagram_Elastic-Load-Balancing_ALB_HIW%402x.cb3ce6cfd5dd549c99645ed51eef9e8be8a27aa3.png)

- Best suitable for protocol HTTP, HTTPS, WebSocket | Layer 7 (Application layer)
- Routes traffic based on request content (hostname, request path, params, headers, source IP etc.).
- Use Case: It is **Intelligent** and can send specific requests to specific servers.

#### Network Load Balancer (NLB)

![Network Load Balancer](https://d1.awsstatic.com/Digital%20Marketing/House/1up/products/elb/Product-Page-Diagram_Elastic-Load-Balancing_NLB_HIW%402x.2f8ded8b565042980c4ad5f8ec57d6b2fafe54ba.png)

- Best suitable for protocol TCP, UDP, TLS | Layer 4 (Transport layer)
- Use case: when extreme performance is required: Handle **volatile workloads** and **extreme low-latency**. Static IP Address.

#### Gateway Load Balancer (GLB)

![Gateway](https://d1.awsstatic.com/Digital%20Marketing/House/1up/products/elb/Product-Page-Diagram_Elastic-Load-Balancing_GWLB_HIW%402x.58547db68b537b4aa4b0cdf7e593a6415d588a09.png)

- Thirdparty appliances, virtual applications e.g. firewalls | Layer 3
- Automatically scales virtual appliances based on demand.

#### Classic Load Balancers (Previous Generation)

- It can operate at both Layer 7 (Application layer) and Layer 4 (Transport layer).
- Use Case: Test & Dev to keep costs low.
- It is not very intelligent — it can’t route traffic based on content like Application Load Balancers.

### ASG (AutoScaling Group)

![ASG](https://d1.awsstatic.com/product-marketing/AutoScaling/aws-auto-scaling-how-it-works-diagram.d42779c774d634883bdcd0463de7bd86f6e2231d.png)

- Monitors and scales applications to optimise performance and costs.
- It can be used across a number of **different services** including EC2 instances and Spot Fleets, ECS tasks, Aurora replicas and DynamoDB tables.
- Autoscaling **across different AZs empowers High Availability** for instances or services.
  - Exam tip: ASG cannot created instances across different Regions.
- Instances are created in ASG using **Launch Configuration (Legacy) or Launch Template (Recommended option)**
  - You can create ASG that launches both Spot and On-Demand Instances or multiple instance types using launch template, not possible with launch configuration.
  - You cannot change the launch configuration for an ASG, you must create a new launch configuration and update your ASG with it.
- You can add **Lifecycle Hooks** to ASG to perform custom action during:
  1. scale-out to run script, install softwares and send complete-lifecycle-action command to continue
  2. scale-in e.g. download logs, take snapshot before termination
- Use Case: How to increase High Availability for Web Applications running on AWS
  1. Enable ASG to add and remove instances
  2. Configure ASG to create instances **across multiple availability zones**
  3. Distribute the traffic load across the different AZs by using an ELB: NLB (layer 4) or ALB (layer 7)

#### Scaling options

Auto Scaling offers both dynamic scaling and predictive scaling options:

##### Dynamic Scaling

- Dynamic scaling scales the capacity of your Auto Scaling group **as traffic changes occur, based on demand**.
- Types of Dynamic Scaling Policies => Increase and decrease the current capacity of the group based on:
  - `Target tracking scaling`: Using **AWS CloudWatch metric with a target value** (it can combine more than one target). Health checks are performed to ensure resource level is maintained. **Most cost-effective**.
    - Use Case:
      1. A company runs an internal browser-based application. The application runs on Amazon EC2 instances behind an Application Load Balancer. The instances run in an Amazon EC2 Auto Scaling group across multiple Availability Zones. The Auto Scaling group scales up to 20 instances during work hours, but scales down to 2 instances overnight. Staff are complaining that the application is very slow when the day begins, although it runs well by midmorning. How should the scaling be changed to address the staff complaints and keep **costs to a minimum**?
         - Though this sounds like a good use case for scheduled actions, using scheduled scaling will have a fixed number of instances (e.g. 20) running regardless of actual demand. A better option to be more cost effective is to use a target tracking action that triggers at a lower CPU threshold.
      2. A web application is being deployed on an Amazon ECS. The application is expected to receive a large volume of traffic initially. The company wishes to ensure that performance is good for the launch and that costs reduce as demand decreases
         - Use Amazon ECS Service Auto Scaling with target tracking policies to scale when an Amazon CloudWatch alarm is breached. A Target Tracking Scaling policy increases or decreases the number of tasks that your service runs based on a target value for a specific metric.
  - `Step scaling`: A set of scaling adjustments, known as _step adjustments_, that vary based on the size of the alarm breach.
    - CloudWatch alarm `CPUUtilization` (60%-80%)- add 1, (>80%) - add 3 more, (30%-40%) - remove 1, (<30%) - remove 2 more
  - `Simple scaling`: A `single scaling adjustment`, with a `cooldown period` between each scaling activity.
    - CloudWatch alarm CPUUtilization (>80%) - add 2 instances.

##### Predictive scaling

Predictive is **only available for EC2** auto scaling groups and the scaling can work in a number of ways:

- Set `Maximum Capacity`: You specify minimum and maximum instances or desired capacity required and EC2 autoscaling manages the progress of creating/terminating based on what you have specified. min <= desired <= max

- Scale Based on a `Schedule`: Scaling performed as a function of time to reflect forecasted load. For example, if you know there will be increased load on the application at 9am every morning you can choose to scale at this time.
  - Use Case: A company runs an application using an Amazon EC2 Auto Scaling group behind an ALB. When running month-end reports on a specific day and time each month the application becomes unacceptably slow. Amazon CloudWatch metrics show the CPU utilization hitting 100%.
    - The best solution ==> Configure an EC2 Auto Scaling scheduled scaling policy based on the monthly schedule. In this case the scaling action can be scheduled to occur just prior to the time that the reports will be run each month.

- Scale based on `Load forecasting`: Auto Scaling analyses the history of your applications load for up to 14 days and then uses this predict to the load for the next 2 days.

### Lambda

- FaaS (**Function as a Service**), Serverless. You don’t have to worry about OS or scaling (scale on demand)
  - Concurrency is the number of in-flight requests your AWS Lambda function is handling at the same time. For each concurrent request, Lambda provisions a separate instance of your execution environment. As your functions receive more requests, Lambda automatically handles scaling the number of execution environments until you reach your account's concurrency limit. By default, Lambda provides your account with a total concurrency limit of 1,000 across all functions in a region.
- Lambda function supports many languages such as Node.js, Python, Java, C#, Golang, Ruby, etc.
- It is cheaper than EC2 because there is **no charge when your code is not running**. What determines price for Lambda?
  - Number of Request (Free Tier: 1 million requests per month)
  - Duration (Execution) and resource (memory) usage
  - Additional Charges: if your lambda uses other AWS services or transfers data. For example, If your lambda function reads and writes data to or from Amazon S3, you will be billed for the read/write requests and the data stored in Amazon S3
- AWS Lambda integrates with other AWS services to invoke functions or take other actions (Check examples [here](https://aws.amazon.com/lambda/)) ==> It can take as input one AWS Service (e.g S3 file), process/analyze/transform its data and put the output in another or the same AWS Service (e.g. S3 or DynamoDB), without requiring any sort of File System.
- Method of Invocation:
  - `Lambda polling`: For services that generate a **queue or data stream**
    - Services: Amazon Managed Streaming for Apache Kafka, Self-managed Apache Kafka, Amazon DynamoDB, Amazon Kinesis, Amazon MQ, Amazon Simple Queue Service
  - `Event-driven`: Some services generate **events (JSON documents) that can invoke your Lambda function**.
    - Synchronous
      - Services: Elastic Load Balancing (Application Load Balancer), Amazon Cognito, Amazon Lex, Amazon Alexa, Amazon API Gateway, Amazon CloudFront (Lambda@Edge), Amazon Kinesis Data Firehose, AWS Step Functions
      - Common Use Case: Respond to incoming HTTP requests using API Gateway.
    - Asynchronous
      - Services: Amazon Simple Storage Service, Amazon Simple Notification Service, Amazon Simple Email Service, AWS CloudFormation, Amazon CloudWatch Logs, Amazon CloudWatch Events, AWS CodeCommit, AWS Config, AWS IoT Events
      - In response to resource **lifecycle events**, such as with Amazon Simple Storage Service (Amazon S3).
      - **On a Schedule** with Amazon EventBridge (CloudWatch Events).

- Lambda limitations:
  - Execution time **can’t exceed 15 min** (900 seconds)
  - Min required memory is 128MB and can go **till 10GB** with 1-MB increment
  - `/temp` directory size to download file **can’t exceed 512 MB**
  - **Max environment variables size can be 4KB**
  - Compressed `.zip` and uncompressed code can’t exceed **50MB and 250MB respectively**



- Uses Case: A a new service that will use an Amazon API Gateway API on the frontend is being designed. The service will need to persist data in a backend database using key-value requests. Which combination of AWS services would meet the most cost efective and scalable solution?
  - Amazon RDS or Dynamo DB => DynamoDB is built for key-value data storage requirements (No-SQL). Moreover, it is serverless and easily scalable.
  - For EC2, AWS fargate, Lambda => Lambda can perform the computation and store the data in an Amazon DynamoDB table (as long as it does not go over its limitations). Lambda can scale concurrent executions to meet demand easily.

## Containers

### Elastic Container Registry (ECR)

- It is Docker Registry to pull and push Docker images, managed by Amazon.

### Elastic Container Service (ECS)

- It is a highly scalable, high performance container management service that supports Docker containers magement and lifecyle.
- Using API calls you can launch and stop container-enabled applications, query the complete state of clusters, and access features like security groups, Elastic Load Balancing, EBS volumes and **IAM roles**.
- Amazon ECS can be used to schedule the placement of containers across clusters based on resource needs and availability requirements.
- There is no additional charge for Amazon ECS. You pay for:
  - Resources created with the EC2 Launch Type (e.g. EC2 instances and EBS volumes).
  - The number and configuration of tasks you run for the Fargate Launch Type.
- Terminology:
  - Cluster: Logical Grouping of EC2 Instances
  - Container Instance: EC2 instance running the ECS agent
  - Task Definition: Blueprint that describes how a docker container should launch
  - Task: A running container using settings in a Task Definition
  - Service: Defines long running tasks – can control task count with Auto Scaling and attach an ELB

![Launch Type](https://digitalcloud.training/wp-content/uploads/2022/01/amazon-ecs-ec2-vs-fargate-1.jpeg)

An Amazon ECS launch type determines the type of infrastructure on which your tasks and services are hosted.

| Amazon EC2                              | Amazon Fargate        |
| ----------------------------------------| ----------------------|
| You can explicitly provision EC2 instances | **Serverless**. The control plane asks for resources and Fargate automatically provisions.|
| You’re responsible for upgrading, patching, care of EC2 pool | Fargate provisions compute as needed |
| You must handle cluster optimization | Fargate handles customer optimizations |
| More granular control over infrastructure | Limited control, as infrastructure is automated |
| Support DockerHub, ECR and Self-Hosted Registries | Only supports DockerHub, ECR |
| Cheaper | Costlier |
| **Good for predictable, long running tasks** | **Good for variable, short running tasks.** |

### Elastic Container Service for Kubernetes (Amazon EKS)

- Amazon also provide the Elastic Container Service for Kubernetes (Amazon EKS) which can be used to deploy, manage, and scale containerized applications using Kubernetes on AWS.
- Use Case: A company runs containerized applications in an on-premise data center (e.g. OpenShift). The company is planning to deploy containers to AWS and the architect has mandated that the same configuration and administrative tools must be used across all containerized environments ==> Applications running on Amazon EKS are fully compatible with applications running on any standard Kubernetes environment, whether running in on-premises data centers or public clouds (or hybrid).

### ECS vs EKS

| ECS                                     | EKS                   |
| ----------------------------------------| ----------------------|
| AWS-specific platform that supports Docker Containers | Compatible with upstream Kubernetes so it’s easy to lift and shift from other Kubernetes deployments |
| Considered simpler and easier to use | Considered more feature-rich and complex with a steep learning curve |
| Leverages AWS services like Route 53, ALB, and CloudWatch | A hosted Kubernetes platform that handles many things internally |
| “Tasks” are instances of containers that are run on underlying compute but more of less isolated | “Pods” are containers collocated with one another and can have shared access to each other |
| Limited extensibility | Extensible via a wide variety of third-party and community add-ons. |

- [Types of Node Groups](https://docs.aws.amazon.com/eks/latest/userguide/eks-compute.html)
  - Self-managed: You bring your own servers and have more control of the server. You have to manage it yourself though.
  - Managed: AWS manages the servers for you. You just have to specify some configurations of server instance types.
  - Fargate (serverless): AWS manages even more of the server for you. You don't even have to think about instance types. Just tell EKS how much RAM and CPU you need and that's it.

## Application_Integration

Go to [Index](#index)

Services that help to **decouple components**.

### Amazon Simple Queue Service (SQS)

- Keywords: Pulling Messages, Only 1 consumer

![SQS](https://d1.awsstatic.com/product-page-diagram_Amazon-SQS%402x.8639596f10bfa6d7cdb2e83df728e789963dcc39.png)

- Fully managed, distributed, scalale **Message Queue** service that can be used for micro-services, distributed applications and serverless applications. In other words, **a temporary repository for messages that are awaiting processing**.
- It **decouples infraestructure** (acts like a buffer between) the software component producing/saving data and the component receiving data for processing.
- Specification for Standard SQS:
  - SQS guarantees that your **messages will be processed at least once**.
  - Can have unlimited number of messages waiting in queue however, there is a quota of 120,000 for the number of inflight messages for a standard queue and 20,000 for a FIFO queue
    - Messages are inflight ==> consuming by component, but have not yet been deleted from the queue.
  - Default retention period is 4 days (min 1 min. and max 14 days)
  - Can send message upto 256KB in size (To send messages larger than 256 KB -up tp 2GB- using library allows you to send an Amazon SQS message that contains a reference to a message payload in Amazon S3)
  - Unlimited throughput and low latency (<10ms on publish and receive)
  - **Can have duplicate messages** (At least once delivery)
  - **Can have out of order messages** (best effort ordering)

![producer-consumer](https://betterdev.blog/app/uploads/2021/08/sqs-messaging.png)

- One or Multiple Producers can push messages to The Queue. **Only one consumer** will read an individual message (**Pull message from the Queue**)
  - Consumer/Producers Examples: EC2 instance, Lambda, ECS task, etc.
  - Exam Tip: Amazon SQS vs SNS:
    - SQS pull-based (polling). Only 1 Consumer
    - SNS Push-based. Multiple Consumers
  - Polling types:
    - Short Polling (`ReceiveMessageWaitTimeSeconds` = 0) - Keeps polling queue looking for work, even if it’s empty.
    - Long Polling (`ReceiveMessageWaitTimeSeconds` > 0) - Reduces the number of empty responses by allowing Amazon SQS to wait until a message is available before sending a response to a ReceiveMessage request, helps to reduce the cost.
  - `Visibility Timeout` — **Immediately after a message is received, it remains in the queue. Amazon SQS doesn't automatically delete the message because it is a distributed system**
    - To prevent other consumers from processing the message again, Amazon SQS sets a `visibility timeout`, a period of time during which Amazon SQS prevents other consumers from receiving and processing the message. The default visibility timeout for a message is 30 seconds.
    - Exam Tip: If you are getting messages delivered twice, the cause could be your visibility timeout is too low.
- Use Cases:
  1. A new application will run across multiple Amazon ECS tasks. Front-end application logic will process data and then pass that data to a back-end ECS task to perform further processing and write the data to a datastore. How to reduce-interdependencies so failures do no impact other components? ==> Create an Amazon SQS queue and configure the front-end to add messages to the queue and the back-end to poll the queue for messages.
  2. A web application allows users to upload photos. The application offers two tiers of service: free and paid. Photos uploaded by paid users should be processed before those submitted using the free tier. The photos are uploaded to an Amazon S3 bucket which uses an event notification to send the job information to Amazon SQS. How to meet the requirements ? ==> AWS recommend using separate queues when you need to provide prioritization of work. The logic can then be implemented at the application layer to prioritize the queue for the paid photos over the queue for the free photos.
  3. A company is working with a partner that has an application that must be able to send messages to one of the company’s Amazon SQS queues. The partner company has its own AWS account. How can least privilege access to the partner be provided? ==> Amazon SQS supports resource-based policies. The best way to grant the permissions using the **principle of least privilege** is to use a resource-based policy attached to the SQS queue that grants the partner company’s AWS account the `sqs:SendMessage` privilege.
  4. Integration: It can be configured to scale EC2 instances using Auto Scaling based on the number of jobs waiting in the SQS queue. It can be used the backlog per instance metric with the target value being the acceptable backlog per instance to maintain.


#### Types of Queues

There are two types of queues: Standard & FIFO.

##### Standard Queues

- Default queue type.
- Nearly **unlimited number of API calls per second**.
- Guarantees message delivered at least once.
- Occasionally more than one copy of a message might be delivered out of order. However, standard queues provide **best-effort ordering** which ensures that messages are generally delivered in the same order as they are sent.

##### FIFO Queues

- First in First Out => The **order in which the messages are sent is preserved**.
- Has high throughput
- **Limits: support up to 3,000 transactions** per API batch call.
- **Processed exactly once** and duplicates are not introduced to the queue.

##### Dead-Letter Queue

- The main task of a dead-letter queue is **handling message failure**.
  - Messages are moved to the dead-letter queue when the `ReceiveCount` for a message exceeds the `maxReceiveCount` for a queue.
- It is not a queue type; it is a standard or FIFO queue that has been specified as a dead-letter queue in the configuration of another standard or FIFO queue.
  - Dead-letter queues will break the order of messages in FIFO queues.

### Amazon Simple Notification Service (SNS)

- Keywords: Pushing Messages, Multiple consumer (subscribers)

![A2A](https://d1.awsstatic.com/Product-Page-Diagram_Amazon-SNS_Event-Driven-SNS-Compute%402x.03cb54865e1c586c26ee73f9dff0dc079125e9dc.png)

![producer-consumer](https://betterdev.blog/app/uploads/2021/08/sns-messaging.png)

- Managed Messaging Service that allows you **push** (Instantaneous) **messages on SNS topic and all topic subscribers receive those messages**.
- Consumers needs to subscribe to the topic to receive the messages. Then, one topic can support deliveries to multiple endpoint types:
  - Lambda function
  - SQS ==> Fanout pattern: Messages sent to the SNS topic and then forwarded to multiple SQS queues that are subscribed to the topic. The messages can then be processed by different consumer applications from these queues.
  - HTTP endpoint
  - Mobile phone – via SMS
  - Mobile app – via push notification
  - Email
  - Kinesis Firehose
- Highly available as all messages stored across multiple regions.
- You can setup a Subscription Filter Policy which is JSON policy to send the filtered messages to specific subscribers.
- Inexpensive, pay-as-you-go model with no up-front costs.

### Amazon MQ

![Amazon MQ](https://d1.awsstatic.com/products/mq/Product-Page-Diagram_Amazon-MQ.17994587d6bf1579ec8c87db2bb3c5a6d485926e.png)

- It Fully managed service for open-source **message brokers** for Apache **ActiveMQ and RabbitMQ** that streamlines setup, operation, and management of message brokers on AWS.
- It allows software systems, which often **use different programming languages on various platforms, to communication and exchange information**.
- It can be configured in HA mode across to AZs.
- Exam Tip: Amazon MQ is similar to SQS but is used to Migrate existing applications (using already ActiveMQ and RabbitMQ) into AWS . **SQS should be used for new applications being created** in the cloud.

### Amazon Comprehend

- It is a **Natural Language Processing (NLP)** service that uses machine learning to find insights and relationships in text.

![Amazon Comprehend](https://img-c.udemycdn.com/redactor/raw/practice_test_question_explanation/2022-08-27_11-07-36-05ab4438c3d5079c3dad300424cbea3b.jpg)

### Amazon EventBridge

- Amazon EventBridge is a serverless, fully managed, and scalable **event bus that enables integrations** between AWS services, Software as a services (SaaS), and your applications. It does not require **writing custom code** (LEAST operational overhead that use Lambda for example).
- How:
  - Event sources (SaaS partner, AWS Services, or your own applications.) emit events as real-time change in a system, data, or environment.
  - Event Bus: pipeline that receives events. Rules associated with the event bus evaluate events as they arrive. Each rule checks whether an event matches the rule’s criteria.
  - Rules: matches incoming events and sends them to targets for processing (using same API as Amazon CloudWatch Events). A single rule can send an event to multiple targets, which then run in parallel.
  - A target is a resource or endpoint that EventBridge sends an event to when the event matches the event pattern defined for a rule

![eventbridge](https://d1.awsstatic.com/product-marketing/EventBridge/Product-Page-Diagram_Amazon-EventBridge%402xa.2ef6accf0d9ff4eb0856422599406e022b552073.png)

- Use Case: A reporting team receives files each day in an Amazon S3 bucket. The reporting team manually reviews and copies the files from this initial S3 bucket to an analysis S3 bucket each day at the same time to use with Amazon QuickSight. Additional teams are starting to send more files in larger sizes to the initial S3 bucket. The reporting team wants to move the files automatically to the analysis S3 bucket as the files enter the initial S3 bucket. The reporting team also wants to use AWS Lambda functions to run pattern-matching code on the copied data. In addition, the reporting team wants to send the data files to a pipeline in Amazon SageMaker Pipelines.
  - Configure S3 replication between the S3 buckets. Configure the analysis S3 bucket to send event notifications to Amazon EventBridge. Configure an ObjectCreated rule in EventBridge. Configure Lambda and SageMaker Pipelines as targets for the rule

### Amazon SageMaker

- It allows you to build, train, and deploy **machine learning models** for any use case with fully managed infrastructure, tools, and workflows

### AWS Data Exchange

- It allows you to gain **access to third party data sets across different types of industries** like Automotive, Financial Services, Gaming, Healthcare & Life Sciences, Manufacturing, Marketing, Media & Entertainment or Retail.

### AWS Private 5G

- AWS Private 5G is a managed service that makes it easy to deploy, operate, and scale your own private cellular network, with all required hardware and software provided by AWS.

![Private 5G](https://d1.awsstatic.com/reInvent/re21-pdp-tier1/private-5g/AWS-Private-5G-HIW%402x.368b813d6263444746862d2a0dad345efb0ccf5d.png)

### Amazon Athena

- It provides a simplified, flexible way to analyze **petabytes of data** where it lives. Analyze data or build applications from an Amazon Simple Storage Service (S3) data lake and 30 data sources, including on-premises data sources or other cloud systems using SQL or Python.
- It is a managed services built on open-source Trino and Presto engines and Apache Spark frameworks

![Athena](https://d1.awsstatic.com/products/athena/product-page-diagram_Amazon-Athena-Connectors%402x.867e3023b0e6b33862d65aa8e786cce46b88cb61.png)

### Amazon Transcribe

- It converts audio input into text, which opens the door for various text analytics applications on voice input. For instance, by using Amazon Comprehend on the converted text data from Amazon Transcribe, customers can perform sentiment analysis or extract entities and key phrases.

## Storage

Go to [Index](#index)

### S3 (Simple Storage Service)

- Keywords: **Object Storage**, Concurrency, Archiving, Lyfecle Management, Versioning, Encryption, Static Website Hosting

![s3](https://d1.awsstatic.com/s3-pdp-redesign/product-page-diagram_Amazon-S3_HIW.cf4c2bd7aa02f1fe77be8aa120393993e08ac86d.png)

- Storage service that is highly scalable, secure and performant. It allows concurency (more than one compute unit can access to the files at the same time).
- It is OBJECT BASED storage (suitable for files). It does not allow to install Operation System (different with EBS for example).
- S3 Object is made up of:
  - `Key` → Name of the object, full path of the object in bucket e.g. /movies/comedy/abc.avi
    - S3 console show **virtual folders based on key**.
  - `Value` → data bytes of object (photos, videos, documents, etc.)
  - `Version ID` → version object (if versioning is enabled)
  - `Metadata`
  - Sub-resources (Access Control Lists & Torrent)
- There is unlimited storage, but individual files uploaded can be from **0 bytes to 5TB**.
  - **Best practice:  use multi-part upload for Object size > 100MB**
  - When you upload a file to S3, you receive a HTTP `200` code if the file upload is successful.
- S3 is a UNIVERSAL NAMESPACE, so **bucket names need to be globally unique**. The reason why is because it creates a **web address (DNS name)** with the buckets name in it.
  - When you view Buckets you view them globally but you have buckets in individual regions.

```sh
https://<bucket-name>.s3.<aws-region>.amazonaws.com
#or
https://s3.<aws-region>.amazonaws.com/<bucket-name>
```

- S3 Consistency
  - Delivers **strong read-after-write consistency for PUTS and DELETES** of objects, for both new objects and for updates to existing objects. This means once there is a successful write, overwrite or delete — the next **read request automatically receives the latest version of the object**.
  - **Updates to a single key are atomic**. For example, if you PUT to an existing key from one thread and perform a GET on the same key from a second thread concurrently, you will get either the old data or the new data, but **never partial or corrupt data**.
- In S3 you pay for the following things:
  - Storage
  - Requests and Data Retrievals
  - Storage Management Pricing
  - Data Transfer Pricing
  - Transfer Acceleration
  - Cross Region Replication Pricing
- We can change storage class and encryption on the fly

#### Optional features

- **Enable `S3 Versioning` and `MFA` to protect against accidental delete of S3 Object**.
- **Enable `S3 Object Lock` to store object using write-once-read-many (WORM) model** to prevent objects from being deleted or overwritten for a fixed amount of time (`Retention period`) or indefinitely (`Legal hold`).
  - Amazon S3 currently does not support enabling object lock after a bucket has been created.
  - Retention:
    - Each version of object can have different retention-period.
    - S3 has two types of retention mode:
      - `Governance Mode` → Users can’t overwrite , delete or alter the object version locked unless they have special permissions (permissions requires to be granted).
      - `Compliance Mode` → A protected object version can’t be overwritten or deleted by ANY user including the root user during its retention period.
- `Glacier Vault Lock` → enforce compliance controls on individual S3 Glacier vaults using a Vault Lock policy.
- You can host **Static websites on S3 bucket** consists of HTML, CSS, client-side JavaScript, and images.
  - Requirements:
    - Enable Static website hosting and Public access for S3 to avoid 403 forbidden error.
    - Add CORS Policy to allow cross origin request.
  - Exam Tip: It is not used for dynamic websites (eg. AJAX) or websites which require database, for ex: Wordpress...etc.
  - Use Case: A company has deployed a new website on Amazon EC2 instances behind an Application Load Balancer (ALB). Amazon Route 53 is used for the DNS service. The company has asked to create a backup website with support contact details that users will be directed to automatically if the primary website is down. How should be deployed this solution cost-effectively? ==> The most cost-effective solution is to create a static website using an Amazon S3 bucket and then use a **failover routing policy** in Amazon Route 53. With a failover routing policy users will be directed to the main website as long as it is responding to health checks successfully.

```sh
https://<bucket-name>.s3-website[.-]<aws-region>.amazonaws.com
```

- `S3 Select` or `Glacier Select` can be used to retrieve subset of data from S3 Objects using SQL query. S3 Objects can be CSV, JSON, or Apache Parquet. GZIP & BZIP2 compression is supported with CSV or JSON format with server-side encryption.
  - Allows you to save money on data transfer and increase speed.
- Using `Range` HTTP Header in a GET Request to download the specific range of bytes of S3 object, known as Byte Range Fetch.
- High Availability: Enable `S3 Cross-Region Replication` for asynchronous **replication of object across buckets in another region**.
  - Requirement:
    - An existing bucket to Replicate data
    - Versioning enabled on both SOURCE & DESTINATION bucket.
  - If enabled, existing objects are not replicated automatically, only subsequent updated files (new objects).
  - You can have this enabled for the entire bucket or just for specific prefixes.
  - Delete markers ARE NOT replicated.
- Enable `Server access logging` for logging object-level fields object-size, total time, turn around time, and Http referrer. Not available with CloudTrail.
- Use `VPC S3 gateway endpoint` to access S3 bucket within AWS VPC to reduce the overall data transfer cost.
- Enable `S3 Transfer Acceleration` for faster transfer (high throughput) to S3 bucket (mainly uploads).

#### Integrations

##### CloudFront to authenticate request to s3: Origin Access Control (OAC) and Origin Access Identity (OAI)

- OAC is the recoemmended option
- It is a function of CloudFront distribution that you can enable when you select **S3 buckets as origin**. If you don’t use an OAI/OAC, the S3 bucket must allow public access for downloading objects.
  - It makes faster **cached** content delivery (mainly reads) over long distances between your client and S3.
  - **Restrict the access of S3 bucket endpoint directly**, only making it possible through CloudFront only endpoints

```sh
#Not available with S3 website endpoints
app-private-bucket-stormit.s3.eu-central-1.amazonaws.com/pics/logo.png
#Available with CloudFront endpoints
d2whx7jax6hbi5.cloudfront.net/pics/logo.png
```

![Origin Access Identity](https://img-c.udemycdn.com/redactor/raw/test_question_description/2021-05-18_05-32-57-0cec77f550d1e2e6100046094949925b.jpg)

##### s3 + Athena

- Use `AWS Athena` (Serverless Query Engine) to perform **analytics directly against S3 objects using SQL** query and save the analysis report in another S3 bucket.
  - Use Case: one time SQL query on S3 objects, S3 access log analysis, serverless queries on S3, IoT data analytics in S3, etc.

##### Amazon S3 Event Notifications

- Enable `S3 event notification` feature to emit notifications when certain events happen in your S3 bucket (eg: push events e.g. `s3:ObjectCreated:\*`) and send to one of the following Destinations:
  - Amazon SNS topic
  - Amazon SQS queue (FIFO queue is not supported, use Event Brdige instead)
  - AWS Lambda function
- It is possible that you receive single notification for two writes to non-versioned object at the same time. Enable versioning to ensure you get all notifications.

##### S3 Object Lambda

- Enable and configure `S3 Object Lambda`, to add your own code to S3 GET, HEAD, and LIST requests to modify and process data as it is returned to an application.
- You can use custom code to modify the data returned by S3 GET requests to filter rows, dynamically resize images, redact confidential data, and much more.

#### S3 Tiered Storage (Storage Classes)

- You can upload files in the same bucket with different Storage Classes like S3 standard, Standard-IA, One Zone-IA, Glacier etc.
- You can setup `S3 Lifecycle Rules` to transition current (or previous version) objects to cheaper storage classes or delete (expire if versioned) objects after certain period of time. Possible transitions are whows in the following diagrama

![transition](https://docs.aws.amazon.com/images/AmazonS3/latest/userguide/images/lifecycle-transitions-v2.png)

| S3 Storage Class                   | Durability | Availability | AZ  | Min Fee for Data Storage | Retrieval Time                                           | Retrieval fee |
| ---------------------------------- | ---------- | ------------ | --- | ------------ | -------------------------------------------------------- | ------------- |
| S3 Standard (General Purpose)      | 11 9’s     | 99.99%       | ≥3  | **N/A**  `*` | milliseconds                                             | **N/A**            |
| S3 Intelligent Tiering             | 11 9’s     | 99.9%        | ≥3  | 30 days      | millisecond                                              | **N/A**       |
| S3 Standard-IA (Infrequent Access) | 11 9’s     | 99.9%        | ≥3  | 30 days      | milliseconds                                             | per GB        |
| S3 One Zone-IA (Infrequent Access) | 11 9’s     | 99.5%        | **1**  | 30 days      | milliseconds                                             | per GB        |
| S3 Glacier Instant Retrieval       |  11 9’s    |  99.99%     |  ≥3 |  **90 days**    | milliseconds  | per GB
| S3 Glacier Flexible Retrieval      |  11 9’s    |  99.99%     |  ≥3 |  **90 days**    | **minutes** to 12 hours | per GB
| S3 Glacier Deep Archive            |  11 9’s    |  99.99%     |  ≥3 |  **180 days**    | 12 **hours** - 48 hours | per GB

`*` Although there is not minimum time for storage, a Lifecycle requires at least 30 days before you transition objects from the S3 Standard

- Types:
  - `Standard`: **General purpose** storage for any type of frequently used data very high availability, and fast retrieval.
  - `Intelligent Tiering`: Analyze your Object’s usage and move them to the appropriate cost-effective storage class automatically, without performance impact.
    - Use case: automatic cost savings for data with **unknown/changing access patterns or frequency**. But you can use S3 Intelligent-Tiering as the default storage class for most workloads.
  - `Standard-IA`: Cost effective for **infrequent access files** which **cannot be recreated**.
    - For data that is not accessed very frequently — but once it is accessed it needs to be retrieved rapidly.
    - It is cheaper than standard S3, but you do get charged a retrieval fee.
  - `One-Zone IA`(also called S3 RRS): Cost effective for **infrequent access** files which **can be recreated**.
    - Low cost option for data that is not accessed frequently and does not require the redundancy, **if the zone fails, we loose the data**.
    - Use case: re-creatable infrequently accessed data that needs milliseconds access.
  - `S3 Glacier Instant Retrieval`: Amazon S3 Glacier Instant Retrieval is an archive storage class that delivers the **lowest-cost storage for long-lived data** that is rarely accessed and requires retrieval in **milliseconds**
    - With S3 Glacier Instant Retrieval, you can save up to 68% on storage costs compared to using the S3 Standard-Infrequent Access (S3 Standard-IA) storage class, when your data is accessed once per quarter.
  - `S3 Glacier Flexible Retrieval` (Formerly S3 Glacier): S3 Glacier Flexible Retrieval delivers low-cost storage, up to 10% lower cost (than S3 Glacier Instant Retrieval), for archive data that is accessed 1—2 times per year and is retrieved asynchronously. For archive data that does not require immediate access but needs the flexibility to retrieve large sets of data at no cost, such as **Backup or Disaster recovery use cases**.
  - `Glacier Deep Archive`: **Cheapest choice** for Long-term storage of large amount of data for compliance.

- Use Case:

  1. A team are planning to run analytics jobs on log files each day and require a storage solution. The size and number of logs is unknown and data will persist for 24 hours only. What is the MOST cost-effective solution?
     - S3 standard is the best choice in this scenario for a short term storage solution. In this case the size and number of logs is unknown and it would be difficult to fully assess the access patterns at this stage. Therefore, using S3 standard is best as it is cost-effective, provides immediate access, and there are no retrieval fees or minimum capacity charge per object.
  2. A video production company is planning to move some of its workloads to the AWS Cloud. The company will require around 5 TB of storage for video processing with the maximum possible I/O performance. They also require over 400 TB of extremely durable storage for storing video files and 800 TB of storage for long-term archival. Which combinations of services would meet these requirements?
     - Amazon EC2 instance store for maximum performance, Amazon S3 for durable data storage, and Amazon S3 Glacier for archival storage.
  3. Application log files needs to backup from an online ecommerce store to Amazon S3. It is unknown how often the logs will be accessed or which logs will be accessed the most. From the following options "S3 Standard-Infrequent Access (S3 Standard-IA)", "S3 One Zone-Infrequent Access (S3 One Zone-IA)", "S3 Intelligent-Tiering" and "S3 Glacier". Which is the most cost effective? ==> "S3 Intelligent-Tiering" It works by storing objects in two access tiers: one tier that is optimized for frequent access and another lower-cost tier that is optimized for infrequent access. The other options are not valid, because they charge retrieval fees and the accesibility is unknown.
  4. A company migrated a two-tier application from its on-premises data center to AWS Cloud. A Multi-AZ Amazon RDS for Oracle deployment is used for the data tier, along with 12 TB of General Purpose SSD Amazon EBS storage. With an average document size of 6 MB, the application processes, and stores documents as binary large objects (blobs) in the database. Over time, the database size has grown, which has reduced performance and increased storage costs. A highly available and resilient solution is needed to improve database performance. Which solution could meet these requirements MOST cost-effectively?
     - Set up an Amazon S3 bucket. The application should be updated to use S3 buckets to store documents. Store the object metadata in the existing database
  5. An application runs on Amazon EC2 Linux instances. The application generates log files which are written using standard API calls. A storage solution is required that can be used to store the files indefinitely and must allow concurrent access to all files. Which storage service meets these requirements and is the MOST cost-effective? ==> The application is writing the files using API calls which means it will be compatible with Amazon S3 which uses a REST API and it is the most cost-effective solution that EFS.


#### Sharing S3 buckets Across Accounts

For multiple accounts within the same organisation, to share S3 buckets among account:

- Bucket policy & IAM — applies to entire bucket, but programmatic access only.
- Using bucket ALCs & IAM — can apply to individual objects — programatic access only.
- Cross Account IAM roles — programatic and console access.

#### S3 Security

- By default newly created buckets are private, but you can make them public if needed, for example - you would need to make it public for static web hosting purposes.

#####  Access

###### Access Control lists (deprecated)

- Access Control Lists can be for **individual files**. Can grant basic read and write permissions at an object level (not just whole bucket)
- For example: use if there is a file in a bucket you don’t want everyone to have access to.

###### Bucket policy (recommended)

- S3 Bucket Policies are JSON based policy for complex access rules at user, account, folder, and object level
- Bucket policies are **bucket wide**. This works at budget levels not individual file level.

###### S3 (Pre-)Signed URLS

- Used to secure content so only authorised people are able to access (upload or download object data) **temporarly** it (it requires an expiration date and time defined).
- It can be generated from CLI or SDK (can’t from web) and has an LIMITED LIFETIME (e.g. 5 min).

```sh
aws s3 presign s3://mybucket/myobject --expires-in 300
```

- Use Case: An application upgrade caused some issues with stability. The application owner enabled logging and has generated a 5 GB log file in an Amazon S3 bucket. The log file must be securely shared with the application vendor to troubleshoot the issues ==> Generate a presigned URL and ask the vendor to download the log file before the URL expires

##### Encryption

- `Encryption at Rest (Client Side)` — client encrypt and decrypt the data before sending and after receiving data from S3.
- `Encryption in Transit` — encrypting network traffic (between client and S3) using SSL/TLS.
- `Encryption at Rest (Server Side)` — By default, Amazon S3 encrypts your objects before saving them on disks in AWS data centers and then decrypts the objects when you download them. All new object uploads to Amazon S3 are automatically encrypted at no additional cost and with no impact on performance.
  - Types:
    - `SSE-S3` (Default encryption): S3 Managed Keys (SSE-S3), AWS Managed Keys.
    - `SSE-KMS`: AWS Key Management Service (SSE-KMS) AWS & you manage keys together.
    - `SSE-C`: Customer provided keys — give AWS you own keys that you manage.
  - If you require your data uploads to be encrypted, use the header `x-amz-server-side-encryption` to encrypt the object using specific configuration, for example `"s3:x-amz-server-side-encryption": "AES256"`
- To meet PCI-DSS or HIPAA compliance, encrypt S3 using SSE-C + Client Side Encryption.

#### S3 Versioning

- It acts **like a backup tool** that stores all versions of an object (even writes & deletes).
  - If you delete a file it will still show up in versioning with the delete marker on it.
- `Versioning's MFA Delete capability`, which uses multi-factor authentication, can be used to provide an **additional layer of security**.
- When enabled on your bucket it cannot be disabled — only suspended.
- If you mark a single file as public and then upload a new version of it — the new version is private.
- The size of your S3 bucket is the sum of all files and all versions of those files.

#### S3 Performance

S3 Has extremely low latency

##### Performance limitations

- If you are using KMS (SSE-KMS) to encrypt your objects in S3, you must keep in mind the KMS limits.
  - When you upload a file, you will call `GenerateDataKey` in the KMS API.
  - When you download a file, you will call `Decrypt` in the KMS API.
- Uploading/Downloading will count towards the KMS per second quota, which could affect performance
  - Region-specific, however, it's either 5500, 10000 or 30000 requests our second.
  - accessed through a Network File System (NFS) mount point

##### Improving Performance

- `S3 Prefix` is the part between the bucket name and the filename. You can get better performance by spreading your reads across different prefixes.

  - Use Case: By default, you can get the first byte out of S3 within 100-200 milliseconds. You can also achieve a high number of requests: 3500 PUT/COPY/POST/DELETE and 5500 GET/HEAD requests per second per prefix. Spreading your reads across different prefixes. For Example, If you are using two prefixes, you can achieve 11000 requests per second.

```sh
mybucketname/folder1/subfolder1/myfile.jpg >  /folder1/subfolder1 is the prefix
```

- `Multipart Uploads` -> It splits your file into parts and uploads them in Parallel

  - Recommended for files over 100MB
  - Required for files over 5GB

- For download this is call `S3 Byte Range Fetches` — Parallelises download by specifying byte ranges, which speeds up downloads and can download partial amounts of info.

### AWS Storage Gateway

- Keyword: Hybrid solution, Linux, not re-architecting, S3 replication

![storagegateway](https://d1.awsstatic.com/pdp-how-it-works-assets/product-page-diagram_AWS-Storage-Gateway_HIW@2x.6df96d96cdbaa61ed3ce935262431aabcfb9e52d.png)

- It enables hybrid storage between on-premises environments and the AWS Cloud.
- How?
  - AWS Storage Gateway is installed on site datacenter => Implemented using a VM (VMware or Hyper-V virtual appliance).
  - On premises applications are connected to AWS Storage Gateway
  - It provides low-latency performance by caching frequently accessed data on premises (**local cache**)
  - It replicates data storage securely and durably into Amazon S3 and Glacier.
  - AWS proceses the replicated data in AWS Cloud (ETL, Lifecycle rules, Backups, Migration...).
- Security:
  - Data transfers between gateway appliance and AWS storage is encrypted using SSL.
  - By Default, data stored by AWS Storage Gateway in S3 is encrypted (SSE-S3). Optionally, encrypted KMS-Managed Keys using SSE-KMS.

- Interfaces:

| Storage Gateway  | Interface   | Use Case                                                                                                                             |
| ---------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| File Gateway  | NFS & SMB  | Allow on-prem or EC2 instances to store objects in S3 via NFS or SMB mount points |
| Volume Gateway  | iSCSI (Block Storage) | Use S3 as point on time snapshots of EBS volumen. Two types: Cached (Primary data stored in S3, Store a subset of frequent access data locally) and Stored (Asynchronous replication of on-prem data to S3 AWS, Entire dataset) |
| Tape Gateway     | iSCSI  | Virtual media changer and tape library for use with existing backup software, Archive in Glacier |

![storagegateway_how](https://td-mainsite-cdn.tutorialsdojo.com/wp-content/uploads/2018/12/aws-storage-gateway-768x520.jpg)

- Use Cases:
  1. Storage capacity has become an issue for a company that runs application servers on-premises. The servers are connected to a combination of block storage and NFS storage solutions. The company requires a solution that supports local caching without re-architecting its existing applications.
     - The AWS Storage Gateway Volume gateway should be used to replace the block-based storage systems as it is mounted over iSCSI and the file gateway should be used to replace the NFS file systems as it uses NFS.
  2. A company is investigating methods to reduce the expenses associated with on-premises backup infrastructure (physical backup tapes). It is a requirement that existing backup applications and workflows should continue to function.
     - The AWS Storage Gateway Tape Gateway enables you to replace using physical tapes on premises with virtual tapes in AWS without changing existing backup workflows.

###  Instance Store

- KeyWords: Block Storage, Ephemeral, Fastest storage, Lowest Latency
- Instance Store is an **Ephemeral/temporal block-based** storage physically attached to an EC2 instance
  - **Data persists on instance reboot, data doesn’t persist on stop or termination**
- It can be attached to an EC2 instance only when the instance is launched and cannot be dynamically resized
- Deliver very **low-latency and high random I/O performance**.
- It is the fastest storage that an EC2 instance can have.
- It is included in the price of the EC2 instance so it can also be **more cost-effective than EBS Provisioned IOPS**.

EXAM TIP: If you can afford to lose an instance (i.e. you are **replicating your data, temporal files**) these can be a good solution for high performance/low latency requirements.

### EBS (Elastic Block Store)

- KeyWords: [**Block Storage**](https://aws.amazon.com/what-is/block-storage/), single AZ, RAID, Encryption, Snapshots

![EBS AWS diagram](https://d1.awsstatic.com/product-marketing/Storage/EBS/Product-Page-Diagram_Amazon-Elastic-Block-Store.5821c6ee4297f3c01cba37e304922451c828fb04.png)

- EBS is Persistent and High Available storage volumes for EC2
  - Data persists on EC2 stop or termination
    - When we terminate EC2 instance, it removes EBS volumes automatically.
  - Each Amazon EBS volume is automatically replicated within it's Availability Zone to protect you from component failure.
- It is Block-based storage: It needs to be **mounted to an EC2 instance within the same Availability Zone (Region)** (EBS Volume think like a "USB stick")
  - 1 EBS - 1 EC2. It can be attached to only one EC2 instance at a time in the same AZ (different from EFS ==> 1 EFS - 1..N EC2).
    - Exception: [EBS multi-attach](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volumes-multi.html) supported for Linux on the Nitro instances in the same AZ. Only support Provisioned IOPS SSD (io1 and io2) volumes.
  - 1 EC2 - 1..N EBS. Can attach multiple EBS volumes to single EC2 instance. Data persist after detaching from EC2
- EBS Snapshots
  - It is an **incremental** backup of EBS Volume at a point in time saved into Amazon S3
    - Incremental => only blocks that have changed since your last snapshot (first snapshots takes longer)
  - Snapshots can be taken while the instance is running but ...
    - To create a snapshot for Amazon EBS volumes that serve as a root devices — best practice to terminate it first.
  - Snapshots can be shared with other AWS accounts or made public.
    - You can share snapshots, but only if they are unencrypted. If they are encrypted, ou need to share the encryption key with the other account.
  - Mechanism to move Volumen data (EBS) to a different AZ location (EBS volume cannot be mount to an EC2 into a different AZ directly)
    - To move an EC2 volume from one region to another, take a snapshot of it, create an AMI from the snapshot and then **copy the AMI from one region to other**. Then use the copied AMI to launch the new EC2 instance in the new region.
    - An AMI's can be created from both Volumes and Snapshots.
  - `EBS fast snapshot restore (FSR)` enables you to create a volume from a snapshot that is fully initialized at creation. This eliminates the latency of I/O operations on a block when it is accessed for the first time
- EBS volumen can be edited after instance is launched, it supports dynamic changes in live production volume e.g. volume type, volume size, and IOPS capacity without service interruption
- EBS Volume encryption:
  - Data at rest inside the volume is encrypted
  - Data in flight (tranSit) between the volume and EC2 instance is encrypted
  - Snapshots of encrypted volumes are automatically encrypted
  - Volumes created from encrypted snapshots are automatically encrypted
  - EBS volumes restored from encrypted snapshots are encrypted automatically.
  - Volumes created from unencrypted snapshots can be encrypted only at the time of creation
  - You can have encrypted an unencrypted EBS volumes attached to an instance at the same time.
- Types of EBS volumes:

**A/ SSD** for small/random IO operations, High IOPS means number of read and write operations per second, Only SSD EBS Volumes can be used as boot volumes for EC2

| SSD VolumeTypes                  |  Description                         |  Usage                                                                                                             |
| -------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| General Purpose _SSD_ (gp2/gp3)  | Max **16000 IOPS**                       | Balances price and performance (most cost-effective) and can be used for most workloads (boot volumes, dev environment, virtual desktop) |
| Provisioned IOPS _SSD_ (io1/io2) | 16000 - 64000 IOPS, EBS Multi-Attach | Mission critical business application, Databases (large SQL and NoSQL database workloads)                          |

**B/ HDD** (Hard Disk Drive) or Magnectic for large/sequential IO operations, High Throughput means number of bytes read and write per second

| HDD VolumeTypes                  |  Description                                                                 |  Usage                                                                                                                      |
| -------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Throughput Optimized _HDD_ (st1) | Low cost, frequently accessed, throughput intensive. Max 500 IOPS per volume | Big Data, Data warehouses, log processing                                                                                   |
| Cold _HDD_ (sc1)                 | Lowest cost, infrequently accessed. Max 250 IOPS per volume                  | Used for less frequently accessed workloads and when lowest storage cost is important. Common use could be for file servers |
| Magnetic (Standard)              | Max 40–200 IOPS per volume.                                                  | Previous generation hard disk drive typically used for infrequently accessed workloads.                                     |

- EBS Volumes with two types of RAID configuration:

  - **RAID 0 (increase performance)** two 500GB EBS Volumes with 4000 IOPS - creates 1000GB RAID0 Array with 8000 IOPS and 1000Mbps throughput
  - **RAID 1 (increase fault tolerance)** two 500GB EBS Volumes with 4000 IOPS - creates 500GB RAID1 Array with 4000 IOPS and 500Mbps throughput

- Use Case:
  1. A company has multiple AWS accounts for several environments (Prod, Dev, Test etc.). A Solutions Architect would like to copy an Amazon EBS snapshot from DEV to PROD. The snapshot is from an EBS volume that **was encrypted** with a custom key
  - When an EBS volume is encrypted with a custom key you must **share the custom key** with the PROD account. You also need to modify the permissions on the snapshot to share it with the PROD account. The PROD account must copy the snapshot before they can then create volumes from the snapshot
  - Note that you cannot share encrypted volumes created using a default CMK key and you cannot change the CMK key that is used to encrypt a volume.

### EFS (Elastic File System)

- Keyword: **File system interface**, Shared Mount (NFSv4.x), Only Linux, High Scalable, High Available, POSIX-compliant, NFSv4.x, Concurrent access (simultaneously)

![EFS AWS diagram](https://d1.awsstatic.com/legal/AmazonEFS/product-page-diagram_Amazon-EFS-Replication_HIW%402x.ccbabcc8777609fc0d23d7ff5ee1d52d5000dbf5.png)

- Fully managed, High scalable (Elastic) and Distributed (available) file storage that supports **Network File Storage version 4 (NFSv4.x)** and can be mounted to your EC2 instance.
  - Highly Scalable - scale on-demand to petabytes (growing and shrinking as you add/remove files) Note: you don't need to pre-provision storage like you do with EBS.
    - With burst mode, the throughput increase, as file system grows in size.
  - Highly Available - stores data redundantly across multiple Availability Zones.
  - Network File System (NFS) that can be mounted on and accessed concurrently in multiple AZs without sacrificing performance.
  - EFS file systems can be accessed by Amazon EC2 Linux instances, Amazon ECS, Amazon EKS, AWS Fargate, and AWS Lambda functions via a file system interface such as NFS protocol. (EBS only for EC2 instances)
    - Native to Unix & Linux, **but not supported on Windows instances**.
- EFS is a POSIX-compliant file-based storage.
- EFS supports file systems semantics - strong read after write consistency and file locking.
- Only pay for what you use
- Performance Mode:
  - General Purpose for most file system for low-latency file operations, good for content-management, web-serving etc.
  - Max I/O is optimized to use with 10s, 100s, 1000s of EC2 instances with high aggregated throughput and IOPS, slightly higher latency for file operations, good for big data analytics, media processing workflow
- Use case: When you need scalable and resilient storage for linux instances
  - Share files, images, software updates, or computing across all EC2 instances in ECS, EKS cluster
- EFS it works similartly to s3 regrading the storage classes (Standard, Standard Infrequent Access, One Zone, and One Zone Infrequent Access) and lifecycle policies.

### FSx for Windows

- Keyword: Shared Mount (NAS, NTFS (SMB)), Windows (also Linux with cifs-utils), Active Directory

![FSx for Windows AWS diagram](https://d1.awsstatic.com/pdp-how-it-works-assets/Product-Page-Diagram_Managed-File-System-How-it-Works_Updated@2x.c0c4e846c0fca27e8f43bd1651883b21b4cc1eec.png)

- Fully managed, HA (multiple AZ), native **Microsoft Windows file system** that supports **SMB protocol, Windows NTFS, Microsoft Active Directory (AD) integration**. And it also support Windows Features like ACLs, user quotas. shawdow copies
  - User quotas give you the option to better monitor and control costs. You pay for only the resources used, with no upfront costs, or licensing fees.
- NTFS file systems that can be accessed from up to thousands of compute instances using the SMB protocol.
- You can easily connect Linux instances to the file system by installing the cifs-utils package. The Linux instances can then mount an SMB/CIFS file system.
- Use cases:
  1. When you need **centralised storage for Windows-based applications** such as Sharepoint, Microsoft SQL Server, Workspaces, IIS Web Server or any other native Microsoft Application.
  2. **Migration from on-premises a Microsoft Windows file server farm to the cloud**
  3. A company requires a high-performance file system that can be mounted on Amazon EC2 Windows instances and Amazon EC2 Linux instances. Applications running on the EC2 instances perform separate processing of the same files and the solution must provide a file system that can be mounted by all instances simultaneously. Which solution meets these requirements? ==> Amazon FSx for Windows File Server provides a native Microsoft Windows file system so you can easily move your Windows-based applications that require shared file storage to AWS. You can easily connect Linux instances to the file system by installing the cifs-utils package (mount an SMB/CIFS file system).

### FSx for Lustre

- Keyword: HPC, Linux, Gaming, Integration with S3

![FSx for Lustre AWS diagram](https://d1.awsstatic.com/pdp-how-it-works-assets/product-page-diagram_Amazon-FSx-for-Lustre.097ed5e5175fa96e8ac77a2470151965774eec32.png)

- Fully managed and High performance file system for **fast processing of workload** with consistent **sub-millisecond latencies**, up to hundreds of gigabytes per second of throughput, and up to millions of IOPS.
- Lustre = Linux + Cluster is a **POSIX-compliant parallel linux file system**, which stores data across multiple network file servers.
- **Seamless integration with Amazon S3** (optional) - connect your S3 data sets to your FSx for Lustre file system, run your analyses, write results back to S3, and delete your file system.
- You can use **FSx for Lustre as hot storage** for your highly accessed files, and **Amazon S3 as cold storage** for rarely accessed files.
- FSx for Lustre provide two deployment options:
  - **Scratch file systems** - for temporary storage and short term processing
  - **Persistent file systems** - for high available & persist storage and long term processing
- Use case: When you need high speed or high capacity distributed storage for compute-intensive workloads, such as for Machine learning (ML), High performance computing (HPC), video processing, financial modeling, genome sequencing, and electronic design automation (EDA).

## Database

Go to [Index](#index)

### RDS (Relational Database Service)

- KeyWords: Relation Database (SQL), Different Enginees, HA/DR (Multi AZ Deployment), Scalable (Read Replicas), Cross Region, Multiple RDBS Enginnes Support

![AWS RDS](https://d1.awsstatic.com/video-thumbs/RDS/product-page-diagram_Amazon-RDS-Regular-Deployment_HIW-V2.96bc5b3027474538840af756a5f2c636093f311f.png)

- Saas to manage High Available and Scalable Relational databases in the Cloud
  - **It supports multiple Engines: PostgreSQL, MySQL, MariaDB, Oracle, Microsoft SQL Server, and Amazon Aurora**
  - RDS runs on Virtual Machines (can’t log in to the OS or SSH in)
  - RDS is not serverless — (one exception Aurora Serverless)
- RDS Main Features
  - **Multi AZ Deployment** > Used for HA (**not cross regions**)
    - Have a primary and secondary database, if you lose the primary database, AWS would detect and automatically update the DNS to point at the secondary database.
    - You can force a fail-over from AZ to another by rebooting the RDS instance.
  - **Read Replicas** > Used for Scaling, improving Performance (not millisecond latency)
    - A Read Replica allows you to have read-only copies (Upto 5 Read replicas) of your production database. This is achieved by using Asynchronous replication so reads are eventually consistent. Every time you write to the main database, it is replicated in the secondary databases.
    - Once RDS is selected as MultiAZ ==> Create a **read replica as a Multi-AZ DB instance**.
      - Exam Tip: Do not confuse with "Deploy a read replica in a different AZ to the master DB instance" (this is not Multi-AZ and not HA)
      - Amazon RDS creates a standby of your replica in another Availability Zone for failover support for the replica, even in a different Region of your running RDS instance. You pay for replication cross Region, but not for cross AZ.
    - Requirement: **Source DB must have automatic backups turned on in order to deploy a read replica**.
    - You can have read replicas of read replicas (but watch out for latency)
    - Each read replica will have its own DNS end point.
    - Read replicas can be promoted to be their own databases. This breaks the replication.
- RDS Backups
  - Automated Backups
    - Enabled by default
    - Allows you to recover your database to any point in time within the specified retention period (Max 35 days)
    - Takes daily snapshots and stores transition logs
    - When recovering AWS will choose the most recent backup
    - Backup data is stored in S3
    - May experience latency when backup is being taken
    - Backups are deleted once you remove the original RDS instances
  - Manual Database Snapshot
    - User-initiated, must be manually done by yourself
    - Stored until you explicitly delete them, even after you delete the original RDS instance they are still persisted (This is not the case with automated backups).
- Amazon RDS Proxy is a fully managed, highly available database proxy for Amazon Relational Database Service (RDS) that makes applications more scalable, more resilient to database failures, and more secure.
  - Use Case: A company hosts a serverless application on AWS. The application uses Amazon RDS for PostgreSQL. During times of peak traffic and when traffic spikes are experienced, the company notices an increase in application errors caused by database connection timeouts. The company is looking for a solution that will reduce the number of application failures with the least amount of code changes.
    - Amazon RDS Proxy allows applications to pool and share connections established with the database, improving database efficiency and application scalability.
- It offers **encryption at rest** but **encryption must be specified when creating the RDS DB instance**. Once your RDS instance is encrypted, as are its automated backups, read replicas, and snapshots. But you cannot create an encrypted Read Replica from an unencrypted master DB instance.
- Controlling access with `Database Security group` ==> Enabling this option only allow traffic that originates from the application security group, any instance that is launched and attached to this security group to connect to the database.
- `AWSAuthenticationPlugin` handles authentication for MariaDB and MySQL. It works seamlessly with IAM to authenticate your users.

```sql
CREATE USER jane_doe IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS';
```

- Use Cases:
  1. To change the encryption status of an existing RDS DB instance ==> Create a new master DB by taking a snapshot of the existing DB, and then creating the new DB from the snapshot (during creation). You can then create the encrypted cross-region Read Replica of the master DB. Applications must be updated to use the new RDS DB endpoint.
  2. A company uses an Amazon RDS MySQL database instance to store customer order data. The security team have requested that SSL/TLS encryption in transit must be used for encrypting connections to the database from application servers. The data in the database is currently encrypted at rest using an AWS KMS key. How can a Solutions Architect enable encryption in transit? => You can download a root certificate from AWS that works for all Regions or you can download Region-specific intermediate certificates.
  3. A team uses an Amazon RDS MySQL database running for running resource-intensive tests each month. The instance has Performance Insights enabled and is only used once a month for up to 48 hours. The team wants to reduce the cost of running the tests without reducing the memory and compute attributes of the DB instance. Which solution meets these requirements MOST cost-effectively? ==> Create a snapshot of the database when the tests are completed. Terminate the DB instance. Create a new DB instance from the snapshot when required

### Amazon Aurora

- KeyWords: Relation Database (SQL), Scalable (Read Replicas - across AZs for HA), Global Database (**across Regions**), AWS proprietary Database, Serveless (optional), RDBS Enginnes Support only MySQL and PostgreSQL

![AWS Aurora](https://d1.awsstatic.com/Product-Page-Diagram_Amazon-Aurora_How-it-Works.b1c2b37e7548757780b195c6dcceb58511de5b1d.png)

- It is Saas which manages own AWS engine for relational database (Aurora Global Database) **compatible with MySQL and PostgreSQL**
  - Provides 5x better performance than MySQL
  - Provides 3x better performance than Postgres SQL

![Aurora Replicas](https://digitalcloud.training/wp-content/uploads/2022/01/amazon-aurora-fault-tolerance.jpeg)

- **Replicas**: 2 copies of your data is contained in each Availability Zone (AZ) — minimum of 3 AZ’s and 6 copies.
  - It works **in-region and cross-regions**
  - Typically operates as a DB cluster consist of one or more DB instances and a cluster volume that manages cluster data with each AZ having a copy of volume.
    - Primary DB instance - Only one primary instance, supports both read and write operation.
    - Read Replicas - There are two types of replication: Aurora replica (up to 15, In-region), MySQL Read Replica (up to 5, Cross-region).
  - **Fault tolerant**: It can handle the loss of up to 2 copies without affecting write ability and the lose of up to 3 copies of data without affecting read ability.
  - **Self-healing storage system** (Data blocks and disks are continuously scanned for errors and repaired automatically.)
  - **Autoscaling for storage and computer capacity**
    - Start with 10Gb, Scales in 10 GB increments to 64 TB (Storage Autoscaling)
    - Compute resources can scale up tp 32vCPUS and 244GB of Memory

![Aurora Global](https://digitalcloud.training/wp-content/uploads/2022/01/aurora-global-database.jpeg)

- **Global Database**: For globally distributed applications you can use Global Database, where a single Aurora database can span **multiple AWS regions** to enable fast local reads and quick disaster recovery.
  - **Disaster Recovery**: You can use a secondary region as a backup option in case you need to recover quickly from a regional degradation or outage.
    - It supports a Recovery Point Objective (RPO) of 1 second and a Recovery Time Objective (RTO) of 1 minute

- Backups (Mix)
  - Backups do not impact performance.
  - Automated Backups are Enabled by default.
  - You can also take manual snapshots with Aurora. Snapshots can be shared with other AWS accounts.

- Aurora Serverless
  - **On demand autoscaling configuration of Aurora**
  - Automatically starts up, shuts down, and scales based on app needs.
  - Used for simple, cost effective (Only pay for invocation), infrequently used, intermittent or unpredictable workloads.

- Use Cases:
  1. A company runs a web application that store data in an Amazon Aurora database. A solutions architect needs to make the application more resilient to sporadic increases in request rates.
  - To resolve this situation Amazon Aurora Read Replicas can be used to serve read traffic which offloads requests from the main database.
  2. An insurance company has a web application that serves users in the United Kingdom and Australia. The application includes a database tier using a MySQL database hosted in eu-west-2. The web tier runs from eu-west-2 and ap-southeast-2. Amazon Route 53 geoproximity routing is used to direct users to the closest web tier. It has been noted that Australian users receive slow response times to queries. How to improve the performance? ==> Migrate the database to an Amazon Aurora global database in MySQL compatibility mode. Configure read replicas in ap-southeast-2
  3. An application requires a MySQL database which will only be used several times a week for short periods. The database needs to provide automatic instantiation and scaling ==> Aurora Severless
  4. An store uses an Amazon Aurora database. The database is deployed as a Multi-AZ deployment. Recently, metrics have shown that database read requests are high and causing performance issues which result in latency for write requests. How to separate the read requests from the write requests? ==> Update the application to read from the Aurora Replica. An Aurora Replica already exists as this is a Multi-AZ configuration and the standby is an Aurora Replica that can be used for read traffic.
  5. A company runs a business-critical application in the us-east-1 Region. The application uses an Amazon Aurora MySQL database cluster. A disaster recovery strategy is required for failover to the us-west-2 Region. The strategy must provide a recovery time objective (RTO) of 10 minutes and a recovery point objective (RPO) of 5 minutes. ==> Recreate the database as an Aurora global database with the primary DB cluster in us-east-1 and a secondary DB cluster in us-west-2. Use an Amazon EventBridge rule that invokes an AWS Lambda function to promote the DB cluster in us-west-2 when failure is detected

### DynamoDB

- KeyWords: NoSQL, AWS proprietary, Eventual Consistent Read, Strongly Consistent Reads, IoT, Near Real Time Performance, key-value database, Session Data, Global tables (Cross Regions)

![AWS Dynamo DB](https://d1.awsstatic.com/product-page-diagram_Amazon-DynamoDBa.1f8742c44147f1aed11719df4a14ccdb0b13d9a3.png)

- AWS proprietary, a fast and flexible **NoSQL** database service for all applications that need consistent, **single-digit millisecond latency/response** at any scale.
- It is fully Managed and Serverless (no servers to provision, patch, or manage) database.
- Its **flexible data model** and reliable performance make it a great fit for mobile, web, gaming, ad-tech, IoT, and many other applications. It supports both:
  - Document (limit of 400KB item size. E.g. JSON documents, or session data.)
  - **Key-value data models**.
- Spread across 3 geographically distinct data centers.
- It supports eventually consistent and strongly consistent reads (eventual consistency is default).
  - Eventual Consistent Read (Default): Consistency across data within a second, meaning the response might not reflect the results of a just completed write operation, but if you repeat the read request again it should return the updated data (Best Read Performance).
  - Strongly Consistent Reads: Returns the latest data. Results should reflect all writes that received a successful response prior to that read!
- `DynamoDB Time to Live (TTL)` allows you to define a per-item timestamp to determine when an item is no longer needed. DynamoDB deletes the item from your table for you without consuming any write throughput. TTL is provided at no extra cost to reduce stored data volumes.
- Use Case: An IoT sensor is being rolled out to thousands of a company’s existing customers. The sensors will stream high volumes of data each second to a central location. A solution must be designed to ingest and store the data for analytics. The solution must provide near-real time performance and millisecond responsiveness.
  - Ingest the data into an Amazon Kinesis Data Stream. Process the data with an AWS Lambda function and then store the data in Amazon DynamoDB.

#### DynamoDB Streams: Integrations with other services via Events

- This feature is enabled to **trigger events on database**.
- It is a time ordered sequence of item level modifications in a table (stored up to 24 hours).
- Possible Integrations
  - Lambda function for e.g. Send welcome email to user added into the table.
  - SNS Topics e.g. Send an alert to the managers multiple teams every time a new record is updated. Note managers needs to subscribe to the topic.

![Dynamo DB Streams](https://img-c.udemycdn.com/redactor/raw/2020-06-28_19-55-43-04c370b6a009c1594a77bd12b9499c3d.png)

#### Global Tables

- This feature is enabled to serve the data globally for distributed apps or for Disaster Recovery scenarios: multi-active & multi-region database, that replicate your DynamoDB tables across selected regions.
- It is based on DynamoDB streams, thus it must enabled first to create global table.

#### Security in DynamoDB

- Encryption at rest using KMS
- Can use site to site VPN, direct connect (Dx) and IAM policies and roles
- Can implement fine grain access
- Can be monitored on Cloud Watch and Cloud trail

####  DynamoDB Accelerator (DAX)

- Add DAX (DynamoDB Accelerator) cluster in front of DynamoDB to **cache** (in memory) frequently read values and offload the heavy read on hot keys of DynamoDB, prevent`ProvisionedThroughputExceededException`
- It improves the performance (up to x10) of DynamoDB. Request time reduced to microseconds.
- Compatible with Dynamo API calls.

### ElastiCache

- KeyWords: In-memory Cache, **sub millisecond** latency, Redis, Memcached

![AWS ElasticCache](https://d1.awsstatic.com/elasticache/EC_Use_Cases/product-page-diagram_ElastiCache_how-it-works.ec509f8b878f549b7fb8a49669bf2547878303f6.png)

- It is SaaS for **in-memory caching** supporting flexible, real-time use cases. In-memory key/value store, not persistent in the traditional sense.
- Fully managed implementations of two popular in-memory data stores – Redis and Memcached.
  - Memcached — A widely adopted in-memory key store, and historically the gold standard of web caching. For simple Uses Cases Memcached is also **multithreaded**, meaning it makes good use of larger Amazon EC2 instance sizes with multiple cores.
  - Redis — An increasingly popular open-source key-value store that supports more advanced data structures (such as sorted sets, hashes, and lists). Unlike Memcached, Redis has **disk persistence** built in and it also supports replication, which can be used to achieve **Multi-AZ redundancy** (HA).
    - `Redis Auth` --> Redis authentication tokens enable Redis to require a token (**password**) before allowing clients to execute commands, thereby improving data security.
    - HIPAA Compliant.
- `in-transit encryption` is an optional feature that allows you to increase the security of your data at its most vulnerable points—when it is in transit from one location to another.
- Uses Cases:
  - Improves Performance of **Applications and Databases**. It allows you to retrieve data fast from memory with high throughput and low latency. Use as distributed cache with **sub millisecond performance**.
    - Best for scenarios where the DB load is based on Online Analytics Processing (OLAP) transactions.
  - Primary data store for use cases that don't require durability/perisistency like session stores, gaming leaderboards, streaming, and analytics

**Exam tip** : the key use cases for ElastiCache are offloading reads from a database and storing the results of computations and session state. Also, remember that ElastiCache is an in-memory database and it’s a managed service (so you can’t run it on EC2).

### Redshift

- KeyWords: SQL for BI, Compression, Massive Parallel Processing, Data Warehousing, Petabyte scale

![AWS Redshift](https://d1.awsstatic.com/Product-Page-Diagram_Amazon-Redshift%402x.6c8ada98ebf822d3ddc113e6b802abe08fd4a4d2.png)

- Saas that uses **SQL** to analyze **structured and semi-structured data across data warehouses, operational databases, and data lakes**, using AWS-designed hardware and machine learning (**ML**) to deliver the best price performance at any scale. For long running operations.
- It can be used for **Business Intelligence (BI)**, allowing integrations with tools like AWS Quicksight or Tableau for analytics
- It uses Advanced compression: Has column compression — compress columns instead of rows because of similar data because similar data is stored sequentially on disk.
- Automated Backups (not manual snapshots)
  - Enabled **by default** with a 1 day retention period (Maximum is 35 days)
  - It tries to maintain at least three copies of your data (the original and replica on the compute nodes and a backup in Amazon S3).
  - It can also asynchronously replicate your snapshots to S3 in another region for DR.
  - Only Redshift can delete these automated snapshots, you can’t delete them manually.
- Security Considerations
  - Encrypted in transit using SSL
  - Encrypted at rest using AES-256 encryption
  - By default, Redshift takes care of key management
- Pricing — compute node hours, backups and data transfer
- It can be configured as follows:
  - Single Node (160Gb)
  - Multi-Node
    1. Leader Node (manages client connections and receives queries)
    2. Compute Node (store data and perform queries and computations). Up to 128 Compute Nodes.
- `Result Cache` (enabled by default): To improve performance, it caches the results of certain types of queries in memory on the leader node. It is transparent to the enduser.
- Availability
  - **Currently only in 1 AZ** (check AWS to confirm for the latest)
  - Can restore snapshots to new AZs in the event of an outage
- It supports Massive Parallel Processing (MPP): It automatically distributes data and query load across all nodes, making easy to add nodes to your data warehouse and enables you to maintain fast query performance as your data warehouse grows.
- COPY: Loads data into a table from data files or from an Amazon DynamoDB table. The files can be located in an Amazon Simple Storage Service (Amazon S3) bucket, an Amazon EMR cluster, or a remote host that is accessed using a Secure Shell (SSH) connection.

### Amazon Kinesis

- KeyWords: Streaming media, **Real-time** performance, IoT
- It is PaaS for collecting, processing, and analyzing **streaming real-time data in the cloud** (video, audio, logs, analytics etc.) and process/analyse that data in real time. Real-time data generally comes from **IoT devices, gaming applications, vehicle tracking, click stream, etc.**
- Use Case: An automotive company plans to implement IoT sensors in manufacturing equipment that will send data to AWS _in real time_. The solution must receive events in an ordered manner from each asset and ensure that the data is saved for future processing.
  - Use Amazon Kinesis Data Streams for real-time events with a partition for each equipment asset. Use Amazon Kinesis Data Firehose to save data to Amazon S3.
  - Amazon Kinesis Data Streams is the ideal service for receiving streaming data. The Amazon Kinesis Client Library (KCL) delivers all records for a given partition key to the same record processor, making it easier to build multiple applications reading from the same Amazon Kinesis data stream. Therefore, a separate partition (rather than shard) should be used for each equipment asset.
  - Amazon Kinesis Firehose can be used to receive streaming data from Data Streams and then load the data into Amazon S3 for future processing.

#### Kinesis Video Streams

![kinesis-video](https://d1.awsstatic.com/Product-Page-Diagram_Amazon-Kinesis-Video-Streams%20(1).bdd5d9aa84af0b6aa1ba0fdfe66f172e02173db2.png)

- It is SaaS that makes it easy to securely (Automatically encrypts it at rest) stream live video from devices to the cloud.
- Enables playback, analytics and machine learning on video data that has been ingested.

#### Kinesis Data Streams

- Keywords: Streaming data, Real time Queue, Shards, No autoscale, Multiple Consumer and Producers, Long Retention (24 hours to 365 days)

![Amazon Kinesis](https://d1.awsstatic.com/Digital%20Marketing/House/1up/products/kinesis/Product-Page-Diagram_Amazon-Kinesis-Data-Streams.e04132af59c6aa1e9372cabf44a17749f4a81b16.png)

- It is SaaS for streaming data that makes it easy to capture, process, and store data streams at any scale.
- Automatically stores data and encrypts it at rest
- Like SQS, the **consumer pulls data** but passes it through a **SHARD** to the consumer
  - Multiple Producer and Consumers
    - Producer can be Amazon Kinesis Agent, SDK, or Kinesis Producer Library (KPL)
    - Kinesis you can have **multiple distinct consumers**: Kinesis Data Analytics, Kinesis Data Firehose, or Kinesis Consumer Library, Lambda.
  - Kinesis keeps the messages for a specified time, from 24 hours (default) to 365 days (max).
  - Order is maintained at Shard (partition) level.
  - Not Autoscale

![consumer-producer](https://betterdev.blog/app/uploads/2021/08/kinesis-streams-messaging.png)

##### Shards

- A shard is a **sequence of data records in a stream** with a fixed unit of capacity.
- A shard limits
  - 1 MB write or 2 MB read per second (on Average)
  - 1000 messages/sec
- **Only data streams have shards**. The total capacity of a stream is the sum of the capacities of its shards.
- A partition key is used to group data by shard within a stream. Kinesis Data Streams segregates the data records belonging to a stream into multiple shards. It uses the partition key that is associated with each data record to determine which shard a given data record belongs to.

#### Kinesis Firehose

- Keywords: Real time ETL, Kinesis Data Streams Consumer

![Firehouse](https://d1.awsstatic.com/Product-Page-Diagram_Amazon-Kinesis-Data-Firehose%20(2).f9965f969e70f3f6f4ca9efaba3a6cfec8a746a1.png)

- It is SaaS for **ETL** with streaming data
  - load data streams into AWS data stores such as S3, Amazon Redshift and ElastiSearch.
  - Transform data using lambda functions and store failed data to another S3 bucket.
  - Can compress, transform and batch data to minimise the amount of storage.
- Encrypts your data streams before loading.
- Pay for the volume of data that transmits through the service.

#### Kinesis Analytics

![KinesisAnalytics](https://d1.awsstatic.com/Product-Page-Diagram_Kinesis-Data-Analytics%20(1).4c9d80d0aac0f17f5043f1677a4db5d427e1157f.png)

- It is SaaS to allows you to analyse streaming data in real time to gain **actionable insights**.
- Allows you to process and analyse data using standard SQL.
- Can gain realtime dashboards and create real time metrics.
- Can use with Data Streams or Firehose as the streaming source.

### Amazon EMR

- KeyWord: BigData, ETL, Petabyte-scale analysis

![Amazon EMR](https://d1.awsstatic.com/products/EMR/Product-Page-Diagram_Amazon-EMR.803d6adad956ba21ceb96311d15e5022c2b6722b.png)

- Amazon EMR (EMR = Elastic MapReduce) is the industry-leading cloud **Big Data** platform for processing vast amounts of data using open-source tools such as **Apache Spark, Apache Hive, Apache HBase, Apache Flink, Apache Hudi and Presto**.
  - With EMR, you can run **petabyte-scale analysis** at less than half the cost of traditional on-premises solutions and over 3x faster than standard Apache Spark.
  - EMR can be used to perform **ETL** operations
- Use case: Analyze Clickstream data from S3 using Apache Spark and Hive to deliver more effective ads.
- The central component of Amazon EMR is the cluster. A cluster is a collection of Amazon EC2 instances. Each instance in the cluster is called a Node, each node has a role within the cluster, referred to as the node type (different software components is installed on each node type)

  - Master node: A node that manages the cluster. The master node tracks the status of tasks and monitors the Health of the cluster. Every cluster has a master node.
    - By default - log data is stored on the master node. Alternatively, it can be configured (only at the moment of creation not after) a cluster to periodically archive the log files to Amazon S3 (at five-minute intervals). This ensures the log files are available after the cluster terminates (due to normal shutdown or an error)
  - Core node: A node with software components that **Runs tasks and Stores data**. Multi-node clusters have at least one core node.
  - Task node: A node with software components that **only runs tasks** and does not store data. Task nodes are optional.

### Neptune

- KeyWord: Graph Database for Graph applications

![AWS Neptune](https://d1.awsstatic.com/products/Neptune/product-page-diagram_Amazon-Neptune%402x.8af655592b659339933079725a914c14cbc0d831.png)

- It is a SaaS for Graph Database (relation between elements) that makes it easier to build and run graph applications. Neptune provides built-in security, continuous backups, serverless compute, and integrations with other AWS services.
- Use case: high relationship data, social networking data, knowledge graphs (Wikipedia)

### OpenSearch (for ElasticSearch)

- KeyWord: ElasticSearch, Logs Indexing and Analysis.

![OpenSearch](https://d1.awsstatic.com/product-marketing/Elasticsearch/product-page-diagram_Amazon-OpenSearch-Service_HIW%402x.f20d73b8aa110b5fb6ca1d9ebb439066a5e31ef5.png)

- It is a managed Elastic Search service Amazon for performing interactive Log Analytics, Real-time application monitoring, Website search, and more.
- OpenSearch is an open source, distributed search and analytics suite derived from Elasticsearch. Amazon OpenSearch Service offers the latest versions of OpenSearch, support for 19 versions of Elasticsearch (1.5 to 7.10 versions), as well as visualization capabilities powered by OpenSearch Dashboards and Kibana (1.5 to 7.10 versions).
- Integration with Kinesis Data Firehose, AWS IoT, and **CloudWatch logs** (stream logs to OpenSearch).
- Use case: Search, indexing, partial or fuzzy search

### Amazon Quantum Ledger Database (QLDB)

- KeyWord: Ledger database, Immutable, NoSQL

![QLDB](https://d1.awsstatic.com/r2018/h/99Product-Page-Diagram_AWS-Quantum.f03953678ba33a2d1b12aee6ee530e45507e7ac9.png)

- It is a fully managed ledger database that provides a transparent, immutable, and **cryptographically verifiable transaction log**.
- It has a built-in immutable journal that stores an accurate and sequenced entry of every data change. The journal is append-only, meaning that data can only be added to a journal, and it cannot be overwritten or deleted.

### Amazon DocumentDB (for MongoDB)

- Amazon DocumentDB (with MongoDB compatibility) is a fully managed native **JSON document database** that makes it easy and cost effective to operate critical document workloads at virtually any scale without managing infrastructure.
- Amazon DocumentDB simplifies your architecture by providing built-in security best practices, continuous backups, and native integrations with other AWS services.

### Amazon Keyspaces (for Apache Cassandra)

- It is a scalable, highly available, and managed Apache Cassandra–compatible database service.

### AWS Lake Formation

- It easily creates secure data lakes, making data available for wide-ranging analytics.
- With AWS Lake Formation, you can import data from MySQL, PostgreSQL, SQL Server, MariaDB, and Oracle databases running in Amazon Relational Database Service (RDS) or hosted in Amazon Elastic

![](https://d1.awsstatic.com/diagrams/Lake-formation-HIW.9ea3fab3b2ac697a42ae7a805b986278ffd4f41e.png)


## Migration

Go to [Index](#index)

### AWS Snow Family

- AWS snow family are **Physical devices** used **FROM on-premises** large scale data migration **TO S3 buckets** and processing data **at low network locations**
- Use case: Addresses a lot of the common challenges that typically comes with with large-scale data transfers, including high network costs, long transfer times, and security concerns.
  - Physical device/service ==> **It does not require Internet to use it**.

| Family Member | Storage | RAM | Migration Type   | DataSync | Migration Size |
| ------------- | ------- | --- | ---------------- | -------- | -------------- |
| Snowcone      | 8TB     | 4GB | online & offline | yes      | GBs and TBs    |

![snowcone](https://d1.awsstatic.com/SnowconHIW122722.406d05c2ce372214190996db3bd52e17e15e4007.png)

| Family Member | Storage | RAM   | Migration Type | DataSync | Migration Size |
| ------------------------------- | ------- | ----- | -------------- | -------- | -------------- |
| Snowball Edge Storage Optimized | 80TB    | 80GB  | offline        | no       | Petabyte-scale |
| Snowball Edge Compute Optimized | 42TB    | 208GB | offline        | no       | Petabyte-scale |

![snowball](<https://d1.awsstatic.com/hiw_snowball%402x%20(3).afde317ee4d3d8abe9a7ecc4fe52fefb9f454683.png>)

- AWS Snowball Edge comes with on-board storage and compute power for select AWS capabilities. Snowball Edge can do **local processing and edge-computing workloads** in addition to transferring data between your local environment and the AWS Cloud.

| Family Member | Storage | RAM | Migration Type | DataSync | Migration Size |
| ------------- | ------- | --- | -------------- | -------- | -------------- |
| Snowmobile    | 100PB   | N/A | offline        | no       | Exabyte scale  |

![snowmobile](https://d1.awsstatic.com/Product-Page-Diagram_AWS-Snowmobile%402x.4f7215d254697f7cb01d2e7189b81cb660165260.png)

- Exam Tip: Direct Connect Link (requires Cable Connection) and Snowball (does not requires any Connection) are not compatible to work together.

### AWS DataSync

- Data transfer service for **moving large amounts of data into AWS**. It automate and **accelerate the replication** of data to AWS storage services. Has built in **security capabilities** (e.g. encryption in transit)
- Note: Its name can be consfusing ==> It syncs on one way only (from source to destination) for migration purpose.
- To deploy DataSync an agent must be installed.
- Types

**A/** FROM an on-premise data center (using NFS and SMB storage protocol) TO AWS Storage: S3 (any storage type) , EFS, or FSx for Windows, AWS Snowcone. => Installing AWS Data Sync Agent on a VM, Amazon s3 Outspots or Snowcone

![on premise](https://d1.awsstatic.com/Digital%20Marketing/House/Editorial/products/DataSync/Product-Page-Diagram_AWS-DataSync_On-Premises-to-AWS%402x.8769b9dea1615c18ee0597b236946cbe0103b2da.png)

**B/** BETWEEN AWS storage services (e.g. to replicate EFS to EFS)

![between aws](https://d1.awsstatic.com/Digital%20Marketing/House/Editorial/products/DataSync/Product-Page-Diagram_AWS-DataSync-to-AWS-Storage-Services%402x.c9ae72a5d796feed1fd562b968fc133f9e66eec2.png)

**C/** FROM other Public Clouds to AWS Storage Services => Installing AWS Data Sync Agent on a VM

![different cloud](https://d1.awsstatic.com/Digital%20Marketing/House/Editorial/products/DataSync/AWS-DataSync-CrossCloud-to-AWS-Storage-Services_1%402x.bf8d56bb81dce99407eed06593b961bcb893dc0f.png)

- Use Case:
  An organization has a large amount of data in their on-premises data center. The organization would like to move data into Amazon S3
  - The most reliable and time-efficient solution that keeps the data secure is to use `AWS DataSync` and synchronize the data from on premise to directly to Amazon S3
  - In case the data center bandwidth is saturated => NOT Use `DataSync` but use `AWS Snowball` because it is requires a pshipical device.
  - Combinations:
    - `AWS Direct Connect` connection to ensure reliability, speed, and security.
    - `AWS Glue` for data transformation when it is required.

### AWS Backup

![backup](https://d1.awsstatic.com/products/backup/Product-Page-Diagram_AWS-Backup%402x.9a3f6d1b456ddadac992018c5b308bb1d9e8c055.png)

- AWS Backup to centrally manage and automate backup process for EC2 instances, EBS Volumes, EFS, RDS databases, DynamoDB tables, FSx for Lustre, FSx for Window server, and Storage Gateway volumes
- Use case: Automate backup of RDS with 90 days retention policy. (Automate backup using RDS directly has max 35 days retention period)

### Database Migration Service (DMS)

- KeyWords: Database Migration, Homogeneos/heterogeneos Migration
- It Saas that to transfer (Replicate) a database to another type (relational databases, data warehouses, NoSQL databases and other types of data stores).
- It supports multiple combinations: Out of AWS => AWS, AWS => AWS, AWS => Out of AWS (different cloud)
- Steps:
  - Create a source and a target endpoints
  - Schedule/Run a Replication Task (Replication Instance - VM) to move the data
  - No downtime (Source stays functioning the whole time during the migration)
- Types of migrations:
- Types:

**A/** Homogenous migrations (origin and target same technology) e.g. On-premise PostgreSQL => AWS RDS PostgreSQL

![dms_homogeneous](https://d1.awsstatic.com/Product-Page-Diagram_AWS-Database-Migration-Service_Homogenous-Database-Migrations_Reduced%402x.053ebcf3f38feed093d6180bb7a351c5551a30a1.png)

**B/** Heterogenous migrations (origin and target different technology) such as MS SQL to Amazon Aurora. It requires to run AWS SCT (Schema Conversion Tool) at source

![dms_heterogeneous](https://d1.awsstatic.com/reInvent/reinvent-2022/data-migration-services/product-page-diagram_AWS-DMS_Heterogenous-Brief.e64d5fda98f36a79ab5ffcefa82b2735f94540ea.png)

Exam Tip: Migration from on-premises Databases to AWS RDS (e.g Microsoft SQL Server)

- Select the same Database Engine in the origin and destination
- Move data using [AWS DMS](#database-migration-service-dms)
  - You only need the Schema Conversion Tool (SCT) if origin and destination are different enginees

### AWS Application Migration Service (MGN)

![mgn](https://d1.awsstatic.com/pdp-headers/2022/application-migration/MGN-How-It-Works-Diagram_biggerfonts1.1cb6cd71af1796ed95842d71c7b7a588a81c442d.jpg)

- It helps on automating the conversion of your **Source servers (VM)** (VMware vSphere, Microsoft Hyper-V or Microsoft Azure) **to run natively on AWS** (EC2). It also simplifies application modernization with built-in and custom optimization options.
- AWS Application Migration Service: Legacy vs New.
  - New, it utilizes continuous, block-level replication and enables cutover windows measured in minutes.
  - Legacy, it utilizes incremental, snapshot-based replication and enables cutover windows measured in hours.

## Networking

Go to [Index](#index)

### Amazon VPC (Virtual Private Cloud)

![vpc](https://d1.awsstatic.com/Digital%20Marketing/House/Hero/products/ec2/VPC/Product-Page-Diagram_Amazon-VPC_HIW.9c472d7f2eb39ab8bdd22aa3ab80be00cdd00d8f.png)

- A VPC is a **logical separated section of AWS Cloud (your own DataCenter in AWS)** for an account to enable:
  - Launch instances
  - Assign custom IP address ranges
  - Configure route tables between subnets
  - Create internet gateway and attach it to our VPC
  - Much better security control over your AWS resources
  - Instance security groups
  - Subnet network access control lists (ACL's)
- VPCs are **region specific** (they do not span across regions)
  - **Every region comes with default VPC**.
  - You can create upto 5 VPC per Region by default (soflimit, it can be extended)
- Default VPC vs Custom VPC
  - **Default VPC is user friendly**, allowing you to immediately deploy instances.
  - All **subnets in a default VPC are public** (have a route out to the internet).
  - Each EC2 instance has both a public and private IP address.
  - In case it is delated, it can be recovered (but, try not to delete it).
- You are not charged for using a VPC, however you are charged for the components used within it e.g. gateway, traffic monitoring etc.
- One way to save costs when it comes to networking is to use private IP addresses instead of public IP addresses as they utilise the AWS Backbone network.
  - If you want to cut all network costs, group all EC2 instances in same AZ and use private IP addresses.
- Types of tenancy: On set up of your VPC you will be asked to choose either:
  - Dedicated → Everything on dedicated hardware (Very expensive)
  - Default → multi-tenant share underlying hardware with other AWS customers
- Cost nothing: VPCs, Route Tables, NACLs, Internet Gateway, Security Groups, Subnets, VPC Peering.
- Cost money: NAT Gateway, VPC Endpoints, VPN Gateway, Customer Gateway.

#### Required Components

- VPC’s consist of an Internet gateway, Subnets, Route tables, Network Access Control Lists and Security Groups.
- When we create a VPC
  - Created by default: a Route Table, Network Access Control List and Security Group.
  - No created by default: Subnets and Internet gateway.

##### A/ Subnet (No created by default)

- A **range of IP addresses** within a VPC.
  - You assign **one CIDR block per Subnet**. It should not overlap with other Subnet’s CIDR in your VPC.
  - Amazon don't allow /8 prefix as it is too large — the largest they allow is /16
  - Amazon always reserve 5 IP addresses within your subnets (First 4 IPs and the last IP): Network Address, Router Address, DNS Server Address, Broadcast address and 1 more for future use.
    - For e.g. If you need 29 IP addresses to use, your should choose CIDR /26 = 64 IP and not /27 = 32 IP, since 5 IPs are reserved and can not use.
  - Enable Auto assign public IPv4 address in public subnets, EC2 instances created in public subnets will be assigned a public IPv4 address
- Private vs Public Subnets:
  - Public Subnet: A subnet that does have a route to the internet gateway.
- Use Case: Multi-tier and highly-available architecture: If you have 3 AZ in a region then you create total 6 subnets.
  - 3 private subnets (1 in each AZ) for EC2 instances, Lambda, Database.
  - 3 public subnets (1 in each AZ) for **API gateway and ELB reside in public subnet**.
- **Each subnet is tied to one Availability Zone, one Route Table, and one Network ACL** (A subnet cannot span multiple AZs. However an AZ can have multiple subnets).

###### CIDR block (Classless Inter-Domain Routing)

- It is an internet protocol address allocation and route aggregation methodology. CIDR block has two components - Base IP (WW.XX.YY.ZZ) and Subnet Mask (From /0 to /32)
- Examples - Base IP 192.168.0.0
  - 192.168.0.0/32 means 2 raised to (32-**32**) = **1 single IP**
  - 192.168.0.0/24 means 2 raised to (32-**24**) = 256 IPs ranging from 192.168.0.0 to 192.168.0.255 (last number can change)
  - 192.168.0.0/16 means 2 raised to (32-**16**) = 65,536 IPs ranging from 192.168.0.0 to 192.168.255.255 (last 2 numbers can change) - Max for AWS
  - 192.168.0.0/8 means 2 raised to (32-8)= 16,777,216 IPs ranging from 192.0.0.0 to 192.255.255.255 (last 3 numbers can change)
  - 0.0 0.0.0.0/0 means 232-0= All IPs ranging from 0.0.0.0 to 255.255.255.255 (all 4 numbers can change)

##### B/ Internet Gateway (No created by default)

![Internet Gateway](https://docs.aws.amazon.com/images/vpc/latest/userguide/images/internet-gateway-basics.png)

- Allows your VPC (**public subnet**) to communicate with the Internet ==> Performs network address translation for instances.
- 1 VPC <-> 1 Internet Gateway. Each Internet Gateway is associated with one VPC only, and each VPC has one Internet Gateway only (one-to-one mapping)
- For internet communication, you must set up a route in your route table that directs traffic to the Internet Gateway ==> It becomes a public subnet.
- **Note:** For Site-to-Site VPN connection, you must use Virtual Private Gateway or Transit Gateway (not Internet Gateway.)

##### C/ Route Table (Created by default)

- A **set of rules (called routes) that are used to determine where network traffic is directed**.
  - Each Route table route has `Destination` like IPs and `Target` like local, IG, NAT, VPC endpoint etc.
  - Allows subnets to talk to each other.
- Each subnet in your VPC must be associated with a route table.
- Cardinality:
  - 1 Subnet -> 1 Route Table. A subnet can only be associated with one route table at a time
  - 1 Route Table -> N Subnets. Multiple subnets can be associated with the same route table For e.g. you create 4 subnets in your VPC where 2 subnets associated with one route table with no internet access rules know as private subnets and another 2 subnets are associated with another route table with internet access rules known as public subnets
- By default subnets are associated with the Main route table, but this can be a security risk (e.g. if you were to put a route out to the public internet in the route table all subnets would automatically be made public).
  - To resolve this — keep main route table as private and then have separate route tables that use the main one, but have additional routes.
- Public vs Private Subnet
  - Public subnet ==> It is a subnet that’s associated with a route table having **rules to connect to internet using Internet Gateway**.
  - Private subnet ==> It is a subnet that’s associated with a route table having **no rules to connect to internet using Internet Gateway**.
    - Private subnet connect to the internet by setting a rule to a **NAT Gateway in a public Subnet**.

##### D/ Network Access Control List (Created by default)

- It **acts as a Firewall**, it controls the inbound and ourbound traffic **at Subnets level** ==> It applies to all instances in associated subnet.
- Differences with Security groups:
  - You can **block IP addresses**, it allows Deny Rules
  - They are **stateless**, when you create an inbound rule and an outbound rule is not automatically created. It means they can have separate inbound and outbound rules.
- Cardinality: A NACL can be associated with many Subnets, but a subnet can only have one NACL.
- VPCs comes with a modifiable default NACL it allows all inbound and outbound traffic (by default)
  - You can create custom NACL --> denies all inbound and outbound traffic until you add rules (by default)
- Each subnet within a VPC must be associated with only 1 NACL
  - If you don’t specify, auto associate with default NACL
  - If you associate with new NACL, auto remove previous association
- Rules
  - **Support both Allow and Deny rules**
  - **Evaluate rules in number order**, starting with lowest numbered rule. NACL rules have number (1 to 32766) and **higher precedence to lowest number** for e.g. #100 ALLOW <IP> and #200 DENY <IP> means IP is allowed
    - Tip: It is recommended to create numbered rules in increments (for example, increments of 10 or 100) so that you can insert new rules where you need to later on.
  - Each network ACL also includes a rule with rule number as asterisk *. If any of the numbered rule doesn’t match, it’s denies the traffic. You can't modify or remove this rule.

##### E/ Security Groups (Created by default)

- It **acts as a Firewall**, it controls inbound and outbound traffic **at EC2 instance level**, specific for each instance.
- Differences with Security groups:
  - You **cannot block IP addresses**, it does not allows Deny Rules
  - **Stateful** when you create an inbound rule and an outbound rule is automatically created.
- You can specify a source in security group rule to be an IP range, a specific IP (/32), or another security group.
- When you first create a security group, by default (no rules)
  - All **outbound** traffic is **allowed**.
  - All **inbound** traffic is **blocked**.
- Cardinality: N Security Group <--> N EC2 instance.
  - You can have any number of EC2 instances within a security group.
  - You can have multiple Security Groups attached/assigned to EC2 instances. Evaluate all rules before deciding whether to allow traffic. Meaning if you have one security group which has no Allow and you add an allow in another than it will Allow
- Use Cases:
  1. An architect is designing a two-tier web application. The application consists of a public-facing web tier hosted on Amazon EC2 in public subnets. The database tier consists of Microsoft SQL Server running on Amazon EC2 in a private subnet. Security is a high priority for the company. How should security groups be configured in this situation?
     - Web Tier: **inbound rule** is required to allow traffic from any internet client to the web front end on SSL/TLS port 443. The source should therefore be set to `0.0.0.0/0` to allow any inbound traffic.
     - Web - DataBase Tier: To secure the connection from the web frontend to the database tier, an **outbound rule** should be created from the public EC2 security group with a destination of the private EC2 security group. The port should be set to 1433 for MySQL. The private EC2 security group will also need to allow inbound traffic on 1433 from the public EC2 security group.
  2. An application is running on Amazon EC2 behind an Elastic Load Balancer (ELB). Content is being published using Amazon CloudFront and you need to restrict the ability for users to circumvent CloudFront and access the content directly through the ELB.
     - The only way to get this working is by using a VPC Security Group for the ELB that is configured to allow only the internal service IP ranges associated with CloudFront. As these are updated from time to time, you can use AWS Lambda to automatically update the addresses. This is done using a trigger that is triggered when AWS issues an SNS topic update when the addresses are changed.

#### NAT Gateway/Instances

![NAT vs IG](https://miro.medium.com/max/1400/1*gftv4LSqU_12kRqNwYISJw.webp)

- NAT gateways/instances provides **private subnets access to internet traffic**, but ensures internet traffic does not initiate a connection with the instances.
- The NAT gateway/instance **must live in a public subnet and then for a private subnet to connect to it**, the private subnet must have a route in its route table that directs traffic to it.
- Use Case: For example this can enable our EC2 Instances in a private subnet to go out and download software by communicating with our Internet Gateway.
- NAT Gateway/Instances works with IPv4
- Exam Tip: A NAT gateway/instance is used for **outbound traffic** not inbound traffic and cannot make applications available to internet-based clients.

##### NAT Instances (legacy)

- NAT Instances are individual EC2 instances. Community AMIs exist to launch NAT Instances. Works same as NAT Gateway.
- NAT instances are managed by you.
- It can be associated with security groups to control inbound and outbound traffic.
- Since NAT Instances send and receive traffic from different sources/destinations, it can cause some issues as EC2 does source/destination checks automatically — so **when using a NAT Instance you need to disable source/destination checks** on the EC2 instance when creating it.

##### NAT Gateway (latest, best practice)

- NAT Gateways are preferred by enterprise as they are **highly available** (redundant instances within the selected AZ), can **scale** and are **managed by AWS**.
  - You can create an AZ independent architecture with Network Gateways to reduce the risks of failures. This can be done by creating a NAT Gateway in each AZ and then configuring the routing to ensure resources in the same NAT Gateway are in the same AZ.
- Can not be associated with security groups, but you can associate the resources behind the NAT Gateway with security groups.
- Automatically assigned public IP Address.
- You don’t need to worry about disabling source & destination checks on the instance.

#### Bastion Host (aka Jump Box)

- A Bastion host is used to **securely administer EC2 instances in private subnet** (using SSH or RDP). From the bastion host they are then able to connect to other instances and applications within AWS by using internal routing within the VPC.
- Exam Tip: A NAT Gateway/Instance is used to provide **outbout traffic** to EC2 instances in a private subnets. **They cannnot be used as Bastion Host**.

#### VPC Flow Logs

- It captures information about **IP traffic information** (not hostnames) entering and leaving interfaces in your VPC.
  - They allow you to monitor the traffic reaching your instances and can help you see if your security groups are restrictive enough.
- They can be created at 3 levels: VPC, Subnet, Network Interface level.
- You can publish these flow logs with CloudWatch or S3. Query VPC flow logs using Athena on S3 or CloudWatch logs insight.
- Flow logs do not impact latency or network throughput as they are collected outside the path of your network traffic.
- You can have flow logs for peered VPCs, but only if they are in same account.

#### VPC Connectivity

- There are several methods of connecting to a VPC, **including connection from Datacenters to VPC**.
  - External DataCenter - AWS VPC
    - AWS Managed VPN
    - AWS Direct Connect
    - AWS Direct Connect plus a VPN
    - AWS VPN CloudHub
    - Software VPN
    - Transit VPC
    - Transit Gateway
  - Among VPCs (Internal to AWS)
    - VPC Peering
    - AWS PrivateLink: VPC Endpoints

##### Case A: External Nextwork (DataCenter or Cloud) - AWS VPC

###### AWS (Managed) VPN

![AWS Managed VPN](https://digitalcloud.training/wp-content/uploads/2022/01/VPC-1.jpg)

- What: AWS-provided network connectivity between two VPCs
  - VPN connection: A secure connection between your on-premises equipment and your VPCs. Each VPN connection includes two VPN tunnels which you can simultaneously use for high availability.
    - VPN tunnel: An encrypted link where data can pass from the customer network to or from AWS.
- When: Multiple VPCs need to communicate or access each other’s resources
- Pros: Uses AWS backbone without traversing the public internet, VPNs are quick, easy to deploy, and cost effective, Secure (Encrypted).
- Cons: Transitive peering is not supported
- How: VPC Peering request made; acceptor accepts request (either within or across accounts)
- Requirements:
  - `Virtual Private Gateway`: It is the **VPN endpoint on the Amazon side** of your Site-to-Site VPN connection that can be attached to a **single VPC**. It is a **redundant** device.
  - Customer gateway device: **One physical device or software application** on the on-premises Data Center side (out of AWS) of the Site-to-Site VPN connection.
  - For route propagation **you need to point your VPN-only subnet’s route tables at the VGW**. (Not Nat gateways)

###### VPN CloudHub

![VPN CloudHub](https://digitalcloud.training/wp-content/uploads/2022/01/VPC-4.jpg)

- What: Connect locations in a **hub and spoke manner** using AWSs `Virtual Private Gateway`
- When: Link remote offices for backup or primary WAN access to AWS resources and each other
- Pros: Reuses existing Internet connections; supports BGP routes to direct traffic
- Cons: Dependent on Internet connections; no inherent redundancy
- How: Assign multiple Customer Gateways to a Virtual Private Gateway, each with their own BGP ASN and unique IP ranges. It can be conbined with Direct Connect.

###### Software VPN

![Software VPN](https://docs.aws.amazon.com/images/whitepapers/latest/aws-vpc-connectivity-options/images/image13.png)

- What: You must provide your own endpoint and software
- When: You must manage both ends of the VPN connection for compliance reasons or you want to use a VPN option not supported by AWS
- Pros: Ultimate flexibility and manageability
- Cons: You must design for any needed redundancy across the whole chain
- How: Install VPN software via Marketplace on an EC2 instance
- It is recommended if you must manage both ends of the VPN connection either for compliance purposes or for leveraging gateway devices that are not currently supported by Amazon VPC’s VPN solution.

###### AWS Direct Connect

![AWS Direct Connect](https://digitalcloud.training/wp-content/uploads/2022/01/VPC-2.jpg)

- What: **Dedicated PRIVATE network connection over private line** straight between AWS and your Data Center
- When: Requires a large network link into AWS; lots of resources and services being provided on AWS to your corporate users. It solves a **VPN connection keeping dropping out** because the amount of throughput.
- Pros: More predictable network performance; potential bandwidth cost reduction; increase in bandwidth throughput (up to 10 Gbps provisioned connections); supports BGP peering and routing
- Cons: May require additional telecom and hosting provider relationships and/or network circuits; costly; It takes time to set up, AWS Direct Connect **does not encrypt** your traffic that is in transit.
- How: Work with your existing data networking provider; create Virtual Interfaces (VIFs) to connect to VPCs (private VIFs) or other AWS services like S3 or Glacier (public VIFs)

| AWS VPN | AWS Direct Connect |
| ------------- | ------- |
| Over the internet connection    | Over the dedicated private connection   |
| Configured in minutes    | Configured in days |
| low to modest bandwidth   | high bandwidth 1 to 100 GB/s |
| encrypted   | no encrypted |

- Use Cases:
  1. A company has acquired another business and needs to migrate their 50TB of data into AWS within 1 month. They also require a secure, reliable and private connection to the AWS cloud ==> AWS Direct Connect provides a secure, reliable and private connection. However, **lead times are often longer than 1 month** so it cannot be used to migrate data within the timeframes.
     - Alternatively, use AWS Snowball to move the data and order a Direct Connect connection to satisfy the other requirement later on. In the meantime the organization can use an AWS VPN for secure, private access to their VPC.
  2. It is required a design for a highly resilient hybrid cloud architecture connecting an on-premises data center and AWS. The network should include AWS Direct Connect (DX). Which DX configuration offers the HIGHEST resiliency?
     - The most resilient solution is to configure DX connections at multiple DX locations. This ensures that any issues impacting a single DX location do not affect availability of the network connectivity to AWS.

###### AWS Direct Connect + VPN

![AWS Direct Connect Plus VPN](https://digitalcloud.training/wp-content/uploads/2022/01/VPC-3.jpg)

- What: **IPSec VPN connection** (encryption) over private lines (Direct Connect), combination of one or more AWS Direct Connect dedicated network connections with the Amazon VPC VPN.
- When: Need the **added security of encrypted tunnels over Direct Connect**
- Pros: More secure (in theory) than Direct Connect alone. This combination provides an IPsec-encrypted private connection that also reduces network costs, increases bandwidth throughput, and provides a more consistent network experience than internet-based VPN connections.
- Cons: More complexity introduced by VPN layer
- How: Work with your existing data networking provider
- Use Case:
  1. An organization is extending a secure development environment into AWS. They have already secured the VPC including removing the Internet Gateway and setting up a Direct Connect connection. What else needs to be done to add encryption?
  - Setup a Virtual Private Gateway (VPG) => A VPG is used to setup an AWS VPN which you can use in combination with Direct Connect to encrypt all data that traverses the Direct Connect link.=> This combination provides an IPsec-encrypted private connection
  - Note: IPSec encryption is not possible to be enabled on the Direct Connect connection => It requires a VPN connection to encrypt the traffic.
  2. Low-cost, short-term option for adding resilience to an AWS Direct Connect connection. What is the MOST cost-effective solution to provide a backup for the Direct Connect connection? => Implement an IPSec VPN connection and use the same BGP prefix. With this option both the Direct Connect connection and IPSec VPN are active and being advertised using the Border Gateway Protocol (BGP). The Direct Connect link will always be preferred unless it is unavailable.

###### Transit Gateway

- A transit **hub** that can be used to interconnect **multiple VPCs** and on-premises networks, and as a VPN endpoint for the Amazon side of the Site-to-Site VPN connection.
- It simplifies your network (no complex peering relationships, do not use route tables).
- It acts as a highly scalable cloud router—each new connection is made only once.
- Difference with Transit VPC: **Transit VPC is more of a network architecture concept while Transit Gateway is a service**.

![Transit Gateway](https://d1.awsstatic.com/products/transit-gateway/product-page-diagram_AWS-Transit-Gateway%402x.921cf305305867447fcabfc6b7acae9f0e5bc9d5.png)

- Use Case:
  1. A company runs a number of core enterprise applications in an on-premises data center. The data center is connected to an Amazon VPC using AWS Direct Connect. The company will be creating additional AWS accounts and these accounts will also need to be quickly, and cost-effectively connected to the on-premises data center in order to access the core applications. Which solution will cause least overhead?
     - Configure AWS Transit Gateway between the accounts. Assign Direct Connect to the transit gateway and route network traffic to the on-premises servers. With AWS Transit Gateway, you can quickly add Amazon VPCs, AWS accounts, VPN capacity, or AWS Direct Connect gateways to meet unexpected demand, without having to wrestle with complex connections or massive routing tables. This is the operationally least complex solution and is also cost-effective.
  2.A company has a Production VPC and a Pre-Production VPC. The Production VPC uses VPNs through a customer gateway to connect to a single device in an on-premises data center. The Pre-Production VPC uses a virtual private gateway attached to two AWS Direct Connect (DX) connections. Both VPCs are connected using a single VPC peering connection. How can this architecture be improved by removing any single point of failure?
     - The only single point of failure in this architecture is the customer gateway device in the on-premises data center. If this device is a single device, then if it fails the VPN connections will fail.  ==> Add additional VPNs to the Production VPC from a second customer gateway device

###### Transit VPC

![Transit VPC](https://docs.aws.amazon.com/images/whitepapers/latest/aws-vpc-connectivity-options/images/image23.png)

- What: Common strategy for connecting geographically dispersed VPCs and locations to create a global network transit center (central hub)
- When: Locations and VPC-deployed assets across multiple regions that need to communicate with one another
- Pros: Ultimate flexibility and manageability but also AWS-managed VPN hub-and-spoke between VPCs. Supports IP Multicast, so can distribute the same content to multiple specific destinations (NOT supported by any other service). Simplify network topology
- Cons: You must design for any redundancy across the whole chain
- How: Providers like Cisco, Juniper Networks, and Riverbed have offerings which work with their equipment and AWS VPC


##### Case B: Among VPCs

######  VPC Peering

![VPC Peering](https://docs.aws.amazon.com/images/vpc/latest/peering/images/peering-intro-diagram.png)

- What: AWS-provided network connectivity between VPCs. It connects two VPC over a direct network route using **private IP addresses** (secure). Instances on peered VPCs behave **just like they are on the same network**.
  - It can connect one VPC to another in same or different region (VPC inter-region peering).
  - It can connect one VPC to another in same or different AWS account.
- When: Multiple VPCs need to connect with one another and access their resources.
- Pros: Uses AWS backbone **without traversing the internet**
- Cons: **Transitive peering is not supported**. Its connections are 1 to 1 (not transitive) i.e. VPC-A peering VPC-B and VPC-B peering to VPC-C doesn’t mean VPC-A peering VPC-C.
- How: VPC Peering request made; accepter request (either within or across accounts). Requirements:
  - Route tables must be updated in both VPC that are peered so that instances can communicate.
  - Must have no overlapping CIDR Blocks.

###### VPC Private Link

![private link](https://d1.awsstatic.com/products/privatelink/product-page-diagram_AWS-PrivateLink.fc899b8ebd46fa0b3537d9be5b2e82de328c63b8.png)

- What: AWS-provided **connectivity technology between VPCs, AWS services and/or datacenters using interface endpoints**, securely on the Amazon network backbone.
- When: Keep private subnets truly private by using the AWS backbone rather than using the public internet. Best way to expose your VPC to hundreds or thousands of other VPC’s. Can secure your traffic and simplify network management.
- Pros: Redundant; uses AWS backbone
- Cons: ?
- How: Create endpoint for required AWS or Marketplace service in all required subnets; access via the provided DNS hostname
- `EXAM TIP`: AWS PrivateLink is NOT the same as ClassicLink
  - ClassicLink may come up in exam questions as a possible (incorrect) answer, so you need to know what it is.
  - ClassicLink allows you to link EC2-Classic instances to a VPC in your account, within the same region
  - EC2-Classic is an old platform from before VPCs were introduced and is not available to accounts created after December 2013.
- VPC endpoints
  - The entrypoint in your VPC that enables to **privately connect a VPC to AWS resources** and it is powered by `Private Link` technology.
  - Services in your VPC **do not require public IP** addresses to communicate with resources in the service. So traffic between your VPC and other services **does not leave the Amazon network**.
  - 2 types:
    - `Interface endpoint` → Attach an **Elastic Network Interface (ENI)** with a private IP address onto your **EC2 instance** for it to communicate to services using AWS network. It serves as an entry point for traffic destined to a AWS supported service.
    - `Gateway endpoint` → Create it as a route table target for traffic to services, like NAT gateways — its supported for **only S3 & Dynamo DB**.

![VPC endpoints](https://docs.aws.amazon.com/images/whitepapers/latest/aws-privatelink/images/connectivity.png)

- **Exam Tip :**: Interface Endpoints can be used for the mayorty of AWS Services (including S3 and DynamoDB) but Gateway Endpoints can only be used for S3 and DynamoDB.

![EC2 and DynamoDB via Gateway endpoint](https://img-c.udemycdn.com/redactor/raw/2020-05-21_01-00-45-ac665c89acb1641afb831f1eb795210e.jpg)

![Interface vs Gateway](https://digitalcloud.training/wp-content/uploads/2022/12/word-image-482401-3.png)

- Use Case:
  - A company runs an application on Amazon EC2 instances which requires access to sensitive data in an Amazon S3 bucket. All traffic between the EC2 instances and the S3 bucket must not traverse the internet and must use private IP addresses. Additionally, the bucket must only allow access from services in the VPC.
    - Private access to public services such as Amazon S3 can be achieved by creating a VPC endpoint in the VPC. For S3 this would be a Gateway endpoint. The bucket policy can then be configured to restrict access to the S3 endpoint only which will ensure that only services originating from the VPC will be granted access.
  - A shared services VPC is being setup for use by several AWS accounts. An application needs to be securely shared from the shared services VPC. The solution should not allow consumers to connect to other instances in the VPC.
    - To restrict access so that consumers cannot connect to other instances in the VPC the best solution is to use PrivateLink to create an endpoint for the application. The endpoint type will be an interface endpoint and it uses an NLB in the shared services VPC.

### Amazon API Gateway

![Amazon API Gateway](https://d1.awsstatic.com/serverless/New-API-GW-Diagram.c9fc9835d2a9aa00ef90d0ddc4c6402a2536de0d.png)

- It is Saas that **creates and manages APIs from back-end systems running on AWS Compute** (EC2, AWS Lambda, etc) or Any other AWS Service
  - It makes easy for developers to publish, maintain, monitor and secure APIs at any scale (auto-scaling).
  - Types - HTTP, WebSocket, and REST.

![API Gateway 2](https://img-c.udemycdn.com/redactor/raw/2020-06-28_20-09-23-7dad959e9a620f37463b0048341769bc.png)

- Options
  - It has **caching** capabilities for a Stage to increase performance ==> When it is enabled the Stage cache responses instead of your endpoint for a specified time-to-live (TTL) period, in seconds (min - max: 0 - 3600).
  - Throttling settings: Allows you to **track and control usage of API** (Set throttle limit (default 10,000 req/s) to prevent from being overwhelmed by too many requests and returns `429 Too Many Request` error response). Different types:
    - AWS throttling limits are applied across all accounts and clients in a region
    - Per-account limits are applied to all APIs in an account in a specified Region
    - Per-API, per-stage throttling limits are applied at the API method level for a stage.
    - Per-client throttling limits are applied to clients that use API keys associated with your usage plan as client identifier
  - You can log results to CloudWatch
- If you are using Javascript/AJAX that uses multiple domains with API Gateway, ensure that you have enable CORS on API Gateway.
  - CORS: Cross-Origin Resource Sharing ==> It is a mechanism that allows restricted resources on a domain (eg: `example.com`) to be requested from another domain outside the domain from which the first resource was served (eg: `fonts.com`).
  - CORS is enforced by the client (Browser)
- Use case: A company has created an application that stores data in an Amazon DynamoDB table. A web application is being created to display the data. Find a couple of designs for the web application using managed services that require minimal operational maintenance => 2 possible solutions:
  - API Gateway REST API that invokes an AWS Lambda function. A Lambda proxy integration can be used, and this will proxy the API requests to the Lambda function which processes the request and accesses the DynamoDB table.
  - API Gateway REST API to directly access data in DynamoDB. In this case a proxy for the DynamoDB query API can be created using a method in the REST API.

### AWS AppSync

- It is a serverless GraphQL and Pub/Sub API service that simplifies building modern web and mobile applications.
- AWS AppSync GraphQL APIs simplify application development by providing a single endpoint to securely query or update data from multiple databases, microservices, and APIs

### AWS Global Accelerator

- KeyWord: Global Redirecction (Non-cache), Optimal routes, HTTP nd non-HTTP

![global_accelerator](https://d1.awsstatic.com/product-page-diagram_AWS-Global-Accelerator%402x.dd86ff5885ab5035037ad065d54120f8c44183fa.png)

- It is a **global service**.
- It Saas which you create accelerators to improve availability and performance of your applications for **global users**.
  - How? It **redirects traffic to closest Edge Location to the user** over the AWS Global network to **reduce latency**.
- Steps:
  - First you create global accelerator using **static IP addresses** (Seamless failover is ensured => IP does not change when failing over between regions so there are no issues with client caches having incorrect entries that need to expire). Two options:
    - Using new static anycast IP
    - Using existing public IPs (migration)
  - Then you register one or more endpoints with Global Accelerator (HTTP nd non-HTTP). Each endpoint can have one or more AWS resources such as NLB, ALB, EC2, S3 Bucket or Elastic IP.
- Within endpoint, global accelerator monitor health checks of all AWS resources to send traffic to healthy resources only
- Adjustment in the Endpoints
  - You can control traffic using traffic dials. This is done within the endpoint group.
  - You can control weighting to individual endpoints using weights (how much traffic is routed to each endpoint)

![Difference with CloudFront](https://jayendrapatil.com/wp-content/uploads/2022/07/AWS-CloudFront-vs-Global-Accelerator.jpg)

### Amazon CloudFront

- Keywords: Global Cache, HTTP applications (websites)

![cloudfront](https://docs.aws.amazon.com/images/AmazonCloudFront/latest/DeveloperGuide/images/how-you-configure-cf.png)

- It is a **global service**.
- It is a **Content Delivery Network (CDN)** uses `AWS edge locations` to **cache and securely deliver** cached content (such as images and videos) based on the **geographic locations** of the user, the origin of the webpage and a content delivery server (Requests to content are automatically routed to nearest geographical edge location). Advantages ==> **Low latency and high transfer speeds**.
  - `Edge Location` → Location where content will be cached (different to an AWS Region). It can be used for read and write.
  - `Origin` → Location that hosts all the files that the CDN will distribute — can be an S3 Bucket, EC2, ELB etc (Any type of AWS resource).
  - `Distribution` → Name of the CDN, which consists of a collection of edge locations. There are two types:
    - Web Distributions which are used for websites (Download Data)
    - RTMP Distributions which are used for streaming media (Stremming Access)
  - `Invalidations` → these can be files or subfolders that you can select to not be on the edge locations. Useful when you need to remove a file from an edge cache before it expires
  - `Versioning` → can be used to serve a different version of a file under a different name.
- Objects are cached for the `Time To Live (TTL)` - default 24 hours.
  - **If requested resources does not exist on CloudFront — it will query the original server and then cache it on the edge location**. Next requests get a cached copy from the Edge Location instead of downloading it again from the server until TTL expires.
  - It is possible to clear cached objects, however you will incur a charge.
- Can integrate with AWS Shield, Web Application Firewall and Route 53 to advance security (to protect from layer 7 attacks).
- It supports **Geo restriction (Geo-Blocking)** to whitelist or blacklist countries that can access the content.
- Use Cases:
  1. A company offers an online product brochure that is delivered from a static website running on Amazon S3. The company’s customers are mainly in the United States, Canada, and Europe. With Amazon CloudFront you can set the price class to determine where in the world the content will be cached. One of the price classes is “U.S, Canada and Europe” and this is where the company’s users are located. Choosing this price class will result in lower costs and better performance for the company’s users.
  2. A company runs a web application that serves weather updates. The application runs on a fleet of Amazon EC2 instances in a Multi-AZ Auto scaling group behind an Application Load Balancer (ALB). How to make the application more resilient to sporadic increases in request rates?
     - On the frontend an Amazon CloudFront distribution can be placed in front of the ALB and this will cache content for better performance and also offloads requests from the backend.
  3. An organization want to share regular updates about their charitable work using static webpages. The pages are expected to generate a large amount of views from around the world. The files are stored in an Amazon S3 bucket. How to design an efficient and effective solution => Amazon CloudFront can be used to cache the files in edge locations around the world and this will improve the performance of the webpages. Possible configuration. Using a REST API endpoint or Using a website endpoint as the origin with anonymous (public) access allowed or with access restricted by a Referer header.
  4. An Amazon S3 bucket in the us-east-1 Region hosts the static website content of a company. The content is made available through an Amazon CloudFront origin pointing to that bucket. A second copy of the bucket is created in the ap-southeast-1 Region using cross-region replication. The chief solutions architect wants a solution that provides greater availability for the website. Which combination of actions should be taken to increase availability?
     - You can set up CloudFront with origin failover for scenarios that require high availability. To get started, you create an origin group with two origins: a primary and a secondary. If the primary origin is unavailable or returns specific HTTP response status codes that indicate a failure, CloudFront automatically switches to the secondary origin.
  5. A company runs a dynamic website that is hosted on an on-premises server in the United States. The company is expanding to Europe and is investigating how they can optimize the performance of the website for European users. The website’s backed must remain in the United States. The company requires a solution that can be implemented within a few days. Best Practice => A custom origin can point to an on-premises server and CloudFront is able to cache content for dynamic websites. Additionally, connections are routed from the nearest Edge Location to the user across the AWS global network. If the on-premises server is connected via a Direct Connect (DX) link this can further improve performance.
  6. An application generates **unique files** that are returned to customers after they submit requests to the application. The application uses an Amazon CloudFront distribution for sending the files to customers. The company wishes to reduce data transfer costs without modifying the application. How can this be accomplished?
     - Use Lambda@Edge to compress the files as they are sent to users
     - Using caching capabilities on the CloudFront is not an valid option as the files are unique and will not be cached.

#### Restricting Access to CloudFront: (Pre-)Signed URL or (Pre-)Signed Cookies

- It is used to restrict access to the resource to certain people so that it is **only accessible through CloudFront and not directly through the AWS resource**.
  - If your origin is EC2, then use CloudFront Signed URL.
  - If your origin is S3, then use S3 signed URL (instead of CloudFront Signed URL).
- You can restrict access using signed URLs or Signed Cookies.
  - A signed URL is for individual files, 1 files = 1 URL.
  - A signed cookie is for multiple file, 1 cookie = multiple files.
- When we create a signed URL or signed cookie, a policy is attached that includes:
  a. URL expiration.
  b. IP ranges
  c. Trusted Signers (which AWS accounts can create signed URL's)
- Use Case: Netflix - Option in AWS CloudFront is "Restrict Viewer access (Use Signed URL's or Signed cookies)"

##### Features of a signed url

- The signed url (key pair) is account wide & managed by the root user.
- Has an associated policy statement (JSON) specifying restrictions on the URL.
- Contains additional information e.g. expiration date/time.
- Can have different origins and can utilise caching features.

##### Lambda@Edge

- It is a feature of Amazon CloudFront that lets you run code closer to users of your application, which improves performance and reduces latency.
- It runs code in response to events generated by the Amazon CloudFront.

##### CloudFront Functions

- Feature in Cloudfront whih supports lightweight functions in JavaScript for high-scale, latency-sensitive CDN customizations.
- Your functions can manipulate the requests and responses that flow through CloudFront, perform basic authentication and authorization, generate HTTP responses at the edge, and more.
- Difference with Lambda@Edge
  - It is cheaper
  - Lower latency: functions are run on the host in the edge location, instead of the running on a Lambda function elsewhere.

### Amazon Route 53

![route53](https://d1.awsstatic.com/Route53/product-page-diagram_Amazon-Route-53_HIW%402x.4c2af00405a0825f83fca113352b480b19d9210e.png)

- It is a Saas for **DNS** highly available, universal (not region specific) and scalable
- It allows you to perform **Domain Registration, DNS routing and also Health Checking**.
  - If you want to use Route 53 for domain purchased from 3rd party websites (example GoDaddy).
    - AWS - You need to create a Hosted Zone in Route 53
    - 3 party DNS provider - update the 3rd party registrar NS (name server) records to use Route 53.
- It also works well with other AWS services — it allows you to connect requests to your infrastructure such as to EC2 instances, ELBs or S3 buckets.
- Private Hosted Zone is used to create an internal (intranet) domain name to be used within Amazon VPC. You can then add some DNS record and routing policy for that internal domain. That internal domain is accessible from EC2 instances or any other resource within VPC.

#### Terminology

- `Internet Protocol (IP)` → is a numerical label assigned to devices and used by computers to identify each other on a network.
- `Domain Name System (DNS)` → used to convert human friendly domain names into IP addresses.
- `Domain Registrars` → authority that can assign domain names.
- `Start of Authority Record (SOA)` → type of resource record that every DNS must begin with, it contains the following information:
  - Stores the name of the server supplying the data
  - Stores the admin zone
  - Currently version of data file
  - Time to live
- `Name Server (NS) records` → used by top level domain servers to direct traffic to the content DNS server. It specifies which DNS server is authoritative for a domain.
- `Address Record`
  - `A Records` →  It indicates the **IPv4 address** of a given hostname or domain.
  - `AAAA Records` →  It indicates the **IPv6 address** of a given hostname or domain.

```txt
NAME                    TYPE   VALUE
--------------------------------------------------
foo.example.com.        A      192.0.2.23
```

- `Canonical Name (CName)` → It maps one domain name (an _alias domain_) to another domain (the _canonical name_). It is convenient when running multiple services in the same IP. **Only works with subdomains** e.g. `something.mydomain.com`

```txt
NAME                    TYPE   VALUE
--------------------------------------------------
bar.example.com.        CNAME  foo.example.com.
```

When an A record lookup for bar.example.com is carried out, the resolver will see a CNAME record and restart the checking at foo.example.com and will then return 192.0.2.23.

- `Alias Record` → It provide CNAME-like behavior on apex domains (a naked/root domain name e.g. example.com). It works with both **root-domain and subdomains**
  - **Alias records are used to map DNS with AWS resources** like ALB, API Gateway, CloudFront, S3 Bucket, Global Accelerator, Elastic Beanstalk, VPC interface endpoint etc. [How do I create alias records for services hosted in AWS](https://repost.aws/knowledge-center/route-53-create-alias-records)
  - It is a Route 53 specific feature. This options is available inside the wizard configuration when creating a types of DNS Record. But only `A` and `AAAA` records offers link options to AWS Resources (_ALB_,_Global Accelerator_,_API Gateway_), the rest (e.g `CNAME`, `TXT`) don't, only Alias to _another record in the hosted zone_.

```txt
example.com Alias(A) dualstack.elb123.us-east 1.elb.amazonaws.com.
```

![CNAME-vs-Alias-Records](https://jayendrapatil.com/wp-content/uploads/2022/04/Route-53-CNAME-vs-Alias-Records.jpg)

- `Time To Live (TTL)` → length of time the DNS record is cached on the server for in seconds. Default is 48 hours.

#### DNS Record: Routing Policy

**Exam Tip**: For Applying any type of Routing Policy is required more that one endpoint (AWS reasource). Exception: Simple Routing Policy.

In order for Route 53 to respond to queries, you need to define one of the following routing policies:

- `Simple` You can only have **one record with multiple IP addresses**. If you specify multiple values in a record, Route 53 returns all values to the user in a random order — so you never know which EC2 you are hitting and it can be shuffled on refreshed!
  - You **can't have any health checks**.
- `Multivalue Answer` configure Amazon Route 53 to return multiple values, such as IP addresses for your web servers, in response to DNS queries.
  - You can specify multiple value for almost any record, but multivalue answer routing also lets you check the health of each resource, so Route 53 returns only values from healthy resources.
  - Similar to Simple Routing only **you can put health checks** on each record set so that only healthy resources are returned.
  - Use case: Your company hosts 10 web servers all serving the same web content in AWS. They want Route 53 to serve traffic to random web servers.
  - Example: create 3 DNS records with associated health check. Acts as client side Load Balancer, expect a downtime of TTL, if an EC2 becomes unhealthy.
- `Weighted` Split traffic based on different **custom proportions** you assign.
  - You can set health checks on individual record sets. If a recordset fails a health check it will be removed from Route53 until it passes the health check.
  - Example: you can set 10% of your traffic to go to US-EAST-1 and 90% to EU-WEST-1.
- `Latency` Allows you to route your traffic based on the **lowest network latency** for your end user (ie which region will give them the fastest response time).
  - Example: create 3 DNS records with region us-east-1, eu-west-2, and ap-east-1.
- `Failover` to route traffic from Primary to Secondary (**DR scenario**) in case of **failover (active/passive set-up)**
  - It is **mandatory to create health check for both IP and associate to record**. The traffic goes to main site when its healthy and then can route traffic to the secondary site when the main one becomes unhealthy.
  - Example create 2 DNS records: for primary site in EU-WEST-2 and secondary (DR) IP in AP-SOUTHEAST-2.
- `Geolocation` to route traffic to specific IP based on **user geolocation (select Continent or Country)**.
  - For this you need to create **separate record sets for each required location**. It also requires a default (select Default location) policy in case there’s no match on location.
  - For Example: You might want all queries from Europe to be routed to a fleet of EC2 instances that are specifically configured for European customers. These servers may have the local language of European customers and all prices are displayed in Euros.
- `Geoproximity` to route traffic to specific IP based on **user AND AWS resources geolocation**.
  - You can also optionally choose to route more traffic or less to a given resource by specifying a value, known as a bias A bias expands or shrinks the size of the geographic region from which traffic is routed to a resource.
  - To use Geoproximity Routing, you must use **Route 53 traffic flow**.

- Use Case: A company hosts data in an Amazon S3 bucket that users around the world download from their website using a URL that resolves to a domain name. The company needs to provide low latency access to users and plans to use Amazon Route 53 for hosting DNS records.
  - The best solution here is to use Amazon CloudFront to cache the content in Edge Locations around the world. This involves creating a web distribution that points to an S3 origin (the bucket) and then create **an Alias** record in Route 53 that resolves the applications URL to the CloudFront distribution endpoint with **Simply routing**.
  - In this scenarios routing strategies like `Geoproximity` would not work ==> There is only a single endpoint (the Amazon S3 bucket) so this strategy would not work. Much better to use CloudFront to cache in multiple locations.

#### DNS Failover

- `Active-Active` failover when you want all resources to be available the majority of time. All records have same name, same type, and same routing policy such as **weighted or latency**
- `Active-Passive` failover when you have active primary resources and standby secondary resources. You create two records - primary & secondary with **failover routing policy**

## Management_and_Governance

Go to [Index](#index)

### Amazon CloudWatch

![cloudwatch](https://d1.awsstatic.com/reInvent/reinvent-2022/cloudwatch/Product-Page-Diagram_Amazon-CloudWatch.095eb618193be7422d2d34e3abd5fdf178b6c0e2.png)

- It is Saas for **monitoring & observability** of AWS resources (EC2, ALB, S3, Lambda, DynamoDB, RDS etc.) and applications to watch **performance**.
- It can collect these Inputs: **Metrics and Log files**.
  - Exam Tip: There is a list for [existing metrics](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html) but **Custom Metrics cannot be created**.
- It allows you to create these Outputs:
  - `Dashboards`: Creates dashboards to see what is happening with your AWS environment
  - `Alarms`: Allows you to set Alarms that notify you when particular metric thresholds are hit
  - `Events`: CloudWatch Events helps you to respond to state changes in your AWS resources.
  - `Logs`: CloudWatch Logs helps you to aggregate, monitor and store logs.
- Share Dashboards to people outside the AWS account/organization (or embeed CloudWatch Dashboards into an external website) => CloudWatch > Dashboard > Select your board > Share Dashboard >Share your dashboard and require a username and password>Enter mail address.

#### CloudWatch with EC2

- It can monitor EC2 at host level: CPU, Network, Disk, Status Check
- It monitors every 5 mins by default (Can switch to every 1min by enabling `Detailed Monitoring`)
- You can terminate or recover EC2 instance based on CloudWatch Alarm

#### The Unified CloudWatch agent

- It collect both system metrics and log files **from Amazon EC2 instances (Linux and Windows) and on-premises servers**, enables you to select the metrics to be collected, including sub-resource metrics such as per-CPU core or Swap utilization.

#### CloudWatch Container Insights

- Use this component to collect, aggregate, and summarize metrics and logs from your **containerized applications and microservices**.
- It is availabble for: Amazon Elastic Container Service (Amazon ECS), Amazon Elastic Kubernetes Service (Amazon EKS), and Kubernetes platforms on Amazon EC2.
- It enables to see top contributors by memory or CPU, or the most recently active resources once you select on of the following dashboard: ECS Services, ECS Tasks, EKS Namespaces, EKS Services, EKS Pods.

### AWS X-Ray

- Analyze and debug production and **distributed applications (microservices)** ==> by **Tracing Requests** as they travel through your application and filters visual data across payloads, functions, traces, services, APIs, and more with no-code and low-code motions.
- Difference with Cloudwatch: It does not use health checks, metrics or central dashboards.

![xray](https://d1.awsstatic.com/Product-Page-Diagram_AWS-X-Ray.6fd8b61bc76bd93741fc209c2afc194b494bff9a.png)

![tracing-output](https://docs.aws.amazon.com/images/xray/latest/devguide/images/scorekeep-PUTrules-timeline.png)

### AWS CloudTrail

![CloudTrail](https://d1.awsstatic.com/product-marketing/CloudTrail/product-page-diagram_AWS-CloudTrail_HIW.feb63815c1869399371b4b9cc1ae00e78ed9e67f.png)

- It is Saas for governance, compliance & operational **auditing**, security analysis.
  - It collect as Inputs: of all the **actions taken on any user on Management Console, AWS service, CLI, or SDK across AWS infrastructure**.
  - Can detect user behaviour patterns and also unusual activity.
- CloudTrail works per AWS account and is configured per region.
  - It is **enabled by default for all regions**.
  - It can consolidate logs using S3 bucket:
    - Turn on CloudTrail in paying account.
    - Create a bucket policy that allows cross-account access.
    - Turn on CloudTrail in the other accounts and use the bucket in the paying account.
- Use case:
  1. Check in the CloudTrail if any resource is deleted from AWS without anyone’s knowledge.
  2. A company plans to provide developers with individual AWS accounts. The company will use AWS Organizations to provision the accounts. A secure auditing using AWS CloudTrail must be implemented so that all events from all AWS accounts are logged. The developers must not be able to use root-level permissions to alter the AWS CloudTrail configuration in any way or access the log files in the S3 bucket. The auditing solution and security controls must automatically apply to all new developer accounts that are created.
     - Create a CloudTrail trail in the management account with the organization trails option enabled and this will create the trail in all AWS accounts within the organization.
     - Member accounts can see the organization trail but can't modify or delete it. By default, member accounts don't have access to the log files for the organization trail in the Amazon S3 bucket.

### AWS CloudFormation

![CloudFormation](https://d1.awsstatic.com/Products/product-name/diagrams/product-page-diagram_CloudFormation.ad3a4c93b4fdd3366da3da0de4fb084d89a5d761.png)

- Allows you to provision AWS resources as code. Infrastructure as Code (IaC).
  - Create, update, or delete your stack of resources using CloudFormation Template (blue prints) as a JSON or YAML file.
- It simplifies infrastructure management and also makes it very easy to replicate infrastructure across different regions.
  - Use case: Use to setup the same infrastructure in different environment for e.g. SIT, UAT and PROD. Use to create DEV resources everyday in working hours and delete later to lower the cost
- Using CloudFormation itself is free, underlying AWS resources are charged

#### Template Sections

- There are ten valid sections a CloudFormation template can contain, however they are not all required:
  - Resources — specify the actual resources you want to create (REQUIRED)
  - Parameters — Any values that you want to pass into your template at run time. (Optional)
  - Rules — used to validate parameters passed into the stack (Optional)
  - Mappings — mapping of key value pairs that can be used to specify conditions (Optional).
    - Exam tip: with mappings you can, for example, set values based on a region. You can create a mapping that uses the region name as a key and contains the values you want to specify for each specific region.
  - Outputs — values that are displayed when you check the stacks properties (Optional)
  - Conditions — can control whether a resource is created or whether certain properties are assigned depending on a particular criteria. (Optional)
  - Format Version — Version that the template conforms to (Optional)
  - Description — Describes what the template is used for. This is optional, but if you use it, it needs to follow the Format Version.
  - MetaData — any additional info about the template. (Optional)
  - Transform — used for serverless applications, allows you to specify the SAM version to use (Optional)
- Allows `DependsOn` attribute to specify that the creation of a specific resource follows another
- Allows `DeletionPolicy` attribute to be defined for resources in the template
  - retain to preserve resources like S3 even after stack deletion
  - snapshot to backup resources like RDS after stack deletion
- Supports Bootstrap scripts to install packages, files and services on the EC2 instances by simple describing them in the template
- automatic rollback on error feature is enabled, by default, which will cause all the AWS resources that CF created successfully for a stack up to the point where an error occurred to be deleted.

#### Serverless Application Model (SAM)

- Is an open-source framework that extends CloudFormation so that it is optimised for serverless applications (e.g. Lambdas, API’s, databases etc.)
- It supports anything CloudFormation supports.
- Also uses templates to define resources and these templates are in a YAML format.
- Can run serverless applications locally using docker.

### AWS Elastic Beanstalk (PaaS)

![ElasticBeanstalk](https://d1.awsstatic.com/Product-Page-Diagram_AWS-Elastic-Beanstalk%402x.6027573605a77c0e53606d5264ec7d3053bf26af.png)

- Platform as a Service (PaaS) ==> Automatically handles the Deployment Details (Architecture Design): capacity provisioning, load balancing, auto-scaling and application health monitoring
- You can launch an applications with following **pre-configured platforms (Templates)**:
  - Apache Tomcat for Java applications,
  - Apache HTTP Server for PHP and Python applications
  - Nginx or Apache HTTP Server for Node.js applications
  - Passenger or Puma for Ruby applications
  - Microsoft IIS 7.5 for `.NET` applications
  - Single and Multi Container Docker
- You can also launch an environment with following environment tier:
  - An application that serves HTTP requests runs in a web server environment tier.
  - A backend environment that pulls tasks from an Amazon Simple Queue Service (Amazon SQS) queue runs in a worker environment tier.
- Simplify developers tasks to quickly deploy and manage applications without thinking about underlying resources.
- It costs nothing to use Elastic Beanstalk, only the resources it provisions e.g. EC2, ASG, ELB, and RDS etc.

### AWS ParallelCluster

- KeyWords: HPC

![ParallelCluster](https://d1.awsstatic.com/HPC2019/Product-Page-Diagram_Paralell-Cluster_How-It-Works.50eb43991f5baa11d4d7687ac8155ed7943341ef.png)

- Open-source cluster management tools **deploy and manage High Performance Computing (HPC) clusters** resources on AWS (VPC, subnet, cluster type and instance types.) using GUI or a simple text file for modeling and provisioning.
- You have full control on the underlying resources.
- AWS ParallelCluster is free, and you pay only for the AWS resources needed to run your applications.

### AWS Step Functions (SF)

- KeyWords: Orchestration, Visual Configuration (No Code)

![AWSStepFunctions](https://d1.awsstatic.com/video-thumbs/Step-Functions/AWS_Step_Functions_HIW.bc3d2930f00dd0401269367b8e8617a7dba5915c.png)

- Visual workflow service that helps developers use AWS services to build distributed applications, **automate processes**, **orchestrate** microservices, and create data and **machine learning (ML) pipelines**.
- You write state machine in declarative JSON, you write a decider program to separate activity steps from decision steps.

![steps-function](https://imgix.datadoghq.com/img/knowledge-center/aws-step-functions/aws-step-functions-visual-editor.png?auto=format&fit=max&w=847)

### AWS Simple Workflow Service (SWF)

- It is a service that makes it easy to **coordinate work across distributed application components** in the AWS Cloud.
- A task represents a logical unit of work that is performed by a component of your workflow. SWF coordinates tasks in a workflow involving the manage intertask dependencies, schedulle, and concurrency in accordance with the logical flow of the application.
- Use cases: including media processing, web application back-ends, business process workflows and analytics pipelines, to be designed as a coordination of tasks.

### AWS Organization

![Organization](https://d1.awsstatic.com/diagrams/organizations-HIW.1870c83be9fdfc55680172a1861080a91b700fff.png)

- Global Services that lets you create new AWS accounts at no additional charge.
  - With accounts in an organization, you can easily allocate resources, group accounts, and apply governance policies to accounts or groups, **consolidate billing across all accounts (single payment method)**
  - It has a master account and multiple member accounts
  - Member Acccounts or `Organization Units (OUs)` are based on department, cost center or environment, OU can have other OUs (hierarchy)
  - <a name="scp">`Service Control Policies (SCPs)` (IAM Organization Policy)</a>
    - It can work at OU level or account level
    - It offers central control over the maximum available permissions for all accounts in your organization.
    - It helps you to ensure your accounts stay within your organization’s access control guidelines.
- Best practices with AWS Organizations.
  - Always enable multi-factor authentication on root or master account.
  - Always use strong and complex passwords on root account.
  - Paying account should be used for billing purposes only. Do not deploy resources into the paying account, into the root account or the master account.
  - Enable and disable AWS services using service control policies (SCPs) either on organisational units or on individual accounts.
- Use Cases:
  1. An AWS Organization has an OU with multiple member accounts in it. The company needs to restrict the ability to launch only specific Amazon EC2 instance types. How can this policy be applied across the accounts with the least effort?
     - Use a Service Control Policy (SCP) in the AWS Organization. The way you would do this is to create a deny rule that applies to anything that does not equal the specific instance type you want to allow.
  2. A company has divested a single business unit and needs to move the AWS account owned by the business unit to another AWS Organization. How can this be achieved?
     - Migrate the account using the AWS Organizations console. To do this you must have root or IAM access to both the member and master accounts. Resources will remain under the control of the migrated account.

#### Consolidated Billing

- It helps to consolidate billing and payment for multiple AWS accounts.
- Consolidated billing has the following benefits:
  - One bill – You get one bill for multiple accounts.
  - Easy tracking – You can track the charges across multiple accounts and download the combined cost and usage data.
  - Combined usage – You can combine the usage across all accounts in the organization to share the volume pricing discounts, Reserved Instance discounts, and Savings Plans. This can result in a lower charge for your project, department, or company than with individual standalone accounts. For more information, see Volume discounts.
  - No extra fee – Consolidated billing is offered at no additional cost.

### AWS Control Tower

- It automates the setup of a new landing zone using best practices blueprints for identity, federated access, and account structure.
- The account factory automates provisioning of new accounts in your organization. As a configurable account template, it helps you standardize the provisioning of new accounts with pre-approved account configurations. You can configure your account factory with pre-approved network configuration and region selections.

### AWS OpsWorks

- It is a Managed **Configuration as Code** Service that lets you use Chef and Puppet to automate how server are configured, deployed, managed across EC2 instances using Code.
- OpsWork Stack let you model you application as a stack containing different layers, such as load balancing, database, and application server.

### AWS Glue

- It is a **ETL (extract, transform, and load)** Saas.
- AWS Glue Crawler scan data from data source such as S3 or DynamoDB table, determine the schema for data, and then creates metadata tables in the AWS Glue Data Catalog.
- AWS Glue provide classifiers for CSV, JSON, AVRO, XML or database to determine the schema for data

### AWS Cost Management

- `AWS Compute Optimizer` --> Ii helps **avoid overprovisioning (reduce cost) and underprovisioning** four  types of AWS resources—Amazon Elastic Compute Cloud (EC2) instance types, Amazon Elastic Block Store (EBS) volumes, Amazon Elastic Container Service (ECS) services on AWS Fargate, and AWS Lambda functions—based on your utilization data.
- `AWS Trusted Advisor` --> It provides recommendations that help you follow AWS best practices. Trusted Advisor evaluates your account by using checks. These checks identify ways to optimize your AWS infrastructure, improve security and performance, reduce costs, and monitor service quotas.
  - Examp Tip: `AWS Compute Optimizer` is better for computing resources, `AWS Trusted Advisor` is a more general advisor covering more areas.
- `AWS Cost Explorer` --> It gives you insight into your spend and usage in a graphical format (it does not make any recommendations).

### AWS Batch

- Keywords: Batch computing
- It empowers developers, scientists, and engineers to run efficiently **hundreds of thousands of batch** and ML computing jobs **running in parallel** while optimizing compute resources, so you can focus on analyzing results and solving problems. Removes the heavy lifting of configuring and managing the required infrastructure,

### AWS Outposts

- It is a fully managed service that **extends virtually** any AWS infrastructure, AWS services, APIs, and tools to **any datacenter (on-premises)**, co-location space, or on-premises facility for a truly consistent hybrid experience.
- AWS Outposts is good for workloads that require **low latency** access to on-premises systems, local data processing, or local data storage.

![Outposts architecture example](https://documentation.commvault.com/img/129254.png)

## References

After doing the course from [Digital Training](https://digitalcloud.training/aws-cheat-sheets/), I reviwed the following resources to make this summary:

- [Amazon Docs](https://aws.amazon.com/)
- [AWS Certified Solutions Architect Associate (SAA-C02) Exam Notes - Coding N Concepts](https://codingnconcepts.com/aws/aws-certified-solutions-architect-associate)
- [AWS_CCP_Notes/AWS_Solution_Architecture_Associate.txt at main · kasukur/AWS_CCP_Notes](https://github.com/kasukur/AWS_CCP_Notes/blob/main/AWS_Solution_Architecture_Associate.txt)
- [AWS Solution Architect Associate Exam Study Notes | by Chloe McAteer | Medium](https://chloemcateer.medium.com/aws-solution-architect-associate-exam-study-notes-b6c5884ee500)

Finally, I practiced the following Exam Tests `AWS Certified Solutions Architect Associate Practice` from Udemy.
