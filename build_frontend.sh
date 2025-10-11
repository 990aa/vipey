#!/bin/bash
# Build script for Vipey frontend

set -e

echo "🔨 Building Vipey Frontend..."

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build the frontend
echo "🎨 Building React app..."
npm run build

# Copy to templates
echo "📋 Copying assets to Python templates..."
cd ..
cp -r frontend/dist/* vipey/templates/

echo "✅ Build complete! Frontend assets copied to vipey/templates/"
