# AWS Terraform Infrastructure

# Restaurant Recommender - AWS Infrastructure

Infrastructure as Code (IaC) using Terraform for deploying the Restaurant Recommender system to AWS.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                           AWS Cloud                                  │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                         VPC (10.0.0.0/16)                      │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │              Application Load Balancer                   │  │  │
│  │  │                    (Port 80/443)                         │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                    │                    │                      │  │
│  │         ┌──────────┴──────────┐         │                      │  │
│  │         │                     │         │                      │  │
│  │  ┌──────▼──────┐       ┌──────▼──────┐                        │  │
│  │  │  Frontend   │       │   Backend   │                        │  │
│  │  │  (Fargate)  │       │  (Fargate)  │                        │  │
│  │  │  Port: 80   │       │  Port: 8000 │                        │  │
│  │  └─────────────┘       └─────────────┘                        │  │
│  │         │                     │                                │  │
│  │  ┌──────▼──────┐       ┌──────▼──────┐                        │  │
│  │  │     ECR     │       │     ECR     │                        │  │
│  │  │  Frontend   │       │   Backend   │                        │  │
│  │  └─────────────┘       └─────────────┘                        │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

1. **AWS CLI** configured with appropriate credentials
2. **Terraform** >= 1.0 installed
3. **Docker** for building images locally

## Quick Start

### 1. Initialize Terraform

```bash
cd infrastructure/terraform
terraform init
```

### 2. Review the plan

```bash
terraform plan -out=tfplan
```

### 3. Apply the infrastructure

```bash
terraform apply tfplan
```

### 4. Get outputs

```bash
terraform output
```

## Resources Created

| Resource | Description |
|----------|-------------|
| VPC | Virtual Private Cloud with public/private subnets |
| ECS Cluster | Fargate cluster for running containers |
| ECR | Container registries for backend and frontend |
| ALB | Application Load Balancer for traffic routing |
| CloudWatch | Log groups for container logs |
| IAM Roles | Execution and task roles for ECS |
| Security Groups | Network security rules |

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `aws_region` | AWS region | us-east-1 |
| `environment` | Environment name | production |
| `backend_cpu` | Backend CPU units | 512 |
| `backend_memory` | Backend memory (MB) | 1024 |
| `frontend_cpu` | Frontend CPU units | 256 |
| `frontend_memory` | Frontend memory (MB) | 512 |

## Custom Configuration

Create a `terraform.tfvars` file:

```hcl
aws_region     = "us-east-1"
environment    = "production"
backend_cpu    = 1024
backend_memory = 2048
```

## Estimated Costs

Using AWS Fargate with minimum configuration:

| Service | Estimated Monthly Cost |
|---------|----------------------|
| Fargate (2 tasks) | ~$30-50 |
| ALB | ~$20 |
| ECR | ~$1 |
| CloudWatch | ~$5 |
| **Total** | **~$60-80/month** |

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

## Security Considerations

- All containers run as non-root users
- Security groups restrict traffic to necessary ports
- ECR images are scanned for vulnerabilities
- CloudWatch logs for audit trails
