# =============================================================================
# TERRAFORM - AWS Free Tier Infrastructure for Restaurant Recommender
# Architecture: EC2 t2.micro + Docker Compose (Free Tier Compatible)
# =============================================================================

terraform {
  required_version = ">= 1.0.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Optional: S3 backend for state
  # backend "s3" {
  #   bucket = "your-terraform-state-bucket"
  #   key    = "restaurant-recommender/terraform.tfstate"
  #   region = "us-east-1"
  # }
}

# =============================================================================
# VARIABLES
# =============================================================================

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"  # Ohio - tu región actual
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "restaurant-recommender"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "instance_type" {
  description = "EC2 instance type (t3.micro for Free Tier in us-east-2)"
  type        = string
  default     = "t3.micro"
}

variable "key_pair_name" {
  description = "Name of the SSH key pair"
  type        = string
  default     = "restaurant-recommender-key"
}

variable "allowed_ssh_cidr" {
  description = "CIDR block allowed for SSH access"
  type        = string
  default     = "0.0.0.0/0"  # Restrict in production
}

# =============================================================================
# PROVIDER
# =============================================================================

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# =============================================================================
# DATA SOURCES
# =============================================================================

# Get latest Amazon Linux 2023 AMI (Free Tier eligible)
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Get available AZs
data "aws_availability_zones" "available" {
  state = "available"
}

# =============================================================================
# NETWORKING (VPC - Free)
# =============================================================================

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Public Subnet (only public - no NAT Gateway to save costs)
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.project_name}-igw"
  }
}

# Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

# Route Table Association
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# =============================================================================
# SECURITY GROUPS
# =============================================================================

resource "aws_security_group" "app" {
  name        = "${var.project_name}-app-sg"
  description = "Security group for application server"
  vpc_id      = aws_vpc.main.id
  
  # SSH access
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }
  
  # HTTP access (Frontend)
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # HTTPS access
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # Backend API
  ingress {
    description = "Backend API"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # MLflow UI (optional - restrict in production)
  ingress {
    description = "MLflow"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }
  
  # Outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-app-sg"
  }
}

# =============================================================================
# IAM ROLE FOR EC2 (ECR Access)
# =============================================================================

resource "aws_iam_role" "ec2_role" {
  name = "${var.project_name}-ec2-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Policy for ECR access
resource "aws_iam_role_policy" "ecr_policy" {
  name = "${var.project_name}-ecr-policy"
  role = aws_iam_role.ec2_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:DescribeRepositories",
          "ecr:ListImages"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2_role.name
}

# =============================================================================
# EC2 INSTANCE (t2.micro - Free Tier)
# =============================================================================

resource "aws_instance" "app" {
  ami                    = data.aws_ami.amazon_linux_2023.id
  instance_type          = var.instance_type
  key_name               = var.key_pair_name
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.app.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  
  # Free Tier: 30 GB EBS storage
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 30
    delete_on_termination = true
    encrypted             = true
  }
  
  # User data script to install Docker
  user_data = base64encode(<<-EOF
    #!/bin/bash
    set -e
    
    # Update system
    dnf update -y
    
    # Install Docker
    dnf install -y docker
    systemctl start docker
    systemctl enable docker
    
    # Install Docker Compose
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    # Add ec2-user to docker group
    usermod -aG docker ec2-user
    
    # Install Git
    dnf install -y git
    
    # Create app directory
    mkdir -p /home/ec2-user/app
    chown ec2-user:ec2-user /home/ec2-user/app
    
    # Configure Docker to start on boot
    systemctl enable docker
    
    # Configure AWS CLI for ECR login
    cat > /home/ec2-user/deploy.sh << 'DEPLOY'
    #!/bin/bash
    set -e
    
    AWS_REGION="us-east-2"
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
    
    # Login to ECR
    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
    
    # Navigate to app directory
    cd /home/ec2-user/app
    
    # Pull latest images
    docker-compose pull
    
    # Restart services
    docker-compose down
    docker-compose up -d
    
    # Cleanup old images
    docker image prune -f
    
    echo "Deployment complete!"
    DEPLOY
    
    chmod +x /home/ec2-user/deploy.sh
    chown ec2-user:ec2-user /home/ec2-user/deploy.sh
    
    echo "EC2 instance setup complete!"
  EOF
  )
  
  tags = {
    Name = "${var.project_name}-app-server"
  }
}

# =============================================================================
# ELASTIC IP (Free Tier: 1 EIP associated with running instance)
# =============================================================================

resource "aws_eip" "app" {
  instance = aws_instance.app.id
  domain   = "vpc"
  
  tags = {
    Name = "${var.project_name}-eip"
  }
}

# =============================================================================
# ECR REPOSITORIES (Free Tier: 500 MB storage)
# =============================================================================

resource "aws_ecr_repository" "backend" {
  name                 = "${var.project_name}-backend"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
  
  # Lifecycle policy to keep costs down
  lifecycle {
    prevent_destroy = false
  }
  
  tags = {
    Name = "${var.project_name}-backend"
  }
}

resource "aws_ecr_repository" "frontend" {
  name                 = "${var.project_name}-frontend"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
  
  tags = {
    Name = "${var.project_name}-frontend"
  }
}

# ECR Lifecycle Policy - Keep only last 5 images to save storage
resource "aws_ecr_lifecycle_policy" "backend" {
  repository = aws_ecr_repository.backend.name
  
  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 5 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 5
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

resource "aws_ecr_lifecycle_policy" "frontend" {
  repository = aws_ecr_repository.frontend.name
  
  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 5 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 5
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# =============================================================================
# CLOUDWATCH (Free Tier: Basic monitoring)
# =============================================================================

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "${var.project_name}-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "CPU utilization is too high"
  
  dimensions = {
    InstanceId = aws_instance.app.id
  }
  
  tags = {
    Name = "${var.project_name}-cpu-alarm"
  }
}

# =============================================================================
# OUTPUTS
# =============================================================================

output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_eip.app.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of the EC2 instance"
  value       = aws_instance.app.public_dns
}

output "frontend_url" {
  description = "Frontend URL"
  value       = "http://${aws_eip.app.public_ip}"
}

output "backend_url" {
  description = "Backend API URL"
  value       = "http://${aws_eip.app.public_ip}:8000"
}

output "ecr_backend_url" {
  description = "ECR repository URL for backend"
  value       = aws_ecr_repository.backend.repository_url
}

output "ecr_frontend_url" {
  description = "ECR repository URL for frontend"
  value       = aws_ecr_repository.frontend.repository_url
}

output "ssh_command" {
  description = "SSH command to connect to EC2"
  value       = "ssh -i ${var.key_pair_name}.pem ec2-user@${aws_eip.app.public_ip}"
}

output "deploy_command" {
  description = "Command to trigger deployment on EC2"
  value       = "ssh -i ${var.key_pair_name}.pem ec2-user@${aws_eip.app.public_ip} '/home/ec2-user/deploy.sh'"
}

# =============================================================================
# FREE TIER COST SUMMARY:
# -----------------------------------------------------------------------------
# Resource              | Free Tier Allowance      | Expected Cost
# -----------------------------------------------------------------------------
# EC2 t2.micro         | 750 hours/month          | $0 (within limit)
# EBS gp3 30GB         | 30 GB/month              | $0 (within limit)
# Elastic IP           | 1 EIP (when associated)  | $0 (associated)
# ECR                  | 500 MB storage           | $0 (within limit)
# CloudWatch           | Basic monitoring FREE    | $0
# VPC/Subnet/IGW       | Always FREE              | $0
# Data Transfer        | 100 GB/month outbound    | $0 (within limit)
# -----------------------------------------------------------------------------
# ESTIMATED MONTHLY COST: $0 (within Free Tier limits)
# =============================================================================
