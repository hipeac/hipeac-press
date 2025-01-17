FROM node:22-bookworm-slim

# Install dependencies from apt
RUN apt-get update && \
  apt-get install -y build-essential libpq-dev python3 python3-pip python3-poetry nginx && \
  rm -rf /var/lib/apt/lists/*

# Set up work directory
WORKDIR /app

# Copy project files
COPY poetry.lock pyproject.toml package*.json ./

# Install Python and Node.js dependencies
RUN poetry config virtualenvs.create false && \
  poetry install --no-root --no-interaction --no-ansi --without dev
RUN npm install -g yarn --force && yarn

# Copy the rest of the application
COPY . .

# Ensure the mounted directory is available
VOLUME ["/app/storage"]

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80
