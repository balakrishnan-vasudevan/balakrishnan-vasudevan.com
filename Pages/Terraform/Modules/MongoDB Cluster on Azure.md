
1. mongo.tf

- This is the main resource definition file that contains all the infrastructure components

- Key components:

- MongoDB Atlas project and cluster configuration

- Search deployment settings

- Private link connection setup between Azure and MongoDB Atlas

- Auto-scaling configurations

- Security settings (TLS, backup, etc.)

- This file defines the actual infrastructure that will be created

```
#-----------------------------------------------------------------------------#
# Existing Resources
#-----------------------------------------------------------------------------#

# Resolve the subnet for private endpoint
data "azurerm_subnet" "private_endpoints" {
  name                 = var.private_endpoint_vnet_subnet_name
  virtual_network_name = var.private_endpoint_vnet_name
  resource_group_name  = var.private_endpoint_vnet_resource_group_name
}

#-----------------------------------------------------------------------------#
# MongoDB Atlas Resources
#-----------------------------------------------------------------------------#

# MongoDB Atlas Project
resource "mongodbatlas_project" "project" {
  org_id = var.atlas_org_id
  name   = "${var.project_name}-${var.environment}"
  lifecycle {
    ignore_changes = [
      teams
    ]
  }
}

# MongoDB Atlas Cluster
resource "mongodbatlas_advanced_cluster" "cluster" {
  project_id                     = mongodbatlas_project.project.id
  name                           = "${var.project_name}-${var.environment}"
  cluster_type                   = "REPLICASET"
  backup_enabled                 = true
  retain_backups_enabled         = true
  pit_enabled                    = true
  termination_protection_enabled = true
  mongo_db_major_version         = var.cluster_mongo_version
  replica_set_scaling_strategy   = "WORKLOAD_TYPE"

  replication_specs {
    region_configs {
      provider_name = "AZURE"
      region_name   = var.cluster_region
      priority      = 7

      electable_specs {
        instance_size = var.cluster_instance_size
        disk_size_gb  = var.cluster_disk_size_gb
        node_count    = var.cluster_node_count
      }

      auto_scaling {
        disk_gb_enabled           = true
        compute_enabled           = true
        compute_min_instance_size = var.cluster_min_instance_size
        compute_max_instance_size = var.cluster_max_instance_size
      }
    }
  }

  advanced_configuration {
    javascript_enabled                 = true
    minimum_enabled_tls_protocol       = "TLS1_2"
    oplog_min_retention_hours          = 74
    transaction_lifetime_limit_seconds = 60
    default_write_concern              = "majority"
  }

  lifecycle {
    ignore_changes = [ 
      replication_specs[0].region_configs[0].electable_specs[0].instance_size,
      replication_specs[0].region_configs[0].electable_specs[0].disk_size_gb,
      replication_specs[0].region_configs[0].auto_scaling[0].compute_min_instance_size
    ]
  }
}

# MongoDB Atlas Search Deployment (dedicated search nodes)
resource "mongodbatlas_search_deployment" "search" {
  project_id   = mongodbatlas_project.project.id
  cluster_name = mongodbatlas_advanced_cluster.cluster.name

  specs = [
    {
      instance_size = var.search_instance_size
      node_count    = var.search_node_count
    }
  ]
}

#-----------------------------------------------------------------------------#
# Privatelink Connection
#-----------------------------------------------------------------------------#

# MongoDB Atlas PrivateLink Endpoint
resource "mongodbatlas_privatelink_endpoint" "private_endpoint" {
  project_id    = mongodbatlas_project.project.id
  provider_name = "AZURE"
  region        = var.private_endpoint_location
}

# Azure Private Endpoint for MongoDB Atlas
resource "azurerm_private_endpoint" "mongo_private_endpoint" {
  name                = "pe-mongo-${var.project_name}-${var.environment}"
  location            = var.private_endpoint_location
  resource_group_name = var.private_endpoint_resource_group_name
  subnet_id           = data.azurerm_subnet.private_endpoints.id

  private_service_connection {
    name                           = "psc-mongo-${var.project_name}-${var.environment}"
    private_connection_resource_id = mongodbatlas_privatelink_endpoint.private_endpoint.private_link_service_resource_id
    is_manual_connection           = true
    request_message                = "Please approve the connection to MongoDB Atlas PrivateLink Endpoint"
  }

  tags = var.tags
}

# Actually create the service to enable private link connections
resource "mongodbatlas_privatelink_endpoint_service" "dedicated" {
  project_id            = mongodbatlas_privatelink_endpoint.private_endpoint.project_id
  private_link_id       = mongodbatlas_privatelink_endpoint.private_endpoint.private_link_id
  endpoint_service_id   = azurerm_private_endpoint.mongo_private_endpoint.id
  private_endpoint_ip_address = azurerm_private_endpoint.mongo_private_endpoint.private_service_connection.0.private_ip_address
  provider_name = "AZURE"
}
```

2. output.tf

- Contains the output definitions that will be displayed after Terraform applies the configuration

- In this case, it outputs:

- The private connection string for the MongoDB cluster

- Outputs are useful for:

- Getting important information after deployment

- Passing information to other Terraform modules

- Displaying important connection details

```
output "mongodb_private_link_endpoint" {
  value = mongodbatlas_advanced_cluster.cluster.connection_strings[0].private_endpoint[0].srv_connection_string
}
```

3. provider.tf

- Defines the required providers and their versions

- In this case, it specifies:

- MongoDB Atlas provider (version >= 1.6.0)

- Azure provider (version ~> 4.21.1)

- This file ensures:

- Correct provider versions are used

- Required providers are available

- Compatibility between providers

```
terraform {
  required_providers {
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = ">= 1.6.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.21.1"
    }
  }
}
```

4. variables.tf

- Contains all the input variables that can be configured

- Organized into sections:

- Environment Configuration (project name, environment)

- Cluster Configuration (MongoDB settings, sizes, versions)

- Networking (private endpoint settings)

- Extras (tags)

- Variables allow:

- Customization of the deployment

- Reuse of the same code for different environments

- Separation of configuration from code

```
#-----------------------------------------------------------------------------#
# Environment Configuration
#-----------------------------------------------------------------------------#

variable "project_name" {
  type        = string
  description = "Name of the project"
}

variable "environment" {
  type        = string
  description = "Environment name (e.g., dev, qa, prod)"
}

#-----------------------------------------------------------------------------#
# Cluster Configuration
#-----------------------------------------------------------------------------#

variable "atlas_org_id" {
  type        = string
  description = "MongoDB Atlas organization ID"
}

variable "cluster_region" {
  type        = string
  description = "Region for the MongoDB Atlas cluster"
}

variable "cluster_mongo_version" {
  type        = string
  description = "MongoDB version"
}

variable "cluster_instance_size" {
  type        = string
  description = "Cluster instance size (e.g., M80)"
}

variable "cluster_max_instance_size" {
  type        = string
  description = "Max cluster instance size during autoscaling (e.g., M80)"
}

variable "cluster_min_instance_size" {
  type        = string
  description = "Min cluster instance size during autoscaling (e.g., M80)"
}

variable "cluster_disk_size_gb" {
  type        = number
  description = "Cluster disk size in GB"
}

variable "cluster_node_count" {
  type        = number
  description = "Cluster node count"
}

variable "search_instance_size" {
  type        = string
  default     = "S50"
  description = "Search instance size (e.g., S50)"
}

variable "search_node_count" {
  type        = number
  default     = 2
  description = "Number of search nodes"
}

#-----------------------------------------------------------------------------#
# Networking
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