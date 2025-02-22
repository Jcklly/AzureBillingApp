namespace AzureBillingApp.Services
{
    public class CosmosDbSettings
    {
        public string? EndpointUrl { get; set; }
        public string? PrimaryKey { get; set; }
        public string? DatabaseName { get; set; }
        public string? ContainerResources { get; set; }
        public string? ContainerUserSubscriptions { get; set; }
    }
}
