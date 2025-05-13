
/*
 *    MCreator note: This file will be REGENERATED on each build.
 */
package net.mcreator.utility.init;

import net.minecraftforge.registries.RegistryObject;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.DeferredRegister;

import net.minecraft.world.level.block.Block;

import net.mcreator.utility.block.FlatdimentionPortalBlock;
import net.mcreator.utility.UtilityMod;

public class UtilityModBlocks {
	public static final DeferredRegister<Block> REGISTRY = DeferredRegister.create(ForgeRegistries.BLOCKS, UtilityMod.MODID);
	public static final RegistryObject<Block> FLATDIMENTION_PORTAL = REGISTRY.register("flatdimention_portal", () -> new FlatdimentionPortalBlock());
	// Start of user code block custom blocks
	// End of user code block custom blocks
}
