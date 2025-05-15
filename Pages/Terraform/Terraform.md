Let’s dive deep into how **Terraform plan** and **Terraform apply** work — both in high-level behavior and the **under-the-hood technical flow** (including the API calls and comparisons Terraform does internally).

If you’ve ever used **Terraform**, you already know the basic flow: **Write configs ➔ Plan ➔ Apply ➔ Infrastructure happens!**

![[Pasted image 20250428093153.png]]

![[image.gif]]

- Load Config
- Load State
- Initialize Providers
- Fetch Real Infrastructure
- Plan Changes
- Apply Changes
- Update State

But have you ever wondered what _really_ happens behind the scenes? How does Terraform **plan changes**? How does it **know** what to create, update, or destroy? Let’s open the hood and explore!

## High-Level Flow

1. **Terraform Init** Initialize backend. Install Provider Plugins. Module Installation. Validation and Setup
2. **Terraform Plan** Reads the **current state** (from your .tfstate file). **Reads your desired configuration** (from .tf files). Connects to **provider APIs** (like AWS, Azure, GCP) to **fetch real-world resource states**. **Diffs** (compares) the desired config vs real-world vs current state. Outputs a **plan** of what changes are needed (create, update, destroy).
3. **Terraform Apply** Takes that plan. Executes the necessary **API calls** to the provider(s) to **create/update/delete** resources. Updates the **terraform state file** after successful changes.

## BEHIND THE SCENES

## What is the Role of terraform init?

**Under the Hood: How Terraform Plan Works**

terraform init is the **first command** you run when starting to work with a new or existing Terraform configuration.

Its main role is to **prepare your working directory** for use with Terraform.

In simple words: 
It **sets up** everything Terraform needs before planning or applying any infrastructure changes.

## What Exactly Happens During terraform init?

Here’s a step-by-step view:

1. **Initialize Backend** If you are using a **remote backend** (like S3, Terraform Cloud, Consul), init configures it. Backends handle things like **state storage**, **locking**, and **history**.
2. **Install Provider Plugins** Terraform downloads the necessary **provider binaries** (like AWS, Azure, GCP, Kubernetes) that your configuration references. Providers are the bridge between Terraform and your cloud services!
3. **Module Installation** If your configs use **modules** (even remote ones from GitHub or Terraform Registry), init downloads them too.
4. **Validation and Setup** Checks your configuration files for syntax issues related to providers and backends. Ensures the directory is ready to run plan and apply without errors.

## Why terraform init is Important

 Without it, Terraform can’t connect to providers or manage state properly. 
 It ensures all **dependencies are installed** and the **backend is ready**. 
 It **saves you** from “provider not found” or “backend not configured” errors later.

## Quick Tip:

Whenever you:

- Add a new provider
- Change backend configuration
- Add or update a module

You **must rerun** terraform init (it’s safe to run multiple times!).

terraform init is like **starting the engine** of a car. Without it, you can’t plan, apply, or deploy anything!

It’s the _silent hero_ that gets everything ready for the real Terraform magic to begin. 

### What Happens During terraform plan?

When you run terraform plan, Terraform isn’t just reading your .tf files and guessing what needs to happen. It actually follows a **very smart, very detailed process**:

When you run terraform plan, Terraform isn’t just reading your .tf files and guessing what needs to happen. It actually follows a **very smart, very detailed process**:

### 1. Loading the Current State

Terraform first **reads your state file** (terraform.tfstate) — either local or remote. This file has the **metadata** about your managed resources: their IDs, settings, and outputs.

### 2. Parsing the Configuration

Next, it parses your **Terraform configurations** — your .tf files — into an internal model.

### 3. Initializing Providers

Terraform then initializes the **provider plugins** (AWS, Azure, GCP, etc.) based on your provider blocks. It loads authentication credentials, endpoints, and regional settings.

### 4. Fetching Real-World Infrastructure

Here’s where the magic starts! Terraform **calls the cloud provider APIs** to pull live data about your resources.

For every declared resource, Terraform uses the provider’s **Read** operation to get the real current state.

### 5. Diffing Phase (Real Intelligence)

Terraform now **compares**:

- The desired config (.tf files)
- The current state file
- The real-world resource fetched via API

And creates a **change plan**:

- What needs to be **created** 
- What needs to be **updated** 
- What needs to be **destroyed** 

### What Happens During terraform apply?

Once you approve the plan, terraform apply kicks off:

- It **executes API calls** to cloud providers to perform the required operations.
- **Creates**, **updates**, or **deletes** resources exactly as needed.
- After each successful operation, it **updates the in-memory state** immediately.
- Finally, Terraform **writes the updated state** back to your .tfstate file.

And just like that — _your infrastructure is alive and well!_

### Under the Microscope: Terraform + Cloud APIs

Every major action Terraform takes results in **specific API calls** to providers:

Terraform **does not trust** the state file blindly — it **validates** against live infrastructure every time. This ensures **consistency**, **accuracy**, and **drift detection**.

### Why Should You Care?

Understanding this deeper flow matters because:

- You can **troubleshoot** better when Terraform behaves “weirdly.”
- You appreciate why **state files** are so crucial.
- You realize why **cloud API limits**, **timeouts**, and **auth issues** impact Terraform runs.

Terraform isn’t magic — it’s a beautifully designed **automation engine** that interacts directly with your infrastructure in real-time.

## Final Thought

Next time you type terraform plan, remember: A whole universe of **live API interactions**, **state validations**, and **smart diffs** are happening behind the scenes — all to make your infra perfect. 

**Terraform isn’t just a tool; it’s an automation work of art. 

