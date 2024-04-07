terraform {
  required_providers {
    azurerm = {
    }
  }
}
provider "azurerm" {
  features{}
}

resource "random_integer" "ri" {
  min = 10000
  max = 99999
}

resource "azurerm_resource_group" "example" {
  name     = "mddns-terraform-${random_integer.ri.result}"
  location = "westeurope"
}

resource "azurerm_service_plan" "appserviceplan" {
  name                = "${azurerm_resource_group.example.name}-plan"
  location            = "${azurerm_resource_group.example.location}"
  resource_group_name = "${azurerm_resource_group.example.name}"
  os_type             = "Linux"
  sku_name            = "B1"

}


resource "azurerm_linux_web_app" "dockerapp" {
  name                = "${azurerm_resource_group.example.name}-dockerapp"
  location            = "${azurerm_resource_group.example.location}"
  resource_group_name = "${azurerm_resource_group.example.name}"
  service_plan_id     = "${azurerm_service_plan.appserviceplan.id}"

   site_config {
    always_on      = "true"
    application_stack {
      docker_image_name = "ittraveler/docker-mddns"
    }
  }
}
