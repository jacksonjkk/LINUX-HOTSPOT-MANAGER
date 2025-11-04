#!/bin/bash
# Build script for Hotspot Manager

echo "Building Hotspot Manager package..."

# Build the .deb package
dpkg-deb --build hotspot-manager-package

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "Package built successfully: hotspot-manager-package.deb"
    echo ""
    echo "To install, run:"
    echo "sudo dpkg -i hotspot-manager-package.deb"
    echo "sudo apt-get install -f  # If there are dependency issues"
else
    echo "Package build failed!"
    exit 1
fi