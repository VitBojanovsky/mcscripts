# example.py:

import minescript

# Write a message to the chat that only you can see:
minescript.echo("Hello, world!")

# Write a chat message that other players can see:
minescript.chat("Hello, everyone!")

# Get your player's current position:
x, y, z = minescript.player_position()

# Set the block directly beneath your player:
x, y, z = int(x), int(y), int(z)
minescript.execute(f"setblock {x} {y-1} {z} yellow_concrete")

# Print the type of block at a particular location:
minescript.echo(minescript.getblock(x, y, z))

# Display the contents of your inventory:
for item_stack in minescript.player_inventory():
  minescript.echo(item_stack.item)

# Display the names of nearby entities:
for entity in minescript.entities():
  minescript.echo(entity.name)  