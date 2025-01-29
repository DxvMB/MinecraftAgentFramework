# Import necessary modules
import mcpi.minecraft as Minecraft
import mcpi.block as block
from MinecraftAgentFramework.mcpi import minecraft

# Connect to the Minecraft game
mc = minecraft.Minecraft.create()
# Interact with the Minecraft world
mc.postToChat("Hello Minecraft World")
pos = mc.player.getTilePos()
mc.setBlock(pos.x+3, pos.y, pos.z, block.STONE.id)