# Stage 1: Base runtime image
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

# Stage 2: Build and publish the app
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copy only the project file and restore dependencies
COPY ["AzureBillingApp/AzureBillingApp.csproj", "AzureBillingApp/"]
RUN dotnet restore "AzureBillingApp/AzureBillingApp.csproj"

# Copy the remaining source code and build the project
COPY . .
WORKDIR "/src/AzureBillingApp"
RUN dotnet build "AzureBillingApp.csproj" -c Release -o /app/build

# Publish the app
FROM build AS publish
RUN dotnet publish "AzureBillingApp.csproj" -c Release -o /app/publish

# Stage 3: Final image
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "AzureBillingApp.dll"]
