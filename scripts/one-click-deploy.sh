#!/bin/bash
# One-Click Deploy Script for GCM Prototype

set -e

echo "🔧 Governable Capability Monitor - One-Click Deploy"
echo "======================================================"

# Check prerequisites
command -v aws >/dev/null 2>&1 || { echo "❌ AWS CLI required. Install: https://docs.aws.amazon.com/cli/"; exit 1; }
command -v sam >/dev/null 2>&1 || { echo "❌ SAM CLI required. Install: https://docs.aws.amazon.com/serverless-application-model/"; exit 1; }

# Check AWS credentials
aws sts get-caller-identity >/dev/null 2>&1 || { echo "❌ AWS credentials not configured. Run: aws configure"; exit 1; }

echo "✅ Prerequisites met"

# Get region
AWS_REGION=$(aws configure get region)
echo "📍 Region: $AWS_REGION"

# Get environment
read -p "Environment (dev/staging/prod) [dev]: " ENV
ENV=${ENV:-dev}

# Confirm
echo ""
echo "Deploying GCM with:"
echo "  Region: $AWS_REGION"
echo "  Environment: $ENV"
echo "  Stack: gcm-prototype-$ENV"
read -p "Continue? (y/n): " CONFIRM

if [[ $CONFIRM != "y" ]]; then
    echo "Cancelled."
    exit 0
fi

# Build and deploy
echo ""
echo "🔨 Building..."
cd "$(dirname "$0")/../backend"
sam build

echo ""
echo "🚀 Deploying..."
sam deploy \
    --guided \
    --stack-name "gcm-prototype-$ENV" \
    --parameter-overrides "Environment=$ENV" \
    --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND

# Get outputs
echo ""
echo "📋 Deployment complete!"
echo ""
WEBSOCKET_URL=$(aws cloudformation describe-stacks \
    --stack-name "gcm-prototype-$ENV" \
    --query 'Stacks[0].Outputs[?OutputKey==`WebSocketEndpoint`].OutputValue' \
    --output text 2>/dev/null || echo "Not available yet")

if [ "$WEBSOCKET_URL" != "None" ] && [ -n "$WEBSOCKET_URL" ]; then
    echo "WebSocket URL: $WEBSOCKET_URL"
    echo ""
    echo "Dashboard setup:"
    echo "  cd ../dashboard"
    echo "  REACT_APP_WEBSOCKET_URL=$WEBSOCKET_URL npm start"
fi

echo ""
echo "✅ GCM is live!"
