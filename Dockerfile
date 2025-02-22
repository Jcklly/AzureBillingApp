# Use the .NET SDK for development (to support hot reload)
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS base
WORKDIR /app
VOLUME /app-keys

# Install Node.js (required for Blazor hot reload)
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Expose the application port
EXPOSE 8080

# Copy project files
COPY ["AzureBillingApp.csproj", "."]
RUN dotnet restore "AzureBillingApp.csproj"

# Copy everything else and build
COPY . .
RUN dotnet build "AzureBillingApp.csproj" -c Debug -o /app/build

# Set the entrypoint for hot reload (dotnet watch run)
CMD ["dotnet", "watch", "run", "--no-launch-profile", "--urls", "http://0.0.0.0:8080"]
