using Microsoft.Azure.Cosmos;
using MudBlazor.Services;
using AzureBillingApp.Services;
using System;
using System.IO;

var builder = WebApplication.CreateBuilder(args);

// Add MudBlazor services
builder.Services.AddMudServices();

// Load environment variables from 'env' file
var envPath = Path.Combine(Directory.GetCurrentDirectory(), "env");
if (File.Exists(envPath))
{
    var envLines = File.ReadAllLines(envPath);
    foreach (var line in envLines)
    {
        var parts = line.Split('=', 2);
        if (parts.Length == 2)
            Environment.SetEnvironmentVariable(parts[0], parts[1]);
    }
}

// Configure Cosmos DB settings
var cosmosSettings = new CosmosDbSettings
{
    EndpointUrl = Environment.GetEnvironmentVariable("COSMOS_DB_URL"),
    PrimaryKey = Environment.GetEnvironmentVariable("COSMOS_DB_KEY"),
    DatabaseName = Environment.GetEnvironmentVariable("COSMOS_DB_NAME"),
    ContainerResources = Environment.GetEnvironmentVariable("COSMOS_DB_CONTAINER_RESOURCES"),
    ContainerUserSubscriptions = Environment.GetEnvironmentVariable("COSMOS_DB_CONTAINER_USER_SUBSCRIPTIONS")
};

builder.Services.AddSingleton(cosmosSettings);
builder.Services.AddSingleton<CosmosDbService>();

builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();

var app = builder.Build();

app.UseStaticFiles();
app.UseRouting();
app.MapBlazorHub();
app.MapFallbackToPage("/_Host");

app.Run();
