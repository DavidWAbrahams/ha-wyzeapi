@@
 from .const import CONF_CLIENT, DOMAIN, IOT3_MODELS, LOCK_UPDATED
 from .token_manager import token_exception_handler
@@
-    skip_models = {"YD_BT1"} | IOT3_MODELS
+    skip_models = {"YD_BT1"} | IOT3_MODELS
@@
-    async_add_entities(locks + lock_bolts + lock_bolts_v2, True)
+    async_add_entities(locks + lock_bolts + lock_bolts_v2, True)
@@
 class WyzeLockBoltV2(CoordinatorEntity, homeassistant.components.lock.LockEntity):
@@
     async def async_lock(self, **kwargs):
-        await self.coordinator.lock_unlock(command="lock")
+        # Coordinator raises HomeAssistantError on failure so callers see it
+        await self.coordinator.lock_unlock(command="lock")
@@
     async def async_unlock(self, **kwargs):
-        await self.coordinator.lock_unlock(command="unlock")
+        await self.coordinator.lock_unlock(command="unlock")
