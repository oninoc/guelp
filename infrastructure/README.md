# Infrastructure Documentation

This directory contains Terraform configurations for provisioning AWS infrastructure for the full-stack application.

## Architecture Overview

The infrastructure is deployed on AWS and consists of the following components:

### Core Components

- **Frontend**: React application served via CloudFront CDN from S3
- **Backend API**: FastAPI application running on AWS App Runner
- **Database**: Aurora PostgreSQL cluster
- **CI/CD**: Repository Actions for automated deployments
- **Container Registry**: ECR for Docker images
- **Secrets Management**: AWS Secrets Manager for credentials

## Infrastructure Diagram

```mermaid
graph TB
    subgraph "Users & Developers"
        Users[Users]
        Developers[Developers]
    end

    subgraph "Frontend Layer"
        CloudFront[CloudFront CDN<br/>Global Content Delivery]
        S3[S3 Bucket<br/>Static Files Storage]
    end

    subgraph "Backend Layer"
        AppRunner[App Runner<br/>Backend API Server<br/>FastAPI Application]
    end

    subgraph "Database Layer"
        Aurora[Aurora PostgreSQL<br/>Database Cluster]
    end

    subgraph "DevOps & Deployment"
        CICD[CI/CD]
        ECR[ECR Container Registry<br/>Docker Images]
        ECS[ECS Fargate<br/>Database Migrations]
    end

    subgraph "Supporting Services"
        Secrets[Secrets Manager<br/>Database Credentials]
        Logs[CloudWatch<br/>Application Logs]
    end

    %% User flow
    Users -->|HTTPS Request| CloudFront
    CloudFront -->|Serves Files| Users
    CloudFront -->|Fetches from| S3
    
    %% Application flow
    Users -->|API Calls| AppRunner
    AppRunner -->|Reads Credentials| Secrets
    AppRunner -->|Queries Data| Aurora
    
    %% Deployment flow
    Developers -->|Push Code| CICD
    CICD -->|Builds & Deploys| S3
    CICD -->|Builds Docker Images| ECR
    CICD -->|Deploys Backend| AppRunner
    CICD -->|Runs Migrations| ECS
    ECR -->|Provides Images| AppRunner
    ECR -->|Provides Images| ECS
    ECS -->|Reads Credentials| Secrets
    ECS -->|Updates Schema| Aurora
    ECS -->|Writes Logs| Logs

    %% Styling
    classDef frontend fill:#4a90e2,stroke:#2c5282,color:#fff,stroke-width:2px
    classDef backend fill:#48bb78,stroke:#2f855a,color:#fff,stroke-width:2px
    classDef database fill:#ed8936,stroke:#c05621,color:#fff,stroke-width:2px
    classDef devops fill:#9f7aea,stroke:#6b46c1,color:#fff,stroke-width:2px
    classDef support fill:#f56565,stroke:#c53030,color:#fff,stroke-width:2px
    classDef users fill:#cbd5e0,stroke:#718096,color:#000,stroke-width:2px

    class CloudFront,S3 frontend
    class AppRunner backend
    class Aurora database
    class CICD,ECR,ECS devops
    class Secrets,Logs support
    class Users,Developers users
```

### Simple Overview (For Developers & Project Managers)

**How it works:**

1. **Users** access the application through a CDN (CloudFront) which serves static files from S3
2. **Frontend** (React app) makes API calls to the **Backend** (FastAPI running on App Runner)
3. **Backend** connects to the **Database** (Aurora PostgreSQL) to fetch/store data
4. **Developers** push code to Repository, which automatically:
   - Builds and deploys the frontend to S3
   - Builds Docker images and deploys the backend
   - Runs database migrations when needed

**Key Components:**
- **CloudFront + S3**: Frontend hosting and global content delivery
- **App Runner**: Backend API server (auto-scales, no server management)
- **Aurora PostgreSQL**: Managed database (automatic backups, high availability)
- **Repository Actions**: Automated deployment pipeline
- **ECR**: Docker image storage
- **ECS**: Runs database migrations automatically


## Usage

### Initialize Terraform
```bash
make init
```

### Plan Changes
```bash
make plan
```

### Apply Changes
```bash
make apply
```

### Deploy Only ECR Repositories
```bash
make apply-ecr
```

### Destroy Infrastructure
```bash
make destroy
```

### Unlock State (if locked)
```bash
make unlock LOCK_ID=<lock-id>
```

## Troubleshooting

- **State Lock Error**: Use `make unlock LOCK_ID=<id>` to release lock
- **Migration Task Fails**: Check CloudWatch Logs for ECS task details
- **Frontend Not Updating**: Verify CloudFront cache invalidation completed
