import minescript
import time

player = minescript.player()  
def sell_items():
    minescript.chat("/sell")
    exit()


while True:
    item_stack = player.getMainHandItem()
    inventory = player.getInventory()
    inventory_full = all(slot is not None for slot in inventory)

    if item_stack.isEmpty() or not item_stack.isDamageableItem():
        minescript.echo("No usable tool in hand.")
        break

    current_damage = item_stack.getDamageValue()
    max_durability = item_stack.getMaxDamage()
    remaining = max_durability - current_damage

    if remaining <= 20:
        minescript.echo(f"Your tool is almost broken! Remaining durability: {remaining}")
        break

    if inventory_full:
        minescript.echo("Stopping: inventory full.")
        #sell_items()
        exit()

    pos = player.getBlockPos()
    look = player.getLookVec()

    front_x = int(pos.x + look.x)
    front_y = int(pos.y + look.y)
    front_z = int(pos.z + look.z)

    behind_x = int(pos.x + look.x * 2)
    behind_y = int(pos.y + look.y * 2)
    behind_z = int(pos.z + look.z * 2)

    minescript.breakBlock(front_x, front_y, front_z)
    minescript.breakBlock(behind_x, behind_y, behind_z)

    time.sleep(0.15)