Automates config management and orchestration and deployment
Ansible is a push tool
Orchestration: Integration of multiple applications and executing them in a particular order
Config Mgmt: Consistency of all systems in the infrastructure is maintained
Deployment: Apps are deployed automatically on a variety of environments

Ansible is agentless, efficient, flexible, simple, idempotent, and has automated reporting


Ansible host file: /etc/ansible/hosts
Add group name
```
[webserver]
web1.machine
web2.machine
[databaseserver]
db1.machine
db2.machine
db3.machine
```

Playbook - Config files in ansible, written in YAML


```
---
- name: sample book /*name of playbook*
  hosts: /*add grup name*
  remote_user: root
  become: true <privilege escalation
  tasks: /*what playbook does*
	  - name: install httpd
	    yum: /*yum command to run*
		    name: httpd
		    state: latest
	  - name: run httpd
		service:
				name: httpd
				state: started
	  - name: create content
		copy:
			content: "Congrats on installing ansible"
			dest: /var/www/html/index.html
```

check syntax ==> ansible-playbook sample.yml --syntax-check

push to client machine ===> ansible-playbook sample.yml

Why Ansible?
Tool that provides IT automation, consistency, and helps to deploy applications automatically


Pull config tool: Nodes check with server periodically and fetch configs from it
Push config - Server pushes config to nodes, no client on remote servers

Ansible uses Push config.

Architecture:
Local Machine -----> Nodes

Local machine files:
	1. Module - Playbooks, Config files in modules are called Playbooks
	2. Inventory - groups nodes under specific labels
Local machine connects to the nodes through an SSH client.

Playbooks:
Instructions to configure nodes
written in YAML

Inventory:
Classifies nodes into groups
Maintains structure of n/w environments

Playbook and inventory are in local machine
SSH used to communicate to nodes
Playbook is then sent to nodes

Why Ansible over Chef or Puppet?


Ansible Tower
Framework for Ansible
GUI to reduce dependency on command prompt window
Instead of typing long commands, you can now do it with a simple click
