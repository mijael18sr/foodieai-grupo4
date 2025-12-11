# AWS Deployment Guide - Free Tier

Complete guide for deploying the Restaurant Recommender system to AWS using Free Tier resources.

## Architecture (Free Tier Optimized)

```
Internet
    │
    ▼
┌─────────────────┐
│   Elastic IP    │  (Free when associated)
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│       EC2 t2.micro (Free Tier)      │
│  ┌─────────────────────────────────┐│
│  │         Docker Compose          ││
│  │  ┌─────────┐    ┌─────────────┐ ││
│  │  │Frontend │    │   Backend   │ ││
│  │  │ (Nginx) │    │  (FastAPI)  │ ││
│  │  │  :80    │    │   :8000     │ ││
│  │  └─────────┘    └─────────────┘ ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│   ECR (500MB)   │  (Container Registry)
└─────────────────┘
```

## Free Tier Resources Used

| Resource | Free Tier Allowance | Usage |
|----------|---------------------|-------|
| EC2 t2.micro | 750 hours/month | Main server |
| EBS gp3 | 30 GB | Storage |
| Elastic IP | 1 (when associated) | Static IP |
| ECR | 500 MB | Docker images |
| Data Transfer | 100 GB outbound | Traffic |
| CloudWatch | Basic monitoring | Alerts |

**Estimated Monthly Cost: $0** (within Free Tier limits)

## Prerequisites

1. **AWS Account** (Free Tier eligible)
2. **AWS CLI** installed and configured
3. **Terraform** >= 1.0
4. **SSH Key Pair** for EC2 access

## Step 1: Configure AWS CLI

```bash
# Configure AWS credentials
aws configure
# Enter: AWS Access Key ID, Secret Access Key, Region (us-east-1)
```

## Step 2: Create SSH Key Pair

```bash
# Create key pair in AWS
aws ec2 create-key-pair \
  --key-name restaurant-recommender-key \
  --query 'KeyMaterial' \
  --output text > restaurant-recommender-key.pem

# Set permissions
chmod 400 restaurant-recommender-key.pem
```

## Step 3: Deploy Infrastructure with Terraform

```bash
# Navigate to infrastructure directory
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply infrastructure (type 'yes' to confirm)
terraform apply

# Save the outputs
terraform output > deployment-info.txt
```

### Terraform Outputs

After successful deployment, you'll see:
- `ec2_public_ip`: Your server IP address
- `frontend_url`: http://[IP]
- `backend_url`: http://[IP]:8000
- `ssh_command`: SSH command to connect

## Step 4: Configure GitHub Secrets

Go to GitHub → Repository → Settings → Secrets and variables → Actions

Add these secrets:

| Secret | Description | Example |
|--------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS access key | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | `wJal...` |
| `AWS_ACCOUNT_ID` | 12-digit account ID | `123456789012` |
| `EC2_SSH_PRIVATE_KEY` | Content of .pem file | `-----BEGIN RSA...` |
| `PRODUCTION_API_URL` | Backend URL | `http://[EC2_IP]:8000` |

### Getting Your AWS Account ID

```bash
aws sts get-caller-identity --query Account --output text
```

### Adding SSH Key to GitHub

```bash
# Copy the content of your key file
cat restaurant-recommender-key.pem
# Paste this entire content into EC2_SSH_PRIVATE_KEY secret
```

## Step 5: Initial Manual Deployment

For the first deployment, manually set up the EC2 instance:

```bash
# SSH into EC2
ssh -i restaurant-recommender-key.pem ec2-user@[EC2_IP]

# Create app directory
mkdir -p /home/ec2-user/app
cd /home/ec2-user/app

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  backend:
    image: ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/restaurant-recommender-backend:latest
    container_name: restaurant-backend
    restart: always
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=info
      - CORS_ORIGINS=*
    volumes:
      - backend-data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  frontend:
    image: ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/restaurant-recommender-frontend:latest
    container_name: restaurant-frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  backend-data:
EOF

# Create .env file
echo "AWS_ACCOUNT_ID=[YOUR_ACCOUNT_ID]" > .env

# Login to ECR (first time)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com

# Pull and start
docker-compose pull
docker-compose up -d
```

## Step 6: Automatic Deployments (CI/CD)

After the initial setup, every push to `main` branch will:

1. Run tests (backend + frontend)
2. Build Docker images
3. Push to ECR
4. SSH into EC2 and deploy

### Manually Trigger Deployment

```bash
# From your local machine
git push origin main
# The GitHub Action will automatically deploy
```

### Manual Deployment Script (on EC2)

```bash
# SSH into EC2
ssh -i restaurant-recommender-key.pem ec2-user@[EC2_IP]

# Run deploy script
cd /home/ec2-user/app
./deploy.sh
```

## Monitoring & Management

### View Container Logs

```bash
# SSH into EC2
ssh -i restaurant-recommender-key.pem ec2-user@[EC2_IP]

# View all logs
docker-compose logs

# View specific service
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Check Container Status

```bash
docker-compose ps
docker stats
```

### Update Application

```bash
# Pull latest images
docker-compose pull

# Restart with new images
docker-compose down
docker-compose up -d
```

## Troubleshooting

### Cannot SSH into EC2

```bash
# Check security group allows SSH (port 22)
aws ec2 describe-security-groups --group-names restaurant-recommender-app-sg

# Check instance is running
aws ec2 describe-instances --filters "Name=tag:Name,Values=restaurant-recommender-app-server"
```

### Docker Not Working

```bash
# Check Docker service
sudo systemctl status docker

# Restart Docker
sudo systemctl restart docker

# Check Docker permissions
sudo usermod -aG docker ec2-user
# Log out and log back in
```

### ECR Login Issues

```bash
# Manual ECR login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com
```

### Out of Disk Space

```bash
# Check disk usage
df -h

# Clean Docker resources
docker system prune -a
```

## Cost Optimization Tips

1. **Stop EC2 when not in use**: If for development only
   ```bash
   aws ec2 stop-instances --instance-ids [INSTANCE_ID]
   ```

2. **Keep ECR images minimal**: Lifecycle policy keeps only 5 images

3. **Monitor usage**: Check AWS Cost Explorer weekly

4. **Stay within Free Tier**:
   - EC2: Don't run more than 750 hours/month
   - EBS: Keep storage under 30 GB
   - Data transfer: Under 100 GB outbound

## Destroy Infrastructure

When you no longer need the infrastructure:

```bash
cd infrastructure/terraform
terraform destroy
```

**Warning**: This will delete all resources including data!

## Security Best Practices

1. **Restrict SSH access**: Update `allowed_ssh_cidr` variable
2. **Use HTTPS**: Add SSL certificate (beyond Free Tier)
3. **Rotate credentials**: Update AWS keys periodically
4. **Enable MFA**: On AWS account

## Next Steps (Beyond Free Tier)

When ready to scale:

1. **Add HTTPS**: Use AWS Certificate Manager + ALB
2. **Custom Domain**: Configure Route 53
3. **Auto Scaling**: Move to ECS Fargate
4. **Database**: Add RDS for persistent data
5. **CDN**: Add CloudFront for frontend

## Quick Reference

```bash
# SSH into server
ssh -i restaurant-recommender-key.pem ec2-user@[EC2_IP]

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Manual deploy
docker-compose pull && docker-compose up -d

# Check status
docker-compose ps
```

## Support

For issues:
1. Check container logs
2. Verify GitHub Action logs
3. Check AWS CloudWatch
4. Open GitHub issue
