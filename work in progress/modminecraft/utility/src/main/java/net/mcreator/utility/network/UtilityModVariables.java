package net.mcreator.utility.network;

import net.minecraftforge.network.PacketDistributor;
import net.minecraftforge.network.NetworkEvent;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.event.AttachCapabilitiesEvent;
import net.minecraftforge.common.util.LazyOptional;
import net.minecraftforge.common.util.FakePlayer;
import net.minecraftforge.common.capabilities.RegisterCapabilitiesEvent;
import net.minecraftforge.common.capabilities.ICapabilitySerializable;
import net.minecraftforge.common.capabilities.CapabilityToken;
import net.minecraftforge.common.capabilities.CapabilityManager;
import net.minecraftforge.common.capabilities.Capability;

import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.Entity;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.nbt.Tag;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.core.Direction;
import net.minecraft.client.Minecraft;

import net.mcreator.utility.UtilityMod;

import java.util.function.Supplier;

@Mod.EventBusSubscriber(bus = Mod.EventBusSubscriber.Bus.MOD)
public class UtilityModVariables {
	@SubscribeEvent
	public static void init(FMLCommonSetupEvent event) {
		UtilityMod.addNetworkMessage(PlayerVariablesSyncMessage.class, PlayerVariablesSyncMessage::buffer, PlayerVariablesSyncMessage::new, PlayerVariablesSyncMessage::handler);
	}

	@SubscribeEvent
	public static void init(RegisterCapabilitiesEvent event) {
		event.register(PlayerVariables.class);
	}

	@Mod.EventBusSubscriber
	public static class EventBusVariableHandlers {
		@SubscribeEvent
		public static void onPlayerLoggedInSyncPlayerVariables(PlayerEvent.PlayerLoggedInEvent event) {
			if (!event.getEntity().level().isClientSide())
				((PlayerVariables) event.getEntity().getCapability(PLAYER_VARIABLES_CAPABILITY, null).orElse(new PlayerVariables())).syncPlayerVariables(event.getEntity());
		}

		@SubscribeEvent
		public static void onPlayerRespawnedSyncPlayerVariables(PlayerEvent.PlayerRespawnEvent event) {
			if (!event.getEntity().level().isClientSide())
				((PlayerVariables) event.getEntity().getCapability(PLAYER_VARIABLES_CAPABILITY, null).orElse(new PlayerVariables())).syncPlayerVariables(event.getEntity());
		}

		@SubscribeEvent
		public static void onPlayerChangedDimensionSyncPlayerVariables(PlayerEvent.PlayerChangedDimensionEvent event) {
			if (!event.getEntity().level().isClientSide())
				((PlayerVariables) event.getEntity().getCapability(PLAYER_VARIABLES_CAPABILITY, null).orElse(new PlayerVariables())).syncPlayerVariables(event.getEntity());
		}

		@SubscribeEvent
		public static void clonePlayer(PlayerEvent.Clone event) {
			event.getOriginal().revive();
			PlayerVariables original = ((PlayerVariables) event.getOriginal().getCapability(PLAYER_VARIABLES_CAPABILITY, null).orElse(new PlayerVariables()));
			PlayerVariables clone = ((PlayerVariables) event.getEntity().getCapability(PLAYER_VARIABLES_CAPABILITY, null).orElse(new PlayerVariables()));
			clone.last_key = original.last_key;
			clone.ultima_y_flat = original.ultima_y_flat;
			clone.ultima_x_flat = original.ultima_x_flat;
			clone.ultima_z_flat = original.ultima_z_flat;
			clone.ultima_y_overword = original.ultima_y_overword;
			clone.ultima_x_overword = original.ultima_x_overword;
			clone.ultima_z_overword = original.ultima_z_overword;
			clone.ultima_y_nether = original.ultima_y_nether;
			clone.ultima_x_nether = original.ultima_x_nether;
			clone.ultima_z_nether = original.ultima_z_nether;
			clone.ultima_y_end = original.ultima_y_end;
			clone.ultima_x_end = original.ultima_x_end;
			clone.ultima_z_end = original.ultima_z_end;
			clone.switch_dimension = original.switch_dimension;
			if (!event.isWasDeath()) {
			}
		}
	}

	public static final Capability<PlayerVariables> PLAYER_VARIABLES_CAPABILITY = CapabilityManager.get(new CapabilityToken<PlayerVariables>() {
	});

	@Mod.EventBusSubscriber
	private static class PlayerVariablesProvider implements ICapabilitySerializable<Tag> {
		@SubscribeEvent
		public static void onAttachCapabilities(AttachCapabilitiesEvent<Entity> event) {
			if (event.getObject() instanceof Player && !(event.getObject() instanceof FakePlayer))
				event.addCapability(new ResourceLocation("utility", "player_variables"), new PlayerVariablesProvider());
		}

		private final PlayerVariables playerVariables = new PlayerVariables();
		private final LazyOptional<PlayerVariables> instance = LazyOptional.of(() -> playerVariables);

		@Override
		public <T> LazyOptional<T> getCapability(Capability<T> cap, Direction side) {
			return cap == PLAYER_VARIABLES_CAPABILITY ? instance.cast() : LazyOptional.empty();
		}

		@Override
		public Tag serializeNBT() {
			return playerVariables.writeNBT();
		}

		@Override
		public void deserializeNBT(Tag nbt) {
			playerVariables.readNBT(nbt);
		}
	}

	public static class PlayerVariables {
		public String last_key = "overword key";
		public double ultima_y_flat = 0.0;
		public double ultima_x_flat = 0;
		public double ultima_z_flat = 0;
		public double ultima_y_overword = 60.0;
		public double ultima_x_overword = 0;
		public double ultima_z_overword = 0;
		public double ultima_y_nether = 58.0;
		public double ultima_x_nether = 0;
		public double ultima_z_nether = 0;
		public double ultima_y_end = 59.0;
		public double ultima_x_end = 39.0;
		public double ultima_z_end = 15.0;
		public String switch_dimension = "\"false\"";

		public void syncPlayerVariables(Entity entity) {
			if (entity instanceof ServerPlayer serverPlayer)
				UtilityMod.PACKET_HANDLER.send(PacketDistributor.PLAYER.with(() -> serverPlayer), new PlayerVariablesSyncMessage(this));
		}

		public Tag writeNBT() {
			CompoundTag nbt = new CompoundTag();
			nbt.putString("last_key", last_key);
			nbt.putDouble("ultima_y_flat", ultima_y_flat);
			nbt.putDouble("ultima_x_flat", ultima_x_flat);
			nbt.putDouble("ultima_z_flat", ultima_z_flat);
			nbt.putDouble("ultima_y_overword", ultima_y_overword);
			nbt.putDouble("ultima_x_overword", ultima_x_overword);
			nbt.putDouble("ultima_z_overword", ultima_z_overword);
			nbt.putDouble("ultima_y_nether", ultima_y_nether);
			nbt.putDouble("ultima_x_nether", ultima_x_nether);
			nbt.putDouble("ultima_z_nether", ultima_z_nether);
			nbt.putDouble("ultima_y_end", ultima_y_end);
			nbt.putDouble("ultima_x_end", ultima_x_end);
			nbt.putDouble("ultima_z_end", ultima_z_end);
			nbt.putString("switch_dimension", switch_dimension);
			return nbt;
		}

		public void readNBT(Tag tag) {
			CompoundTag nbt = (CompoundTag) tag;
			last_key = nbt.getString("last_key");
			ultima_y_flat = nbt.getDouble("ultima_y_flat");
			ultima_x_flat = nbt.getDouble("ultima_x_flat");
			ultima_z_flat = nbt.getDouble("ultima_z_flat");
			ultima_y_overword = nbt.getDouble("ultima_y_overword");
			ultima_x_overword = nbt.getDouble("ultima_x_overword");
			ultima_z_overword = nbt.getDouble("ultima_z_overword");
			ultima_y_nether = nbt.getDouble("ultima_y_nether");
			ultima_x_nether = nbt.getDouble("ultima_x_nether");
			ultima_z_nether = nbt.getDouble("ultima_z_nether");
			ultima_y_end = nbt.getDouble("ultima_y_end");
			ultima_x_end = nbt.getDouble("ultima_x_end");
			ultima_z_end = nbt.getDouble("ultima_z_end");
			switch_dimension = nbt.getString("switch_dimension");
		}
	}

	public static class PlayerVariablesSyncMessage {
		private final PlayerVariables data;

		public PlayerVariablesSyncMessage(FriendlyByteBuf buffer) {
			this.data = new PlayerVariables();
			this.data.readNBT(buffer.readNbt());
		}

		public PlayerVariablesSyncMessage(PlayerVariables data) {
			this.data = data;
		}

		public static void buffer(PlayerVariablesSyncMessage message, FriendlyByteBuf buffer) {
			buffer.writeNbt((CompoundTag) message.data.writeNBT());
		}

		public static void handler(PlayerVariablesSyncMessage message, Supplier<NetworkEvent.Context> contextSupplier) {
			NetworkEvent.Context context = contextSupplier.get();
			context.enqueueWork(() -> {
				if (!context.getDirection().getReceptionSide().isServer()) {
					PlayerVariables variables = ((PlayerVariables) Minecraft.getInstance().player.getCapability(PLAYER_VARIABLES_CAPABILITY, null).orElse(new PlayerVariables()));
					variables.last_key = message.data.last_key;
					variables.ultima_y_flat = message.data.ultima_y_flat;
					variables.ultima_x_flat = message.data.ultima_x_flat;
					variables.ultima_z_flat = message.data.ultima_z_flat;
					variables.ultima_y_overword = message.data.ultima_y_overword;
					variables.ultima_x_overword = message.data.ultima_x_overword;
					variables.ultima_z_overword = message.data.ultima_z_overword;
					variables.ultima_y_nether = message.data.ultima_y_nether;
					variables.ultima_x_nether = message.data.ultima_x_nether;
					variables.ultima_z_nether = message.data.ultima_z_nether;
					variables.ultima_y_end = message.data.ultima_y_end;
					variables.ultima_x_end = message.data.ultima_x_end;
					variables.ultima_z_end = message.data.ultima_z_end;
					variables.switch_dimension = message.data.switch_dimension;
				}
			});
			context.setPacketHandled(true);
		}
	}
}
