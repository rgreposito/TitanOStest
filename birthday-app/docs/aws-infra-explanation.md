# AWS Infrastructure Explanation

## Diagram Components
1. **Amazon EKS Cluster**
   - Managed Kubernetes control plane
   - Worker nodes in Auto Scaling Groups across 3 AZs
2. **Application Load Balancer (ALB)**
   - Routes external traffic to EKS nodes
   - SSL termination with ACM certificates
3. **Amazon RDS PostgreSQL**
   - Multi-AZ deployment for high availability
   - Automated backups and read replicas
4. **VPC Architecture**
   - Public subnets for ALB and NAT gateways
   - Private subnets for EKS worker nodes and RDS
5. **Auto Scaling**
   - Cluster Autoscaler for EKS nodes
   - Horizontal Pod Autoscaler for application
6. **Monitoring & Logging**
   - CloudWatch for metrics and alarms
   - CloudTrail for API monitoring
7. **Security**
   - IAM roles for service accounts
   - Security Groups for network isolation
   - Secrets Manager for credentials

## Implementation Steps
1. Set up VPC with public/private subnets
2. Create EKS cluster with managed node groups
3. Deploy RDS PostgreSQL with Multi-AZ
4. Configure ALB Ingress Controller
5. Set up CloudWatch logging and monitoring
6. Implement CI/CD pipeline using CodePipeline/ArgoCD
7. Configure IAM roles for Kubernetes service accounts
