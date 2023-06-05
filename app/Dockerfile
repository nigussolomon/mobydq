FROM node:14.2.0-alpine3.11

# Project files
ARG PROJECT_DIR=/srv/app
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

# Copy both 'package.json' and 'package-lock.json' (if available)
COPY ./init/package*.json ./

# Install http-server to serve files to Nginx for production
RUN npm install -g http-server

# Install Vue CLI
RUN npm install -g @vue/cli

# Install project dependencies
RUN npm install

# Copy project files and folders to the current working directory
COPY ./entrypoint.sh ./
COPY ./init/ ./

# Use entrypoint to differentiate build process between dev and prod
RUN chmod +x entrypoint.sh
RUN export NODE_ENV=production

    # Minify Javascript files and create distribution folder (dist)
RUN npm run build

    # Move files to app root folder
RUN cp -a ./dist/. ./

    # Delete all unnecessary files
RUN rm -rf ./dist
RUN rm -rf ./node_modules
RUN rm -rf ./public
RUN rm -rf ./src

ENTRYPOINT [ "http-server", "." ]