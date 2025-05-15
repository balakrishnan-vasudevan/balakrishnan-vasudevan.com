
```
import argparse
import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Replace with your Azure Key Vault URL
key_vault_url = ""

def create_secret_single(key_vault_url, secret_name, secret_value):
    """Create a single secret in Azure Key Vault."""
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)
        secret = client.set_secret(secret_name, secret_value)
        print(f"Secret '{secret_name}' created. Identifier: {secret.id}")
        return secret.id
    except Exception as e:
        print(f"Error creating secret '{secret_name}': {e}")
        return None

def delete_secret_single(key_vault_url, secret_name):
    """Delete a single secret from Azure Key Vault."""
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)
        client.begin_delete_secret(secret_name)
        print(f"Secret '{secret_name}' has been deleted.")
    except Exception as e:
        print(f"Error deleting secret '{secret_name}': {e}")

def create_secrets_bulk(key_vault_url, csv_file_path):
    """Create secrets in bulk from a CSV file and update the file with secret URLs."""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    
    try:
        secrets_df = pd.read_csv(csv_file_path)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return

    if "Name" not in secrets_df.columns or "Secret Value" not in secrets_df.columns:
        print("CSV file must contain 'Name' and 'Secret Value' columns.")
        return
    
    if "Secret URL" not in secrets_df.columns:
        secrets_df["Secret URL"] = ""

    for index, row in secrets_df.iterrows():
        secret_name = row["Name"]
        secret_value = row["Secret Value"]
        
        try:
            secret = client.set_secret(secret_name, secret_value)
            print(f"Secret '{secret_name}' created. Identifier: {secret.id}")
            secrets_df.at[index, "Secret URL"] = secret.id
        except Exception as e:
            print(f"Error creating/updating secret '{secret_name}': {e}")
            secrets_df.at[index, "Secret URL"] = f"Error: {e}"

    try:
        secrets_df.to_csv(csv_file_path, index=False)
        print(f"Updated CSV file with Secret URLs saved to {csv_file_path}")
    except Exception as e:
        print(f"Error saving updated CSV file: {e}")

def delete_secrets_bulk(key_vault_url, csv_file_path):
    """Delete secrets in bulk from Azure Key Vault based on a CSV file."""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    
    try:
        secrets_df = pd.read_csv(csv_file_path)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return

    if "Name" not in secrets_df.columns:
        print("CSV file must contain a 'Name' column.")
        return

    for index, row in secrets_df.iterrows():
        secret_name = row["Name"]
        
        try:
            client.begin_delete_secret(secret_name)
            print(f"Secret '{secret_name}' has been deleted.")
        except Exception as e:
            print(f"Error deleting secret '{secret_name}': {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Azure Key Vault Secret Management Script")
    parser.add_argument("-bulk", help="Create secrets from a CSV file", action="store_true")
    parser.add_argument("-delete_bulk", help="Delete secrets from a CSV file", action="store_true")
    parser.add_argument("-single", help="Create a single secret", action="store_true")
    parser.add_argument("-delete_single", help="Delete a single secret", action="store_true")
    parser.add_argument("--file", help="Path to the CSV file (for bulk operations)", type=str)
    parser.add_argument("--name", help="Secret name (for single operations)", type=str)
    parser.add_argument("--value", help="Secret value (for single creation)", type=str)

    args = parser.parse_args()

    if args.bulk:
        if not args.file:
            print("Error: --file argument is required for bulk creation.")
        else:
            create_secrets_bulk(key_vault_url, args.file)
    elif args.delete_bulk:
        if not args.file:
            print("Error: --file argument is required for bulk deletion.")
        else:
            delete_secrets_bulk(key_vault_url, args.file)
    elif args.single:
        if not args.name or not args.value:
            print("Error: --name and --value arguments are required for single secret creation.")
        else:
            create_secret_single(key_vault_url, args.name, args.value)
    elif args.delete_single:
        if not args.name:
            print("Error: --name argument is required for single secret deletion.")
        else:
            delete_secret_single(key_vault_url, args.name)
    else:
        print("Error: You must specify one of -bulk, -delete_bulk, -single, or -delete_single.")
```