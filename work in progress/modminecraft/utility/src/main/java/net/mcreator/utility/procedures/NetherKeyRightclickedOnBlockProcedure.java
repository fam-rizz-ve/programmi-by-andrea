package net.mcreator.utility.procedures;

import net.minecraftforge.items.ItemHandlerHelper;

import net.minecraft.world.level.Level;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.resources.ResourceKey;
import net.minecraft.network.protocol.game.ClientboundUpdateMobEffectPacket;
import net.minecraft.network.protocol.game.ClientboundPlayerAbilitiesPacket;
import net.minecraft.network.protocol.game.ClientboundLevelEventPacket;
import net.minecraft.network.protocol.game.ClientboundGameEventPacket;
import net.minecraft.core.BlockPos;

import net.mcreator.utility.network.UtilityModVariables;
import net.mcreator.utility.init.UtilityModItems;

public class NetherkeyRightclickedOnBlockProcedure {
	public static void execute(Entity entity) {
		if (entity == null)
			return;
		if (entity instanceof Player _player) {
			ItemStack _stktoremove = new ItemStack(UtilityModItems.NETHERKEY.get());
			_player.getInventory().clearOrCountMatchingItems(p -> _stktoremove.getItem() == p.getItem(), 1, _player.inventoryMenu.getCraftSlots());
		}
		if (((entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).orElse(new UtilityModVariables.PlayerVariables())).last_key).equals("flate key")) {
			if (entity instanceof Player _player) {
				ItemStack _setstack = new ItemStack(UtilityModItems.FLATKEY.get()).copy();
				_setstack.setCount(1);
				ItemHandlerHelper.giveItemToPlayer(_player, _setstack);
			}
			{
				double _setval = entity.getX();
				entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
					capability.ultima_x_flat = _setval;
					capability.syncPlayerVariables(entity);
				});
			}
			{
				double _setval = entity.getY();
				entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
					capability.ultima_y_flat = _setval;
					capability.syncPlayerVariables(entity);
				});
			}
			{
				double _setval = entity.getZ();
				entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
					capability.ultima_z_flat = _setval;
					capability.syncPlayerVariables(entity);
				});
			}
		} else if (((entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).orElse(new UtilityModVariables.PlayerVariables())).last_key).equals("overword key")) {
			if (entity instanceof Player _player) {
				ItemStack _setstack = new ItemStack(UtilityModItems.OVERWORDKEY.get()).copy();
				_setstack.setCount(1);
				ItemHandlerHelper.giveItemToPlayer(_player, _setstack);
			}
			{
				double _setval = entity.getX();
				entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
					capability.ultima_x_overword = _setval;
					capability.syncPlayerVariables(entity);
				});
			}
			{
				double _setval = entity.getY();
				entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
					capability.ultima_y_overword = _setval;
					capability.syncPlayerVariables(entity);
				});
			}
			{
				double _setval = entity.getZ();
				entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
					capability.ultima_z_overword = _setval;
					capability.syncPlayerVariables(entity);
				});
			}
		} else if (((entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).orElse(new UtilityModVariables.PlayerVariables())).last_key).equals("nether key")) {
			if (entity instanceof Player _player) {
				ItemStack _setstack = new ItemStack(UtilityModItems.NETHERKEY.get()).copy();
				_setstack.setCount(1);
				ItemHandlerHelper.giveItemToPlayer(_player, _setstack);
			}
			{
				double _setval = entity.getX();
				entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
					capability.ultima_x_nether = _setval;
					capability.syncPlayerVariables(entity);
				});
			}
			{
				double _setval = entity.getY();
				entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
					capability.ultima_y_nether = _setval;
					capability.syncPlayerVariables(entity);
				});
			}
			{
				double _setval = entity.getZ();
				entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
					capability.ultima_z_nether = _setval;
					capability.syncPlayerVariables(entity);
				});
			}
		} else if (((entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).orElse(new UtilityModVariables.PlayerVariables())).last_key).equals("end key")) {
			if (entity instanceof Player _player) {
				ItemStack _setstack = new ItemStack(UtilityModItems.ENDKEY.get()).copy();
				_setstack.setCount(1);
				ItemHandlerHelper.giveItemToPlayer(_player, _setstack);
			}
			{
				double _setval = entity.getX();
				entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
					capability.ultima_x_end = _setval;
					capability.syncPlayerVariables(entity);
				});
			}
			{
				double _setval = entity.getY();
				entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
					capability.ultima_y_end = _setval;
					capability.syncPlayerVariables(entity);
				});
			}
			{
				double _setval = entity.getZ();
				entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
					capability.ultima_z_end = _setval;
					capability.syncPlayerVariables(entity);
				});
			}
		}
		{
			String _setval = "nether key";
			entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
				capability.last_key = _setval;
				capability.syncPlayerVariables(entity);
			});
		}
		{
			Entity _ent = entity;
			_ent.teleportTo(((entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).orElse(new UtilityModVariables.PlayerVariables())).ultima_x_nether),
					((entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).orElse(new UtilityModVariables.PlayerVariables())).ultima_y_nether),
					((entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).orElse(new UtilityModVariables.PlayerVariables())).ultima_z_nether));
			if (_ent instanceof ServerPlayer _serverPlayer)
				_serverPlayer.connection.teleport(((entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).orElse(new UtilityModVariables.PlayerVariables())).ultima_x_nether),
						((entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).orElse(new UtilityModVariables.PlayerVariables())).ultima_y_nether),
						((entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).orElse(new UtilityModVariables.PlayerVariables())).ultima_z_nether), _ent.getYRot(), _ent.getXRot());
		}
		if (entity instanceof ServerPlayer _player && !_player.level().isClientSide()) {
			ResourceKey<Level> destinationType = Level.NETHER;
			if (_player.level().dimension() == destinationType)
				return;
			ServerLevel nextLevel = _player.server.getLevel(destinationType);
			if (nextLevel != null) {
				_player.connection.send(new ClientboundGameEventPacket(ClientboundGameEventPacket.WIN_GAME, 0));
				_player.teleportTo(nextLevel, _player.getX(), _player.getY(), _player.getZ(), _player.getYRot(), _player.getXRot());
				_player.connection.send(new ClientboundPlayerAbilitiesPacket(_player.getAbilities()));
				for (MobEffectInstance _effectinstance : _player.getActiveEffects())
					_player.connection.send(new ClientboundUpdateMobEffectPacket(_player.getId(), _effectinstance));
				_player.connection.send(new ClientboundLevelEventPacket(1032, BlockPos.ZERO, 0, false));
			}
		}
		{
			String _setval = "true";
			entity.getCapability(UtilityModVariables.PLAYER_VARIABLES_CAPABILITY, null).ifPresent(capability -> {
				capability.switch_dimension = _setval;
				capability.syncPlayerVariables(entity);
			});
		}
	}
}
