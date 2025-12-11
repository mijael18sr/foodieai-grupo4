# =====================================================
# AWS Deployment Guide
# =====================================================

# Restaurant Recommender - AWS Deployment Guide

Complete guide for deploying the Restaurant Recommender system to AWS.

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **Docker** installed locally
4. **Terraform** >= 1.0 (for infrastructure)
5. **GitHub repository** with secrets configured

## Architecture

```
Internet
    │
    ▼
┌─────────────────┐
│   Route 53      │  (Optional: Custom domain)
│   (DNS)         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Application    │
│  Load Balancer  │
│  (ALB)          │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│Backend│ │Frontend│
│(ECS)  │ │(ECS)   │
│Fargate│ │Fargate │
└───┬───┘ └───────┘
    │
    ▼
┌───────┐
│ ECR   │  (Container Registry)
└───────┘
```

## Step 1: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

| Secret Name | Description |
|-------------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `PRODUCTION_API_URL` | Production API URL (e.g., `https://api.yourapp.com`) |

## Step 2: Create AWS Infrastructure

### Option A: Using Terraform (Recommended)

```bash
# Navigate to infrastructure directory
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Review the plan
terraform plan -out=tfplan

# Apply infrastructure
terraform apply tfplan

# Get the outputs
terraform output
```

### Option B: Using AWS Console

1. **Create ECR Repositories**
   - Navigate to ECR in AWS Console
   - Create `restaurant-recommender-backend`
   - Create `restaurant-recommender-frontend`

2. **Create ECS Cluster**
   - Navigate to ECS
   - Create cluster: `restaurant-recommender-cluster`
   - Select Fargate as capacity provider

3. **Create VPC and Networking**
   - Create VPC with CIDR 10.0.0.0/16
   - Create public subnets in 2 AZs
   - Create Internet Gateway
   - Configure route tables

4. **Create Application Load Balancer**
   - Create ALB in public subnets
   - Configure listeners (HTTP:80)
   - Create target groups for backend and frontend

## Step 3: Push Docker Images

### First-time setup:

```bash
# Get ECR login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
cd backend
docker build -t restaurant-backend .
docker tag restaurant-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/restaurant-recommender-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/restaurant-recommender-backend:latest

# Build and push frontend
cd ../frontend
docker build --build-arg VITE_API_BASE_URL=https://your-alb-url.amazonaws.com -t restaurant-frontend .
docker tag restaurant-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/restaurant-recommender-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/restaurant-recommender-frontend:latest
```

## Step 4: Configure ECS Services

### Backend Task Definition

```json
{
  "family": "restaurant-backend-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [{
    "name": "backend",
    "image": "<ecr-url>/restaurant-recommender-backend:latest",
    "portMappings": [{
      "containerPort": 8000,
      "protocol": "tcp"
    }],
    "environment": [
      {"name": "ENVIRONMENT", "value": "production"},
      {"name": "DEBUG", "value": "false"}
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/restaurant-backend",
        "awslogs-region": "us-east-1",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }]
}
```

## Step 5: Automatic Deployment

Once everything is configured, the CI/CD pipeline will automatically:

1. **On Pull Request:**
   - Run tests (backend + frontend)
   - Build Docker images (validation only)

2. **On Push to main:**
   - Run tests
   - Build and push Docker images to ECR
   - Update ECS task definitions
   - Deploy to ECS services

## Monitoring

### CloudWatch Logs

View logs in AWS Console:
- Backend: `/ecs/restaurant-recommender/backend`
- Frontend: `/ecs/restaurant-recommender/frontend`

### Health Checks

- Backend: `http://<alb-url>/health`
- Frontend: `http://<alb-url>/`
- API Docs: `http://<alb-url>/docs`

## Cost Optimization

### Development/Testing
- Use Fargate Spot for non-production
- Scale down to 0 during non-business hours

### Production
- Use reserved capacity for consistent workloads
- Enable auto-scaling based on CPU/memory

## Troubleshooting

### Common Issues

1. **ECS Task fails to start**
   - Check CloudWatch logs
   - Verify ECR image exists
   - Check task role permissions

2. **Health checks failing**
   - Verify security group rules
   - Check container port mappings
   - Ensure health endpoint returns 200

3. **Cannot pull image from ECR**
   - Verify task execution role has ECR permissions
   - Check ECR repository exists
   - Verify image tag

### Useful Commands

```bash
# View ECS service events
aws ecs describe-services --cluster restaurant-recommender-cluster --services restaurant-backend-service

# View running tasks
aws ecs list-tasks --cluster restaurant-recommender-cluster

# View task logs
aws logs tail /ecs/restaurant-recommender/backend --follow

# Force new deployment
aws ecs update-service --cluster restaurant-recommender-cluster --service restaurant-backend-service --force-new-deployment
```

## Security Best Practices

1. **Use IAM roles** instead of access keys where possible
2. **Enable ECR image scanning** for vulnerabilities
3. **Use Secrets Manager** for sensitive configuration
4. **Enable VPC Flow Logs** for network monitoring
5. **Configure WAF** for application protection

## Next Steps

1. Configure custom domain with Route 53
2. Add SSL/TLS certificate with ACM
3. Set up auto-scaling policies
4. Configure backup and disaster recovery
5. Implement blue/green deployments
