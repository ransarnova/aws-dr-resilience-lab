# Disaster Recovery Requirements

## System

Order API

## Business Criticality

Business-critical application.

## Availability Target

99.9%

## Recovery Objectives

### Recovery Time Objective (RTO)

15 minutes.

The application must resume service within 15 minutes of a
qualifying regional disaster.

### Recovery Point Objective (RPO)

5 minutes.

A maximum of five minutes of data loss is acceptable following
a qualifying disaster.

## AWS Regions

Primary:

ap-south-1

Disaster Recovery:

ap-southeast-1

## Initial Architecture

Route 53
→ Application Load Balancer
→ Amazon EKS
→ FastAPI Order Service
→ DynamoDB

## Failure Domains

The DR strategy will consider failures at the following levels:

- Application process
- Kubernetes pod
- Kubernetes worker node
- Availability Zone
- EKS cluster
- AWS managed service
- AWS Region
- Application deployment
- Data corruption or accidental deletion
- Security or credential incident

## Recovery Principles

1. Infrastructure should be reproducible through Infrastructure as Code.
2. Recovery should minimize manual intervention.
3. Recovery procedures must be measurable and testable.
4. Data recovery and infrastructure recovery must be considered separately.
5. Replication must not be treated as a replacement for backup.
6. Recovery procedures must account for application dependencies.
7. DR architecture should balance RTO, RPO, complexity, risk and cost.

## DR Strategy Classification Exercise

| Workload | RTO | RPO | Candidate Strategy |
|---|---|---|---|
| A | 24 hours | 24 hours | Backup and Restore |
| B | 4 hours | 1 hour | Pilot Light |
| C | 15 minutes | 5 minutes | Warm Standby |
| D | <1 minute | Near-zero | Active-Active |

DR patterns are selected based on business recovery objectives rather
than application criticality alone.

RTO and RPO must be evaluated independently. Application and
infrastructure readiness primarily affect recovery time, while data
replication and recovery mechanisms strongly influence achievable RPO.

Active-active architectures should be adopted when justified by recovery
requirements because they introduce additional cost and complexity
around traffic management, data consistency, concurrent writes,
conflict resolution, regional dependencies, and operational testing.