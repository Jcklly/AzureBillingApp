using Microsoft.Azure.Cosmos;
using System;
using System.Threading.Tasks;

namespace AzureBillingApp.Services
{
    public class CosmosDbService
    {
        private readonly CosmosClient _cosmosClient;
        private readonly string _databaseName;
        private readonly string _containerName;

        public CosmosDbService(CosmosDbSettings settings)
        {
            _cosmosClient = new CosmosClient(settings.EndpointUrl, settings.PrimaryKey);
            _databaseName = settings.DatabaseName!;
            _containerName = settings.ContainerResources!;
        }

        public async Task<bool> TestConnectionAsync()
        {
            try
            {
                var database = _cosmosClient.GetDatabase(_databaseName);
                var container = database.GetContainer(_containerName);
                await container.ReadContainerAsync();
                Console.WriteLine("✅ Successfully connected to Cosmos DB!");
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Failed to connect to Cosmos DB: {ex.Message}");
                return false;
            }
        }
    }
}
