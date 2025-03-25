# Birthday Reminder Application

[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![Helm](https://img.shields.io/badge/helm-%230F1689.svg?style=for-the-badge&logo=helm&logoColor=white)](https://helm.sh)

A cloud-native application that manages user birthdays with Kubernetes deployment and AWS infrastructure design.

---

## Features

- REST API for managing birthdays:
  - `PUT /hello/<username>` - Store/update a user's birthday.
  - `GET /hello/<username>` - Retrieve a birthday message.
- PostgreSQL database for persistent storage.
- Helm chart for easy Kubernetes deployment.
- Designed for high availability and scalability on AWS.

---

## Repository Structure
```
TitanOStest/birthday-app
├── app/                 # Application code
│   ├── app.py           # Flask application
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile       # Dockerfile for containerization
├── helm-chart/          # Helm chart for Kubernetes deployment
│   ├── Chart.yaml       # Chart metadata
│   ├── values.yaml      # Default configuration
│   ├── requirements.yaml # Helm chart dependencies
│   └── templates/       # Kubernetes manifest templates
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── configmap.yaml
│       ├── secret.yaml
│       ├── db-deployment.yaml
│       ├── db-service.yaml
│       └── pvc.yaml
├── docs/                # Documentation and diagrams
│   ├── aws-system-diagram.drawio
│   └── aws-infra-explanation.md
└── README.md           # This file
```

---

## System Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                            AWS Cloud                               │
│                                                                     │
│  ┌─────────────┐        ┌─────────────────┐        ┌─────────────┐  │
│  │  ALB        │        │    EKS Cluster  │        │  RDS        │  │
│  │ (Internet   │        │ ┌─────────────┐ │        │ PostgreSQL  │  │
│  │  Facing)    │◄───────┼─┤  Birthday   │ │◄───────┤ (Multi-AZ)  │  │
│  └─────────────┘        │ │  App Pods   │ │        └─────────────┘  │
│                         │ └─────────────┘ │                         │
│                         │ ┌─────────────┐ │                         │
│                         │ │   PostgreSQL│ │                         │
│                         │ │   Service   │ │                         │
│                         │ └─────────────┘ │                         │
│                         └─────────────────┘                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

### Components:
1. **Application Layer**:
   - Flask-based REST API.
   - Handles user requests and interacts with the database.
2. **Database Layer**:
   - PostgreSQL for storing user data.
   - Persistent storage using Kubernetes PersistentVolumeClaims (PVC).
3. **Kubernetes Layer**:
   - Deployed using Helm for easy management.
   - Includes Deployments, Services, ConfigMaps, and Secrets.
4. **AWS Infrastructure**:
   - EKS for managed Kubernetes.
   - RDS for PostgreSQL database.
   - ALB for load balancing.
   - VPC for secure networking.
   - CloudWatch for monitoring and logging.

---

## Prerequisites

- Docker
- Minikube or k3s
- Helm 3.x
- kubectl

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/rgreposito/TitanOStest.git
cd TitanOStest
```

### 2. Build the Docker Image
```bash
docker build -t birthday-app:latest ./app
```

### 3. Start Minikube
```bash
minikube start
minikube addons enable ingress
```

### 4. Update Helm Dependencies
```bash
helm dependency update ./helm-chart
```

### 5. Deploy with Helm
```bash
helm install birthday-app ./helm-chart
```

### 6. Verify Deployment
```bash
kubectl get pods,svc,pvc
```

## API Usage

### Store/Update Birthday
```bash
curl -X PUT -H "Content-Type: application/json" \
  -d '{"dateOfBirth": "1990-01-01"}' \
  http://$(minikube ip):30007/hello/john
```

### Get Birthday Message
```bash
curl http://$(minikube ip):30007/hello/john
```

Sample Responses:
- If birthday is today:
```json
{"message":"Hello, john! Happy birthday!"}
```
- If birthday is in 5 days:
```json
{"message":"Hello, john! Your birthday is in 5 day(s)"}
```

## Helm Chart Structure

The Helm chart is structured as follows:

```
helm-chart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration
├── requirements.yaml   # Chart dependencies (e.g., PostgreSQL)
└── templates/          # Kubernetes manifest templates
    ├── deployment.yaml # App deployment specs
    ├── service.yaml    # Network exposure
    ├── configmap.yaml  # Non-sensitive config
    ├── secret.yaml     # Credentials management
    ├── db-deployment.yaml # Postgres setup
    ├── db-service.yaml # Database networking
    └── pvc.yaml        # Persistent storage
```

## AWS Infrastructure Design

The application is designed for high availability and scalability on AWS. Key components include:

### Amazon EKS:
- Managed Kubernetes cluster.
- Worker nodes spread across multiple Availability Zones (AZs).

### RDS PostgreSQL:
- Multi-AZ deployment for high availability.
- Automated backups and read replicas.

### Application Load Balancer (ALB):
- Routes external traffic to the application.
- SSL termination using ACM certificates.

### VPC Networking:
- Public and private subnets.
- NAT gateways for outbound internet access.

### Auto Scaling:
- Cluster Autoscaler for EKS nodes.
- Horizontal Pod Autoscaler for the application.

### Monitoring & Logging:
- CloudWatch for metrics and alarms.
- CloudTrail for API monitoring.

### Security:
- IAM roles for service accounts.
- Security Groups for network isolation.

For a detailed explanation, see the AWS Infrastructure Documentation.

## Cleanup

To remove the deployment and clean up resources:

```bash
helm uninstall birthday-app
minikube delete
```

## License

This project is licensed under the Apache 2.0 License. See LICENSE for details.

## System Diagram (ASCII Representation)

```
┌───────────────────────────────────────────────────────────────┐
│                           AWS Cloud                           │
│                                                               │
│  ┌─────────────┐       ┌─────────────┐       ┌─────────────┐  │
│  │    ALB      │       │    EKS      │       │    RDS      │  │
│  │ (Load       │       │ (Kubernetes │       │ (PostgreSQL │  │
│  │  Balancer)  │◄──────►  Cluster)   │◄──────►  Database)  │  │
│  └─────────────┘       └─────────────┘       └─────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```
