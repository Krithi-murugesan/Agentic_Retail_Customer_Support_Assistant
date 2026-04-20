from crewai import Agent

router_agent = Agent(
    role="Router",
    goal="Decide if query needs order or policy lookup",
    verbose=True
)

order_agent = Agent(
    role="Order Specialist",
    goal="Fetch order data from DB",
    verbose=True
)

policy_agent = Agent(
    role="Policy Expert",
    goal="Retrieve policy info",
    verbose=True
)

response_agent = Agent(
    role="Support Assistant",
    goal="Generate final response",
    verbose=True
)
