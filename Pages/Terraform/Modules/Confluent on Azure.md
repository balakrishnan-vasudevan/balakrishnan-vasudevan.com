
confluent.tf

This Terraform configuration sets up a Confluent Cloud Kafka environment with private networking in Azure. Let me break down the main components:

1. Locals and Data Sources:
    
    hcl
    
    Apply
    
    locals {
    
      subnet_name_by_zone = {
    
        "1" = "default",
    
        "2" = "default",
    
        "3" = "default",
    
      }
    
    }
    

- Defines a map of availability zones to subnet names

- Fetches existing Azure VNet and subnet information

1. Confluent Environment:
    
    hcl
    
    Apply
    
    resource "confluent_environment" "environment" {
    
      display_name = var.environment
    
      stream_governance {
    
        package = "ESSENTIALS"
    
      }
    
    }
    

- Creates a Confluent Cloud environment

- Enables Stream Governance with ESSENTIALS package

1. Private Network Setup:
    
    hcl
    
    Apply
    
    resource "confluent_network" "azure_private_link" {
    
      display_name     = "${var.environment}-azure-private-link"
    
      cloud            = "AZURE"
    
      region           = var.cluster_location
    
      connection_types = ["PRIVATELINK"]
    
      # ...
    
    }
    

- Sets up private networking between Azure and Confluent

- Configures DNS resolution for private endpoints

1. Kafka Cluster:
    
    hcl
    
    Apply
    
    resource "confluent_kafka_cluster" "dedicated" {
    
      display_name = "canopy-${var.environment}"
    
      availability = var.cluster_availability
    
      cloud        = "AZURE"
    
      region       = var.cluster_location
    
      dedicated {
    
        cku = var.cluster_cku
    
      }
    
      # ...
    
    }
    

- Creates a dedicated Kafka cluster

- Configures availability and region settings

- Sets up private networking

1. Service Account and API Keys:
    
    hcl
    
    Apply
    
    resource "confluent_service_account" "manager" {
    
      display_name = "manager-${var.environment}"
    
      # ...
    
    }
    
    resource "confluent_api_key" "cluster_api_key" {
    
      # ...
    
    }
    
    resource "confluent_api_key" "schema_registry_api_key" {
    
      # ...
    
    }
    

- Creates a service account for management

- Generates API keys for cluster and schema registry access

- Sets up role bindings for permissions

1. Schema Registry:
    
    hcl
    
    Apply
    
    resource "confluent_schema_registry_cluster_config" "dedicated" {
    
      # ...
    
      compatibility_level = "BACKWARD_TRANSITIVE"
    
    }
    

- Configures the schema registry

- Sets compatibility level for schema evolution

1. Azure Private Endpoints:
    
    hcl
    
    Apply
    
    resource "azurerm_private_endpoint" "confluent" {
    
      for_each = local.subnet_name_by_zone
    
      # ...
    
    }
    

- Creates private endpoints for each availability zone

- Sets up private DNS zones and records

- Configures private service connections

1. DNS Configuration:
    
    hcl
    
    Apply
    
    resource "azurerm_private_dns_zone" "confluent" {
    
      # ...
    
    }
    
    resource "azurerm_private_dns_a_record" "confluent" {
    
      # ...
    
    }
    
    resource "azurerm_private_dns_a_record" "zonal" {
    
      # ...
    
    }
    

- Sets up private DNS zones

- Creates DNS records for the private endpoints

- Configures zone-specific DNS records

This configuration:

- Creates a secure, private Kafka environment

- Sets up proper networking between Azure and Confluent

- Configures necessary service accounts and permissions

- Establishes private DNS resolution

- Supports multi-zone deployment

- Includes schema registry configuration
```
locals {
  subnet_name_by_zone = {
    "1" = "default",
    "2" = "default",
    "3" = "default",
  }
}

#-----------------------------------------------------------------------------#
# Existing Resources
#-----------------------------------------------------------------------------#

# Resolve the Vnet for private endpoint
data "azurerm_virtual_network" "private_endpoints" {
  name                = var.private_endpoint_vnet_name
  resource_group_name = var.private_endpoint_vnet_resource_group_name
}

# Resolve the subnet for private endpoint
data "azurerm_subnet" "private_endpoints" {
  name                 = var.private_endpoint_vnet_subnet_name
  virtual_network_name = var.private_endpoint_vnet_name
  resource_group_name  = var.private_endpoint_vnet_resource_group_name
}

#-----------------------------------------------------------------------------#
# Confluent Environment
#-----------------------------------------------------------------------------#

resource "confluent_environment" "environment" {
  display_name = var.environment

  stream_governance {
    package = "ESSENTIALS"
  }
}

#-----------------------------------------------------------------------------#
# Confluent Network for Private Link
#-----------------------------------------------------------------------------#

resource "confluent_network" "azure_private_link" {
  display_name     = "${var.environment}-azure-private-link"
  cloud            = "AZURE"
  region           = var.cluster_location
  connection_types = ["PRIVATELINK"]

  environment {
    id = confluent_environment.environment.id
  }

  dns_config {
    resolution = "PRIVATE"
  }
}

#-----------------------------------------------------------------------------#
# Confluent Private Link Access
#-----------------------------------------------------------------------------#

resource "confluent_private_link_access" "azure_private_access" {
  display_name = "${var.environment}-private-link-access"

  azure {
    subscription = var.private_endpoint_subscription_id
  }

  environment {
    id = confluent_environment.environment.id
  }

  network {
    id = confluent_network.azure_private_link.id
  }
}

#-----------------------------------------------------------------------------#
# Kafka Cluster Definition
#-----------------------------------------------------------------------------#

# Create cluster
resource "confluent_kafka_cluster" "dedicated" {
  display_name = "canopy-${var.environment}"
  availability = var.cluster_availability
  cloud        = "AZURE"
  region       = var.cluster_location
  dedicated {
    cku = var.cluster_cku
  }

  environment {
    id = confluent_environment.environment.id
  }

  network {
    id = confluent_network.azure_private_link.id
  }
}


# Resolve the schema registry cluster
data "confluent_schema_registry_cluster" "dedicated" {
  environment {
    id = confluent_environment.environment.id
  }
  depends_on = [
    confluent_kafka_cluster.dedicated
  ]
}

# Create a service account for the cluster
resource "confluent_service_account" "manager" {
  display_name = "manager-${var.environment}"
  description  = "Service Account for ${var.environment} environment"
}

# Allow service account admin on environment
resource "confluent_role_binding" "manager" {
  principal   = "User:${confluent_service_account.manager.id}"
  role_name   = "EnvironmentAdmin"
  crn_pattern = confluent_environment.environment.resource_name
}

# Create an API key for managing cluster
resource "confluent_api_key" "cluster_api_key" {
  display_name           = "manager-${var.environment}-cluster"
  description            = "Manages cluster"
  disable_wait_for_ready = true
  owner {
    id          = confluent_service_account.manager.id
    api_version = confluent_service_account.manager.api_version
    kind        = confluent_service_account.manager.kind
  }

  managed_resource {
    id          = confluent_kafka_cluster.dedicated.id
    api_version = confluent_kafka_cluster.dedicated.api_version
    kind        = confluent_kafka_cluster.dedicated.kind

    environment {
      id = confluent_environment.environment.id
    }
  }
}

# Create an API key for the service account to use in subsequent steps
resource "confluent_api_key" "schema_registry_api_key" {
  display_name           = "manager-${var.environment}-schema-registry"
  description            = "Manages schema registry"
  disable_wait_for_ready = true
  owner {
    id          = confluent_service_account.manager.id
    api_version = confluent_service_account.manager.api_version
    kind        = confluent_service_account.manager.kind
  }

  managed_resource {
    id          = data.confluent_schema_registry_cluster.dedicated.id
    api_version = data.confluent_schema_registry_cluster.dedicated.api_version
    kind        = data.confluent_schema_registry_cluster.dedicated.kind

    environment {
      id = confluent_environment.environment.id
    }
  }
}

# Configure the schema registry cluster
resource "confluent_schema_registry_cluster_config" "dedicated" {
  schema_registry_cluster {
    id = data.confluent_schema_registry_cluster.dedicated.id
  }

  credentials {
    key    = confluent_api_key.schema_registry_api_key.id
    secret = confluent_api_key.schema_registry_api_key.secret
  }

  rest_endpoint       = data.confluent_schema_registry_cluster.dedicated.rest_endpoint
  compatibility_level = "BACKWARD_TRANSITIVE"
}

#-----------------------------------------------------------------------------#
# Azure Private Endpoint
#-----------------------------------------------------------------------------#

resource "azurerm_private_endpoint" "confluent" {
  for_each = local.subnet_name_by_zone

  name                = "pe-confluent-canopy-${var.environment}-${each.key}"
  location            = var.private_endpoint_location
  resource_group_name = var.private_endpoint_resource_group_name
  subnet_id           = data.azurerm_subnet.private_endpoints.id

  private_service_connection {
    name                              = "psc-confluent-canopy-${var.environment}-${each.key}"
    private_connection_resource_alias = lookup(confluent_network.azure_private_link.azure[0].private_link_service_aliases, each.key, "\n\nerror: ${each.key} subnet is missing from CCN's Private Link service aliases")
    is_manual_connection              = true
    request_message                   = "Requesting connection to Confluent Private Link Service for the ${var.environment} environment."
  }

  tags = var.tags
}

resource "azurerm_private_dns_zone" "confluent" {
  resource_group_name = var.private_endpoint_resource_group_name
  name                = confluent_network.azure_private_link.dns_domain
  tags = var.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "confluent" {
  name                  = var.private_endpoint_vnet_name
  resource_group_name   = var.private_endpoint_resource_group_name
  private_dns_zone_name = azurerm_private_dns_zone.confluent.name
  virtual_network_id    = data.azurerm_virtual_network.private_endpoints.id
  tags = var.tags
}

resource "azurerm_private_dns_a_record" "confluent" {
  name                = "*"
  zone_name           = azurerm_private_dns_zone.confluent.name
  resource_group_name = var.private_endpoint_resource_group_name
  ttl                 = 60
  records = [
    for _, ep in azurerm_private_endpoint.confluent : ep.private_service_connection[0].private_ip_address
  ]
  tags = var.tags
}

resource "azurerm_private_dns_a_record" "zonal" {
  for_each = local.subnet_name_by_zone

  name                = "*.az${each.key}"
  zone_name           = azurerm_private_dns_zone.confluent.name
  resource_group_name = var.private_endpoint_resource_group_name
  ttl                 = 60
  records = [
    azurerm_private_endpoint.confluent[each.key].private_service_connection[0].private_ip_address,
  ]
  tags = var.tags
}
```


Output.tf

This `output.tf` file defines various outputs that will be displayed after Terraform applies the configuration. Let me break down each output:

1. **Environment and Cluster IDs**:
```hcl
output "environment" {
  value = confluent_environment.environment.id
}

output "cluster_id" {
  value = confluent_kafka_cluster.dedicated.id
}
```
- Outputs the Confluent environment ID
- Outputs the Kafka cluster ID
- These IDs are useful for referencing in other Terraform configurations or scripts

2. **Connection Endpoints**:
```hcl
output "bootstrap_endpoint" {
  value = confluent_kafka_cluster.dedicated.bootstrap_endpoint
}

output "rest_endpoint" {
  value = confluent_kafka_cluster.dedicated.rest_endpoint
}

output "schema_registry_endpoint" {
  value = data.confluent_schema_registry_cluster.dedicated.rest_endpoint
}
```
- `bootstrap_endpoint`: The Kafka bootstrap server address
- `rest_endpoint`: The REST API endpoint for the Kafka cluster
- `schema_registry_endpoint`: The Schema Registry REST endpoint
- These endpoints are needed for applications to connect to Kafka

3. **Schema Registry API Keys**:
```hcl
output "schema_registry_api_key_id" {
  value = confluent_api_key.schema_registry_api_key.id
}

output "schema_registry_api_key_secret" {
  value = confluent_api_key.schema_registry_api_key.secret
}

output "schema_registry_api_auth" {
  sensitive = true
  value = "${confluent_api_key.schema_registry_api_key.id}:${confluent_api_key.schema_registry_api_key.secret}"
}
```
- Outputs the Schema Registry API key ID and secret separately
- Also outputs them combined in the format `id:secret`
- The `sensitive = true` flag marks the combined output as sensitive (won't show in logs)

4. **Cluster API Keys**:
```hcl
output "cluster_api_key_id" {
  value = confluent_api_key.cluster_api_key.id
}

output "cluster_api_key_secret" {
  value = confluent_api_key.cluster_api_key.secret
}
```
- Outputs the Kafka cluster API key ID and secret
- These are needed for applications to authenticate with Kafka

These outputs are useful for:
1. Getting connection information after deployment
2. Passing credentials to other systems
3. Configuring applications to connect to Kafka
4. Debugging and troubleshooting
5. Integration with other infrastructure components

The sensitive outputs (marked with `sensitive = true`) are particularly important for security as they contain credentials that shouldn't be exposed in logs or version control.

Would you like me to explain any specific output in more detail?

```
output "environment" {
  value = confluent_environment.environment.id
}

output "cluster_id" {
  value = confluent_kafka_cluster.dedicated.id
}

output "bootstrap_endpoint" {
  value = confluent_kafka_cluster.dedicated.bootstrap_endpoint
}

output "rest_endpoint" {
  value = confluent_kafka_cluster.dedicated.rest_endpoint
}

output "schema_registry_endpoint" {
  value = data.confluent_schema_registry_cluster.dedicated.rest_endpoint
}

output "schema_registry_api_key_id" {
  value = confluent_api_key.schema_registry_api_key.id
}

output "schema_registry_api_key_secret" {
  value = confluent_api_key.schema_registry_api_key.secret
}

output "schema_registry_api_auth" {
  sensitive = true
  value = "${confluent_api_key.schema_registry_api_key.id}:${confluent_api_key.schema_registry_api_key.secret}"
}

output "cluster_api_key_id" {
  value = confluent_api_key.cluster_api_key.id
}

output "cluster_api_key_secret" {
  value = confluent_api_key.cluster_api_key.secret
}



```





provider.tf

```
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.21.1"
      configuration_aliases = [
        azurerm.identity
      ]
    }
    confluent = {
      source  = "confluentinc/confluent"
      version = "~> 2.12.0"
    }
  }
}

```

variables.tf

```#-----------------------------------------------------------------------------#
# Environment
#-----------------------------------------------------------------------------#

variable "environment" {
  type = string
}

#-----------------------------------------------------------------------------#
# Cluster Configuration
#-----------------------------------------------------------------------------#

variable "cluster_availability" {
  description = "Cluster availability"
  type        = string
  default     = "SINGLE_ZONE"
}

variable "cluster_cku" {
  description = "Cluster Confluent Kafka Unit"
  type        = number
  default     = 1
}

variable "cluster_location" {
  description = "Cluster location"
  type        = string
  default     = "us-west-2"
}

#-----------------------------------------------------------------------------#
# Network Configuration
#-----------------------------------------------------------------------------#

variable "private_endpoint_location" {
  description = "Private endpoint location"
  type        = string
  default     = "centralus"
}

variable "private_endpoint_subscription_id" {
  description = "Azure subscription ID for private endpoint"
  type        = string
}

variable "private_endpoint_resource_group_name" {
  description = "Resource group where the private endpoint will be deployed"
  type        = string
}

variable "private_endpoint_vnet_resource_group_name" {
  description = "Resource group name for the virtual network for private endpoint"
  type        = string
}

variable "private_endpoint_vnet_name" {
  description = "Azure virtual network ID for private endpoint"
  type        = string
}

variable "private_endpoint_vnet_subnet_name" {
  description = "Azure subnet name for private endpoint"
  type        = string
}

#-----------------------------------------------------------------------------#
# Extras
#-----------------------------------------------------------------------------#

variable "tags" {
  type        = map(string)
  description = "Map of tags to apply to all resources"
  default     = null
}
```