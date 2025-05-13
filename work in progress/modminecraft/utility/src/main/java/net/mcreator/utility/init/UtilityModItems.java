
/*
 *    MCreator note: This file will be REGENERATED on each build.
 */
package net.mcreator.utility.init;

import net.minecraftforge.registries.RegistryObject;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.DeferredRegister;

import net.minecraft.world.item.Item;

import net.mcreator.utility.item.OverwordkeyItem;
import net.mcreator.utility.item.NightelmetItem;
import net.mcreator.utility.item.NetherkeyItem;
import net.mcreator.utility.item.FlatkeyItem;
import net.mcreator.utility.item.EndkeyItem;
import net.mcreator.utility.UtilityMod;

public class UtilityModItems {
	public static final DeferredRegister<Item> REGISTRY = DeferredRegister.create(ForgeRegistries.ITEMS, UtilityMod.MODID);
	public static final RegistryObject<Item> NIGHTELMET_HELMET = REGISTRY.register("nightelmet_helmet", () -> new NightelmetItem.Helmet());
	public static final RegistryObject<Item> FLATKEY = REGISTRY.register("flatkey", () -> new FlatkeyItem());
	public static final RegistryObject<Item> OVERWORDKEY = REGISTRY.register("overwordkey", () -> new OverwordkeyItem());
	public static final RegistryObject<Item> NETHERKEY = REGISTRY.register("netherkey", () -> new NetherkeyItem());
	public static final RegistryObject<Item> ENDKEY = REGISTRY.register("endkey", () -> new EndkeyItem());
	// Start of user code block custom items
	// End of user code block custom items
}
