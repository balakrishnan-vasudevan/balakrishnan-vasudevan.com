Procedure:
1. Handle alert + Create incident
	1. Ack the alert
		1. Ack the page 
		2. Reply to the customer that it is being investigated
		3. for service owner reported issues, reply to the owner that you are beginning the IMS process.
	2. Evaluate alert + impact 
		1. Correlate alert info with other observability signals 
		2. Check if there is an ongoing change, deployment, or maintenance
		3. Identify which services are impacted
		4. Which clusters/datacenters are impacted
	3. Prioritize the incident
		1. Determine incident severity
		2. Is this a production incident?
		3. Determine if a bridge is necessary
	4. Create incident artifacts
		1. Create an incident response channel, tickets etc.
	5. Assess initial CAN
		1. Gather initial understanding from the channel
		2. Consider customer impact, blast radius, priority/severity
		3. Make sure teams are engaged
	5. Update incident artifacts
	6. Announce the incident on necessary channels - provide summaries regularly.
2. Assemble responders
	Input = Incident Record, Slack IR channel
	Output = Pagerduty pages, Slack mentions
	1. Determine if secondary SRE support is needed. When? If there is an external customer impact, high severity internal engineering impact, other complex situations
	2. Determine which SMEs to engage - search service catalog/registry to identify owners
	3. Page the appropriate teams
3. Begin Incident command loop
	1. Size up the situation.
		1. primary functions of incident command:
			1. Ensure everyone is on same page
			2. Establish common ground regarding the incident
			3. Communicate the common ground to everyone
			4. Create a CAN report - Conditions, Actions, Needs
		2. What recent actions have been taken?
		3. What is the current status?
		4. Do the proposed solutions seem like the right thing to do?
			1. What is the impact of making a config change or pushing out a release?
			2. Does the change have dependency or customer impact?
			3. Does the change resolve an incident completely or a part of it?
		5. Assess if any additional resources are needed.
			1. Are the right teams engaged on the bridge?
			2. Is everyone necessary for the incident on the bridge?
			3. Are the SMEs engaged reasonably able to assist?
			4. Is the incident commander, fatigued or otherwise unable to perform incident response?
		6. Engage additional resources if necessary
		7. Assess the need for unified command - necessary for external customer impacting incidents.
		8. Assess the severity/impact of the incident and escalate if needed
		9. Send updates or TCEs (technical Customer Escalation)
		10. Repeat IC loop until the incident is resolved.
4. Resolve the incident
	1. Ensure everyone is out of impact
	2. Resolve the incident record
	3. Create/Associate a problem record.
	4. Archive the Slack channel
	5. Confirm your incident is marked as completed.
	