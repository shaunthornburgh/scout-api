# AWS Deployment Guide (App Runner + RDS)

This guide deploys the Scout API to AWS App Runner with an RDS PostgreSQL database.  
Pushing to the `main` branch on GitHub automatically builds and deploys a new version.

## 1. Create an RDS PostgreSQL database

1. Go to **RDS → Create database**.
2. Choose **PostgreSQL**, template **Free tier** (or Production).
3. Settings:
   - DB instance identifier: `scout-api-db`
   - Master username: `scout`
   - Master password: generate a strong one
   - Initial database name: `scout`
4. Instance: `db.t4g.micro`
5. Storage: default
6. Connectivity:
   - VPC: default
   - Public access: **No** (recommended)
   - Create a new security group (or use existing)
7. Create the database and note the **endpoint** (e.g. `scout-api-db.xxxx.eu-west-2.rds.amazonaws.com`).

## 2. Create an ECR repository

```bash
aws ecr create-repository --repository-name scout-api --region eu-west-2
```

## 3. Create an App Runner service

1. Go to **App Runner → Create service**.
2. Source: **Container registry** → Amazon ECR.
3. Select the `scout-api` repository and the `latest` image (you can push a first image manually or let the first GitHub Action do it).
4. Deployment: **Automatic** (or Manual if you prefer the workflow to trigger it).
5. Service settings:
   - Service name: `scout-api`
   - Port: `8000`
6. Environment variables (or use Secrets Manager):
   - `DATABASE_URL` = `postgresql+asyncpg://scout:<password>@<rds-endpoint>:5432/scout`
   - `API_KEY` = a long random string
   - `DB_HOST` = the RDS endpoint hostname
   - `DB_USER` = `scout`
   - `DB_NAME` = `scout`
   - `ENV` = `production`
7. Networking: connect the App Runner VPC connector to the same VPC as the RDS instance and allow the security group to reach port 5432 on the RDS security group.
8. Create the service and note the **Service ARN**.

## 4. GitHub repository secrets

In your GitHub repo → **Settings → Secrets and variables → Actions**, add:

- `AWS_ROLE_ARN` — IAM role ARN that GitHub Actions can assume (with permissions for ECR and App Runner)
- `APP_RUNNER_SERVICE_ARN` — the App Runner service ARN from step 3

## 5. IAM role for GitHub Actions (OIDC)

Create an IAM role with a trust policy for GitHub OIDC, and attach permissions for:
- `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:PutImage`, etc.
- `apprunner:StartDeployment`

(See AWS docs for the exact GitHub OIDC trust policy.)

## 6. First deploy

Push the code to the `main` branch. The workflow will build the image, push it to ECR, and trigger an App Runner deployment.

After the first successful deploy, the API will be available at the App Runner URL (HTTPS).

## Local vs production

- Local: `docker compose up --build` (uses the `db` service)
- Production: App Runner uses the environment variables above to reach RDS

## Security notes

- Keep the RDS instance private.
- Store the real `API_KEY` and database password in AWS Secrets Manager and reference them from App Runner.
- Restrict the App Runner security group so only the App Runner service can reach the database.
