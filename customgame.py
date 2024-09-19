# TASK DEFINITIONS
tasks = {
    "brush teeth": {
        "needs": {},  # Requires 1 unit of water
        "depletes": {"toothpaste": 1},  # Depletes 1 unit of toothpaste
        "place": "bathroom",  # Needs to be in the bathroom
        "cost": 15,  # Cost of brushing teeth
    },
    "drink water": {
        "needs": {"water": 1},  # Requires 1 unit of water
        "depletes": {"water": 1},  # Depletes 1 unit of water
        "place": "kitchen",
        "cost": 5,
    },
    "buy water": {
        "needs": {},  # No specific resource needs
        "depletes": {},  # No resources are depleted
        "place": "store",
        "cost": 20,
    }
}

# STORAGES
main_stock = {}  # Main stock for refilling room-specific stocks
room_stocks = {  # Dictionary to hold stocks for each room
    "kitchen": {"water": 0, "soap": 1},
    "bathroom": {"water": 0, "toothpaste": 0},
    "store": {"water": 100, "soap": 100, "toothpaste": 100},  # Store stock to buy resources
}

# CHECK LEVELS OF RESOURCE
def check_needs(task):
    return tasks.get(task, {}).get("needs", {})

# Method to check what a task depletes
def check_depletes(task):
    return tasks.get(task, {}).get("depletes", {})

def check_place(task):
    return tasks.get(task, {}).get("place", "")

def check_main_stock(resource):
    return main_stock.get(resource, 0)

# Method to check stock in a specific room
def check_room_stock(room, resource):
    return room_stocks.get(room, {}).get(resource, 0)

# INITIALIZE PLAYER AND GAME
player_location = "home"  # Starting location
total_cost = 0  # Track total cost

# Initialize main stock with resources
def init_main_stock(resources):
    global main_stock
    main_stock = resources.copy()

# Method to refill resources in a room from the main stock
def refill_room(room, resource, X):
    global total_cost, main_stock
    if main_stock.get(resource, 0) >= X:
        room_stocks[room][resource] += X
        main_stock[resource] -= X
        # total_cost += 5  # Assume refilling room costs 5
        print(f"Refilled {X} {resource}(s) in the {room}. Main stock left: {main_stock[resource]}. Cost: 5")
    else:
        print(f"Not enough {resource} in the main stock to refill {room}. Needed: {X}, Available: {main_stock.get(resource, 0)}.")

# Method to buy resources from the store to replenish the main stock
def buy_resource(resource, X):
    global total_cost, room_stocks, main_stock
    if room_stocks["store"].get(resource, 0) >= X:
        room_stocks["store"][resource] -= X
        main_stock[resource] = main_stock.get(resource, 0) + X
        total_cost += 20  # Assume buying from the store costs 20
        print(f"Bought {X} {resource}(s) from the store. Cost: 20")
    else:
        print(f"Store doesn't have enough {resource}. Needed: {X}, Available: {room_stocks['store'].get(resource, 0)}.")

# Method to change location
def goto(place):
    global player_location, total_cost
    if player_location != place:
        player_location = place
        total_cost += 5  # Assume moving locations costs 5
        print(f"Moved to {place}. Cost: 5")
    else:
        print(f"Already at {place}.")
    
# Method to check current location
def where():
    return player_location


# Function to execute tasks
def execute_tasks(task_list):
    global total_cost

    for task in task_list:
        # Check if task exists
        if task not in tasks:
            print(f"Task '{task}' not recognized.")
            return "Failure"
        
        if 'check inventory' in tasks:
            resource = task.split()[3]
            print(check_main_stock(resource))
            continue

        if 'check' in tasks:
            room = task.split()[1]
            resource = task.split()[3]
            print(check_room_stock(room, resource))
            continue

        if 'go to' in task or 'Go to' in task:
            place = task.split()[2]
            goto(place)
            continue
        
        # Check required location
        place = check_place(task)
        # if where() != place:
        #     goto(place)

        if 'buy' in task:
            resource = task.split()[2]
            amount = int(task.split()[1])
            buy_resource(resource, amount)
            continue

        if 'refill' in task:
            room = task.split()[2]
            resource = task.split()[4]
            amount = int(task.split()[3])
            refill_room(room, resource, amount)
            continue

        # Check if required resources are available in the current room
        needs = check_needs(task)
        for resource, amount in needs.items():
            if check_room_stock(where(), resource) < amount:
                print(f"Not enough {resource} in {where()} to complete {task}. Needed: {amount}, Available: {check_room_stock(where(), resource)}.")
                return "Failure"
        
        # Deplete resources from the room stock
        depletes = check_depletes(task)
        for resource, amount in depletes.items():
            if check_room_stock(where(), resource) >= amount:
                room_stocks[where()][resource] -= amount
                print(f"Depleted {amount} {resource}(s) in {where()} for {task}. Remaining: {room_stocks[where()][resource]}")
            else:
                print(f"Not enough {resource} in {where()} to complete {task}. Needed: {amount}, Available: {check_room_stock(where(), resource)}.")
                return "Failure"

        # Add task cost to total cost
        task_cost = tasks[task]["cost"]
        total_cost += task_cost
        print(f"Executed {task}. Cost: {task_cost}")
    
    print(f"All tasks executed successfully. Total cost: {total_cost}")
    return "Success"

# Initialize main stock with resources
init_main_stock({"water": 5, "toothpaste": 2})

# Define a list of tasks to execute
task_list = ["refill toothpaste", "brush teeth", "drink water", "buy water"]

print(check_room_stock("kitchen", "soap"))
# Execute the tasks and track success/failure
result = execute_tasks(task_list)
print(result)

# # Example: Refilling resources
# goto("kitchen")
# refill_room("kitchen", "water", 3)  # Refill water in kitchen from main stock

# # Example: Buying resources
# goto("store")
# buy_resource("water", 5)  # Buy 5 units of water from the store

