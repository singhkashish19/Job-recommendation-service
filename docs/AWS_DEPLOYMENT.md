# AWS Deployment Guide

This guide covers deploying the Job Recommendation Service to AWS.

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Docker installed locally
- Git repository with your code

## Architecture Overview

```
                    ┌─────────────────────┐
                    │  CloudFront CDN     │
                    │  (Optional - for    │
                    │   static assets)    │
                    └──────────┬──────────┘
                               │
                    ┌─────────────────────┐
                    │   Load Balancer     │
                    │   (ELB/ALB)         │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────▼──────┐      ┌─────▼──────┐      ┌─────▼──────┐
    │   ECS       │      │   ECS       │      │   ECS       │
    │   Container │      │   Container │      │   Container │
    │   (App)     │      │   (App)     │      │   (App)     │
    └─────┬──────┘      └─────┬──────┘      └─────┬──────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                    ┌─────────────────────┐
                    │   RDS PostgreSQL    │
                    │   (Multi-AZ)        │
                    └─────────────────────┘
```

## Deployment Options

### Option 1: ECS (Elastic Container Service) - Recommended

#### Step 1: Create ECR Repository

```bash
# Create ECR repository
aws ecr create-repository \
  --repository-name job-recommendation-service \
  --region us-east-1

# Get login token and login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Build and push image
docker build -t job-recommendation-service .
docker tag job-recommendation-service:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/job-recommendation-service:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/job-recommendation-service:latest
```

#### Step 2: Create RDS PostgreSQL Database

```bash
# Using AWS Console or CLI:
aws rds create-db-instance \
  --db-instance-identifier job-recommendation-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password <STRONG_PASSWORD> \
  --allocated-storage 20 \
  --publicly-accessible false \
  --vpc-security-group-ids sg-xxxxxxxx \
  --backup-retention-period 7 \
  --multi-az
```

#### Step 3: Create ECS Cluster and Task Definition

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name job-recommendation-cluster

# Register task definition (create task-definition.json first - see below)
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

**task-definition.json**:
```json
{
  "family": "job-recommendation-service",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "job-recommendation-service",
      "image": "<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/job-recommendation-service:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://postgres:password@job-recommendation-db.xxxxx.us-east-1.rds.amazonaws.com:5432/jobs_db"
        },
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:job-SECRET_KEY"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/job-recommendation-service",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole"
}
```

#### Step 4: Create Service

```bash
# Create ECS service
aws ecs create-service \
  --cluster job-recommendation-cluster \
  --service-name job-recommendation-service \
  --task-definition job-recommendation-service \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=DISABLED}" \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=job-recommendation-service,containerPort=8000
```

### Option 2: Elastic Beanstalk

```bash
# Initialize Elastic Beanstalk
eb init -p docker job-recommendation-service

# Create environment
eb create job-recommendation-prod

# Deploy
eb deploy
```

### Option 3: App Runner

```bash
# Deploy using App Runner
aws apprunner create-service \
  --service-name job-recommendation-service \
  --source-configuration RepositoryType=ECR,ImageRepository={ImageIdentifier=<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/job-recommendation-service:latest,RepositoryType=ECR}
```

## Environment Setup

### 1. Create Secrets in AWS Secrets Manager

```bash
# Store SECRET_KEY
aws secretsmanager create-secret \
  --name job-recommendation-SECRET_KEY \
  --secret-string "your-super-secret-key-here"

# Store DATABASE_URL
aws secretsmanager create-secret \
  --name job-recommendation-DATABASE_URL \
  --secret-string "postgresql://user:password@db-endpoint:5432/jobs_db"
```

### 2. Create CloudWatch Log Group

```bash
aws logs create-log-group --log-group-name /ecs/job-recommendation-service
```

### 3. Configure VPC Security Groups

```bash
# Allow RDS access from ECS
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxx \
  --protocol tcp \
  --port 5432 \
  --source-security-group-id sg-xxxxxxxx
```

## Configuration

### Database Migrations (First Time)

```bash
# Connect to RDS and run migrations
psql postgresql://user:password@endpoint:5432/jobs_db < migrations.sql

# Or use Alembic:
alembic upgrade head
```

### Load Mock Data

The application automatically loads jobs from `jobs_mock.json` at startup.

## Monitoring & Logging

### CloudWatch Monitoring

```bash
# Create custom metric for API latency
aws cloudwatch put-metric-alarm \
  --alarm-name job-recommendation-api-latency \
  --alarm-description "Alert when API latency is high" \
  --metric-name TargetResponseTime \
  --namespace AWS/ApplicationELB \
  --statistic Average \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold
```

### View Logs

```bash
# View logs from CloudWatch
aws logs tail /ecs/job-recommendation-service --follow

# Or in CloudWatch console
# Navigate to CloudWatch → Log Groups → /ecs/job-recommendation-service
```

## Auto Scaling

```bash
# Create scaling policies
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/job-recommendation-cluster/job-recommendation-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

# Create scaling policy
aws application-autoscaling put-scaling-policy \
  --policy-name cpu-scaling \
  --service-namespace ecs \
  --resource-id service/job-recommendation-cluster/job-recommendation-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

**scaling-policy.json**:
```json
{
  "TargetValue": 70.0,
  "PredefinedMetricSpecification": {
    "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
  },
  "ScaleOutCooldown": 60,
  "ScaleInCooldown": 300
}
```

## API Configuration for AWS

Update your frontend to use AWS endpoints:

```javascript
// Frontend configuration
const API_BASE_URL = "https://your-load-balancer-url.com";

// Or use API Gateway
const API_BASE_URL = "https://api-id.execute-api.us-east-1.amazonaws.com/prod";
```

## Cost Optimization

1. **RDS**: Use db.t3.micro for development, db.t3.small for production
2. **ECS**: Use Spot instances for non-critical tasks (save up to 70%)
3. **Network**: Use NAT Gateway for outbound traffic
4. **Storage**: Configure S3 lifecycle policies for logs

## Production Deployment Checklist

- [ ] Database backups configured
- [ ] SSL/TLS certificate installed (ACM)
- [ ] Load balancer health checks configured
- [ ] Auto-scaling policies in place
- [ ] CloudWatch alarms set up
- [ ] CloudTrail logging enabled
- [ ] VPC and security groups hardened
- [ ] Secrets managed in AWS Secrets Manager
- [ ] Application logging to CloudWatch
- [ ] Regular security updates scheduled
- [ ] Disaster recovery plan documented
- [ ] Load testing completed
- [ ] Performance baseline established
- [ ] Monitoring dashboards created

## Troubleshooting

### Container Fails to Start

```bash
# Check ECS task logs
aws ecs describe-tasks \
  --cluster job-recommendation-cluster \
  --tasks <task-arn>

# Check CloudWatch logs
aws logs tail /ecs/job-recommendation-service --follow
```

### Database Connection Issues

```bash
# Test database connectivity
psql -h <RDS-ENDPOINT> -U postgres -d jobs_db

# Check security group rules
aws ec2 describe-security-groups --group-ids sg-xxxxxxxx
```

### High Latency

```bash
# Check CloudWatch metrics
# Look for:
# - ECS CPU/Memory utilization
# - RDS CPU/Connections
# - ALB Target Health
# - Network performance
```

## Scaling Strategy

### Development
- 1 ECS task (t3.micro)
- db.t3.micro PostgreSQL
- Cost: ~$30-50/month

### Production
- 2-10 ECS tasks (auto-scaling)
- db.t3.small+ PostgreSQL (Multi-AZ)
- Load balancer + CloudFront
- Cost: ~$200-500+/month

## Next Steps

1. Deploy to ECS
2. Configure CloudFront for static assets
3. Set up RDS read replicas for scaling reads
4. Implement Redis caching layer
5. Configure AWS Lambda for scheduled tasks
6. Set up CI/CD with CodePipeline

## References

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker on AWS](https://aws.amazon.com/docker/)
