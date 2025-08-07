# Stage 1: Build the Flutter web app
FROM ghcr.io/cirruslabs/flutter:latest AS build-stage

# Create a non-root user
RUN useradd -m flutter

# IMPORTANT FIX: Change ownership of the Flutter SDK directory to the new 'flutter' user.
# This ensures the 'flutter' user has the necessary write permissions for the SDK's cache
# and other internal files, preventing 'Permission denied' errors during build operations.
RUN chown -R flutter:flutter /sdks/flutter

USER flutter
WORKDIR /home/flutter/app

# Fix for Git ownership issue: Add /sdks/flutter to safe directories
# This is necessary because the Flutter SDK might be owned by root or another user
# in the base image, and Git's security features prevent operations by a different owner.
RUN git config --global --add safe.directory /sdks/flutter

# Copy pubspec files
COPY --chown=flutter:flutter pubspec.yaml pubspec.lock ./

# Get dependencies
RUN flutter pub get

# Copy the rest of the application
COPY --chown=flutter:flutter . .

# Build for web
RUN flutter build web --release

# Stage 2: Serve the app with nginx
FROM nginx:alpine

# Copy the built web app from the build stage
COPY --from=build-stage /home/flutter/app/build/web /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]