# Use the latest LTS version of Node.js
FROM node:18 AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json first (optimizes caching)
COPY package.json package-lock.json ./

# Ensure all dependencies are installed properly
RUN npm install

# Copy the rest of the application code
COPY . .

# Ensure react-scripts is globally available
RUN npm install -g react-scripts

# Build the React app
RUN npm run build

# Use Nginx to serve the frontend
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html

# Expose the default Nginx port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
